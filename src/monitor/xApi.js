// Thin client for the official X API v2 (paid tiers). Handles auth,
// rate limits (429 + x-rate-limit-reset) and transient 5xx retries.

const X_API_BASE = 'https://api.x.com/2';

// Tweet IDs are snowflakes: 41 bits of millisecond timestamp shifted left 22,
// offset from the Twitter epoch. This gives us the post's creation time with
// millisecond precision (created_at from the API only has second precision),
// which is what we use to measure detection latency.
const TWITTER_EPOCH_MS = 1_288_834_974_657n;

/** @param {string} id @returns {number} unix ms of tweet creation */
export function tweetIdToMs(id) {
  return Number((BigInt(id) >> 22n) + TWITTER_EPOCH_MS);
}

/** @param {number} ms @returns {string} smallest snowflake for that ms (useful in tests) */
export function msToTweetId(ms) {
  return ((BigInt(ms) - TWITTER_EPOCH_MS) << 22n).toString();
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export class XApi {
  /**
   * @param {{ bearerToken: string, logger: import('../util/logger.js').createLogger extends (...a:any)=>infer R ? R : any, fetchImpl?: typeof fetch, baseUrl?: string }} opts
   */
  constructor({ bearerToken, logger, fetchImpl = fetch, baseUrl = X_API_BASE }) {
    if (!bearerToken) throw new Error('XApi: bearerToken is required');
    this.bearerToken = bearerToken;
    this.logger = logger;
    this.fetch = fetchImpl;
    this.baseUrl = baseUrl;
  }

  /**
   * GET with rate-limit handling. On 429 waits until x-rate-limit-reset
   * (plus jitter) and retries; on 5xx retries with exponential backoff.
   */
  async request(pathname, { searchParams, maxRetries = 4 } = {}) {
    const url = new URL(this.baseUrl + pathname);
    for (const [k, v] of Object.entries(searchParams ?? {})) {
      if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    }

    let attempt = 0;
    for (;;) {
      const res = await this.fetch(url, {
        headers: { authorization: `Bearer ${this.bearerToken}` },
        signal: AbortSignal.timeout(15_000),
      });

      if (res.status === 429) {
        const resetSec = Number(res.headers.get('x-rate-limit-reset'));
        const waitMs = Number.isFinite(resetSec) && resetSec > 0
          ? Math.max(1_000, resetSec * 1000 - Date.now()) + 500 + Math.random() * 1_000
          : 30_000;
        this.logger?.warn('x api rate limited, waiting', {
          path: pathname,
          waitMs: Math.round(waitMs),
        });
        await sleep(waitMs);
        continue;
      }

      if (res.status >= 500 && attempt < maxRetries) {
        const backoff = 2_000 * 2 ** attempt;
        attempt += 1;
        this.logger?.warn('x api server error, retrying', { status: res.status, backoff });
        await sleep(backoff);
        continue;
      }

      if (!res.ok) {
        const body = await res.text().catch(() => '');
        throw new Error(`X API ${res.status} on ${pathname}: ${body.slice(0, 500)}`);
      }
      return res.json();
    }
  }

  /**
   * Search recent posts from the monitored accounts. One request covers all
   * accounts in the query (up to the tier's query-length limit), which is far
   * cheaper in rate-limit terms than per-user timeline polling.
   *
   * @param {{ query: string, sinceId?: string, maxResults?: number }} opts
   */
  async searchRecent({ query, sinceId, maxResults = 100 }) {
    return this.request('/tweets/search/recent', {
      searchParams: {
        query,
        since_id: sinceId,
        max_results: maxResults,
        'tweet.fields': 'created_at,entities,author_id',
        expansions: 'author_id',
        'user.fields': 'username',
      },
    });
  }

  // ---- filtered stream (Pro tier) ----

  async getStreamRules() {
    const data = await this.request('/tweets/search/stream/rules');
    return data.data ?? [];
  }

  async setStreamRules(ruleValues) {
    const existing = await this.getStreamRules();
    const wanted = new Set(ruleValues);
    const stale = existing.filter((r) => !wanted.has(r.value)).map((r) => r.id);
    const current = new Set(existing.map((r) => r.value));
    const toAdd = ruleValues.filter((v) => !current.has(v));

    if (stale.length > 0) {
      await this.#postRules({ delete: { ids: stale } });
    }
    if (toAdd.length > 0) {
      const res = await this.#postRules({ add: toAdd.map((value) => ({ value })) });
      const errors = res.errors ?? [];
      if (errors.length > 0) {
        throw new Error(`failed to add stream rules: ${JSON.stringify(errors).slice(0, 500)}`);
      }
    }
  }

  async #postRules(payload) {
    const res = await this.fetch(`${this.baseUrl}/tweets/search/stream/rules`, {
      method: 'POST',
      headers: {
        authorization: `Bearer ${this.bearerToken}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(15_000),
    });
    if (!res.ok && res.status !== 201) {
      const body = await res.text().catch(() => '');
      throw new Error(`X API ${res.status} updating stream rules: ${body.slice(0, 500)}`);
    }
    return res.json();
  }

  /**
   * Opens the filtered stream. Returns the raw Response — consumption and
   * reconnection live in stream.js.
   */
  async openStream() {
    const url = new URL(`${this.baseUrl}/tweets/search/stream`);
    url.searchParams.set('tweet.fields', 'created_at,entities,author_id');
    url.searchParams.set('expansions', 'author_id');
    url.searchParams.set('user.fields', 'username');
    const res = await this.fetch(url, {
      headers: { authorization: `Bearer ${this.bearerToken}` },
    });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      const err = new Error(`X API ${res.status} opening stream: ${body.slice(0, 500)}`);
      err.status = res.status;
      err.rateLimitReset = Number(res.headers.get('x-rate-limit-reset')) || undefined;
      throw err;
    }
    return res;
  }
}

/**
 * Builds `from:` query strings for the monitored accounts, chunked so each
 * query stays under the tier's length limit (512 chars on Basic/Pro search;
 * stream rules have the same order of magnitude).
 *
 * @param {string[]} accounts usernames without @
 * @param {{ includeReplies?: boolean, includeRetweets?: boolean, maxLen?: number }} [opts]
 * @returns {string[]} one or more query strings
 */
export function buildAccountQueries(accounts, { includeReplies = false, includeRetweets = false, maxLen = 512 } = {}) {
  const suffix =
    (includeRetweets ? '' : ' -is:retweet') + (includeReplies ? '' : ' -is:reply');
  const queries = [];
  let current = [];

  const render = (parts) => `(${parts.join(' OR ')})${suffix}`;

  for (const account of accounts) {
    const clause = `from:${account.replace(/^@/, '')}`;
    const candidate = [...current, clause];
    if (current.length > 0 && render(candidate).length > maxLen) {
      queries.push(render(current));
      current = [clause];
    } else {
      current = candidate;
    }
  }
  if (current.length > 0) queries.push(render(current));
  return queries;
}
