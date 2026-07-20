// Filtered-stream monitor (X API v2, Pro tier). Lower latency than polling:
// posts are pushed within ~1-5s of publication. Handles keep-alives, stalled
// connections and reconnection with exponential backoff.

import { tweetIdToMs, buildAccountQueries } from './xApi.js';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// X sends a keep-alive (\r\n) at least every 20s; if we see nothing for
// longer than this, the connection is considered dead.
const STALL_TIMEOUT_MS = 30_000;

export class StreamMonitor {
  /**
   * @param {{
   *   xApi: import('./xApi.js').XApi,
   *   accounts: string[],
   *   includeReplies?: boolean,
   *   includeRetweets?: boolean,
   *   logger: any,
   *   onTweet: (tweet: object, ctx: { username: string, detectedAtMs: number, detectionLatencyMs: number }) => Promise<void> | void,
   * }} opts
   */
  constructor({ xApi, accounts, includeReplies, includeRetweets, logger, onTweet }) {
    this.xApi = xApi;
    // Stream rules are limited to 512 chars each on Pro.
    this.rules = buildAccountQueries(accounts, { includeReplies, includeRetweets, maxLen: 512 });
    this.logger = logger;
    this.onTweet = onTweet;
    this.stopped = false;
  }

  stop() {
    this.stopped = true;
  }

  async run() {
    this.logger.info('configuring stream rules', { rules: this.rules.length });
    await this.xApi.setStreamRules(this.rules);

    let backoffMs = 2_000;
    while (!this.stopped) {
      try {
        this.logger.info('connecting to filtered stream');
        const res = await this.xApi.openStream();
        this.logger.info('stream connected');
        backoffMs = 2_000; // reset on successful connect
        await this.#consume(res);
        if (!this.stopped) this.logger.warn('stream ended, reconnecting');
      } catch (err) {
        if (this.stopped) break;
        if (err.status === 429) {
          const waitMs = err.rateLimitReset
            ? Math.max(5_000, err.rateLimitReset * 1000 - Date.now())
            : 60_000;
          this.logger.warn('stream rate limited', { waitMs });
          await sleep(waitMs);
          continue;
        }
        this.logger.error('stream error, backing off', { error: err.message, backoffMs });
        await sleep(backoffMs);
        backoffMs = Math.min(backoffMs * 2, 60_000);
      }
    }
    this.logger.info('stream monitor stopped');
  }

  async #consume(res) {
    let buffer = '';
    let lastDataAt = Date.now();

    const reader = res.body.getReader();
    const watchdog = setInterval(() => {
      if (Date.now() - lastDataAt > STALL_TIMEOUT_MS) {
        this.logger.warn('stream stalled (no keep-alive), aborting connection');
        reader.cancel().catch(() => {});
      }
    }, 5_000);

    try {
      const decoder = new TextDecoder();
      for (;;) {
        const { done, value } = await reader.read();
        if (done || this.stopped) break;
        lastDataAt = Date.now();
        buffer += decoder.decode(value, { stream: true });

        let idx;
        while ((idx = buffer.indexOf('\r\n')) !== -1) {
          const line = buffer.slice(0, idx);
          buffer = buffer.slice(idx + 2);
          if (line.trim() === '') continue; // keep-alive
          await this.#handleLine(line);
        }
      }
    } finally {
      clearInterval(watchdog);
      reader.cancel().catch(() => {});
    }
  }

  async #handleLine(line) {
    let payload;
    try {
      payload = JSON.parse(line);
    } catch {
      this.logger.warn('unparseable stream line', { line: line.slice(0, 200) });
      return;
    }
    if (payload.errors && !payload.data) {
      this.logger.error('stream payload error', { errors: payload.errors });
      return;
    }
    const tweet = payload.data;
    if (!tweet?.id) return;

    const detectedAtMs = Date.now();
    const users = new Map((payload.includes?.users ?? []).map((u) => [u.id, u.username]));
    const username = users.get(tweet.author_id) ?? tweet.author_id;
    const detectionLatencyMs = detectedAtMs - tweetIdToMs(tweet.id);
    this.logger.info('new post detected (stream)', {
      tweetId: tweet.id,
      username,
      detectionLatencyMs,
    });
    await this.onTweet(tweet, { username, detectedAtMs, detectionLatencyMs });
  }
}
