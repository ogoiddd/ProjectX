// Per-post pipeline: parse -> (optional external-site scan) -> validate ->
// alert -> (optional) execute. Kept separate from index.js so it can be
// exercised in tests with injected dependencies.

import { extractFromPost } from './parser/extract.js';
import { fetchAndScan } from './parser/siteScan.js';

export class Pipeline {
  /**
   * @param {{
   *   config: object,
   *   validator: import('./validator/caValidator.js').CaValidator,
   *   notifier: import('./alerts/notifier.js').Notifier,
   *   executor?: import('./executor/executor.js').Executor | null,
   *   logger: any,
   *   fetchImpl?: typeof fetch,
   * }} opts
   */
  constructor({ config, validator, notifier, executor = null, logger, fetchImpl = fetch }) {
    this.config = config;
    this.validator = validator;
    this.notifier = notifier;
    this.executor = executor;
    this.logger = logger;
    this.fetch = fetchImpl;
    // Dedup: never alert twice for the same mint (bounded memory).
    this.seenAddresses = new Set();
  }

  #markSeen(address) {
    if (this.seenAddresses.size > 5_000) this.seenAddresses.clear();
    this.seenAddresses.add(address);
  }

  /**
   * @param {{ id: string, text: string, entities?: object }} tweet
   * @param {{ username: string, detectionLatencyMs: number }} ctx
   */
  async handleTweet(tweet, ctx) {
    const parsed = extractFromPost(tweet.text ?? '', tweet.entities);
    const candidates = [...parsed.addresses];

    // No address in text/links: fall back to scanning linked external sites.
    if (candidates.length === 0 && parsed.externalSites.length > 0 && this.config.parser.fetchExternalSites) {
      const sites = parsed.externalSites.slice(0, this.config.parser.maxExternalSitesPerPost);
      const scans = await Promise.all(
        sites.map((url) =>
          fetchAndScan(url, {
            timeoutMs: this.config.parser.siteFetchTimeoutMs,
            maxBytes: this.config.parser.maxSiteBytes,
            fetchImpl: this.fetch,
            logger: this.logger,
          }),
        ),
      );
      for (const scan of scans) {
        this.logger.info('external site scanned', {
          url: scan.url,
          fetchMs: scan.fetchMs,
          candidates: scan.candidates.length,
        });
        // Only trust the top-ranked candidate per site; pages are noisy.
        const best = scan.candidates[0];
        if (best) candidates.push({ address: best.address, source: 'site', url: scan.url, maybePair: false });
      }
    }

    if (candidates.length === 0) {
      this.logger.debug('no address candidates in post', { tweetId: tweet.id });
      return [];
    }

    const results = [];
    for (const candidate of candidates) {
      if (this.seenAddresses.has(candidate.address)) {
        this.logger.debug('address already seen, skipping', { address: candidate.address });
        continue;
      }
      this.#markSeen(candidate.address);

      const validation = await this.validator.validate(candidate.address, {
        maybePair: candidate.maybePair,
      });
      // Pair links resolve to a different (token) address — dedupe on it too.
      this.#markSeen(validation.address);

      if (!validation.valid && this.config.validation.requireOnChainMint) {
        this.logger.warn('candidate failed validation, no alert', {
          address: validation.address,
          reason: validation.reason,
        });
        continue;
      }

      await this.notifier.sendTokenAlert({
        username: ctx.username,
        tweetId: tweet.id,
        address: validation.address,
        source: candidate.source,
        sourceUrl: candidate.url,
        detectionLatencyMs: ctx.detectionLatencyMs,
        validation,
      });

      let execution = { status: 'disabled' };
      if (this.executor) {
        execution = await this.executor.execute({
          mint: validation.address,
          trigger: { username: ctx.username, tweetId: tweet.id },
        });
        if (execution.status !== 'disabled') {
          await this.notifier.sendText(
            `⚙️ Execução (${execution.mode ?? '-'}): ${execution.status} — mint ${validation.address}` +
              (execution.signature ? `\nhttps://solscan.io/tx/${execution.signature}` : '') +
              (execution.error ? `\nErro: ${execution.error}` : ''),
          );
        }
      }

      results.push({ address: validation.address, validation, execution });
    }
    return results;
  }
}
