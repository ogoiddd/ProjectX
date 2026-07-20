// Polling monitor built on /2/tweets/search/recent. A single query covers all
// monitored accounts (chunked if needed), which is far more rate-limit
// efficient than hitting per-user timeline endpoints.

import { tweetIdToMs, buildAccountQueries } from './xApi.js';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export class Poller {
  /**
   * @param {{
   *   xApi: import('./xApi.js').XApi,
   *   accounts: string[],
   *   pollIntervalMs: number,
   *   includeReplies?: boolean,
   *   includeRetweets?: boolean,
   *   logger: any,
   *   onTweet: (tweet: object, ctx: { username: string, detectedAtMs: number, detectionLatencyMs: number }) => Promise<void> | void,
   * }} opts
   */
  constructor({ xApi, accounts, pollIntervalMs, includeReplies, includeRetweets, logger, onTweet }) {
    this.xApi = xApi;
    this.queries = buildAccountQueries(accounts, { includeReplies, includeRetweets });
    this.pollIntervalMs = pollIntervalMs;
    this.logger = logger;
    this.onTweet = onTweet;
    // since_id per query chunk; null until the baseline poll establishes it.
    this.sinceIds = new Array(this.queries.length).fill(null);
    this.stopped = false;
  }

  stop() {
    this.stopped = true;
  }

  async run() {
    this.logger.info('poller starting', {
      queries: this.queries.length,
      pollIntervalMs: this.pollIntervalMs,
    });

    // Baseline pass: record the newest tweet id per query without alerting,
    // so a restart does not replay old posts.
    for (let i = 0; i < this.queries.length; i++) {
      try {
        const data = await this.xApi.searchRecent({ query: this.queries[i], maxResults: 10 });
        this.sinceIds[i] = data.meta?.newest_id ?? null;
      } catch (err) {
        this.logger.warn('baseline poll failed, will retry in loop', { error: err.message });
      }
    }
    this.logger.info('poller baseline established', { sinceIds: this.sinceIds });

    while (!this.stopped) {
      const cycleStart = Date.now();
      for (let i = 0; i < this.queries.length && !this.stopped; i++) {
        try {
          await this.#pollOnce(i);
        } catch (err) {
          this.logger.error('poll cycle failed', { query: i, error: err.message });
        }
      }
      const elapsed = Date.now() - cycleStart;
      const wait = Math.max(250, this.pollIntervalMs - elapsed);
      await sleep(wait);
    }
    this.logger.info('poller stopped');
  }

  async #pollOnce(queryIndex) {
    const sinceId = this.sinceIds[queryIndex];
    const data = await this.xApi.searchRecent({
      query: this.queries[queryIndex],
      sinceId: sinceId ?? undefined,
      // Without a baseline yet, keep the window tiny to avoid replaying history.
      maxResults: sinceId ? 100 : 10,
    });
    const detectedAtMs = Date.now();

    if (data.meta?.newest_id) this.sinceIds[queryIndex] = data.meta.newest_id;
    if (sinceId === null) return; // this call only established the baseline

    const tweets = data.data ?? [];
    if (tweets.length === 0) return;

    const users = new Map((data.includes?.users ?? []).map((u) => [u.id, u.username]));

    // API returns newest first; process oldest first to keep ordering sane.
    for (const tweet of [...tweets].reverse()) {
      const username = users.get(tweet.author_id) ?? tweet.author_id;
      const detectionLatencyMs = detectedAtMs - tweetIdToMs(tweet.id);
      this.logger.info('new post detected', {
        tweetId: tweet.id,
        username,
        detectionLatencyMs,
      });
      await this.onTweet(tweet, { username, detectedAtMs, detectionLatencyMs });
    }
  }
}
