// Fetches an external site linked from a post and scans the HTML for a
// Solana contract address. Scanning is separated from fetching so it can be
// unit-tested with plain strings.

import { findAddresses } from './extract.js';

// Words that typically sit next to a published contract address.
const KEYWORD_RE = /(contract|token\s*address|\bCA\b|\bmint\b|\bcontrato\b|\bendere[cç]o\b)/gi;
const KEYWORD_WINDOW = 300;

/**
 * Scans HTML/text for address candidates, ranked by (a) distance to the
 * nearest contract-related keyword, then (b) number of occurrences.
 *
 * @param {string} html
 * @param {{ max?: number }} [opts]
 * @returns {Array<{ address: string, occurrences: number, nearKeyword: boolean, keywordDistance: number }>}
 */
export function scanHtmlForAddresses(html, { max = 5 } = {}) {
  if (!html) return [];

  const keywordRanges = [...html.matchAll(KEYWORD_RE)].map((m) => [m.index, m.index + m[0].length]);
  const stats = new Map();

  for (const address of findAddresses(html)) {
    let occurrences = 0;
    let keywordDistance = Infinity;
    let idx = html.indexOf(address);
    while (idx !== -1) {
      occurrences += 1;
      const end = idx + address.length;
      for (const [kwStart, kwEnd] of keywordRanges) {
        // A label ("Contract Address:", "CA:") normally *precedes* the value,
        // so an address before the keyword gets a heavy distance penalty.
        let dist;
        if (idx >= kwEnd) dist = idx - kwEnd;
        else if (kwStart >= end) dist = (kwStart - end) * 4 + 1;
        else dist = 0; // overlapping
        if (dist < keywordDistance) keywordDistance = dist;
      }
      idx = html.indexOf(address, end);
    }
    stats.set(address, {
      address,
      occurrences,
      keywordDistance,
      nearKeyword: keywordDistance <= KEYWORD_WINDOW,
    });
  }

  return [...stats.values()]
    .sort((a, b) => a.keywordDistance - b.keywordDistance || b.occurrences - a.occurrences)
    .slice(0, max);
}

/**
 * Fetches a URL with timeout and size cap, then scans it.
 *
 * @param {string} url
 * @param {{ timeoutMs?: number, maxBytes?: number, fetchImpl?: typeof fetch, logger?: any }} [opts]
 */
export async function fetchAndScan(url, { timeoutMs = 5_000, maxBytes = 1_500_000, fetchImpl = fetch, logger } = {}) {
  const startedAt = Date.now();
  let res;
  try {
    res = await fetchImpl(url, {
      redirect: 'follow',
      signal: AbortSignal.timeout(timeoutMs),
      headers: {
        // Some token sites block default fetch UAs.
        'user-agent':
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
        accept: 'text/html,application/xhtml+xml,*/*;q=0.8',
      },
    });
  } catch (err) {
    logger?.warn('site fetch failed', { url, error: err.message });
    return { url, candidates: [], fetchMs: Date.now() - startedAt, error: err.message };
  }

  if (!res.ok) {
    logger?.warn('site fetch non-200', { url, status: res.status });
    return { url, candidates: [], fetchMs: Date.now() - startedAt, error: `HTTP ${res.status}` };
  }

  // Read incrementally so a huge page cannot blow up memory.
  let html = '';
  let bytes = 0;
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      html += decoder.decode(value, { stream: true });
      if (bytes >= maxBytes) {
        await reader.cancel().catch(() => {});
        break;
      }
    }
  } catch (err) {
    logger?.warn('site body read failed', { url, error: err.message });
  }

  const candidates = scanHtmlForAddresses(html);
  return { url, candidates, fetchMs: Date.now() - startedAt };
}
