// Extracts Solana contract-address candidates from a post: raw base58 in the
// text, addresses embedded in known launch/chart URLs, and external links
// worth fetching. Pure functions, no I/O — fully unit-testable.

import { isSolanaAddress } from '../util/base58.js';

// Base58 run of plausible pubkey length, with boundaries so we never match a
// 32-44 char window inside a longer base58-looking run (e.g. long hashes).
const ADDRESS_RE = /(?<![1-9A-HJ-NP-Za-km-z])[1-9A-HJ-NP-Za-km-z]{32,44}(?![1-9A-HJ-NP-Za-km-z])/g;
const URL_RE = /https?:\/\/[^\s<>"'\)\]]+/gi;

// Domains where a base58 path segment identifies the token (or pair) directly.
const KNOWN_DOMAINS = [
  { match: /(^|\.)pump\.fun$/i, kind: 'pump.fun' },
  { match: /(^|\.)dexscreener\.com$/i, kind: 'dexscreener', maybePair: true },
  { match: /(^|\.)birdeye\.so$/i, kind: 'birdeye' },
  { match: /(^|\.)solscan\.io$/i, kind: 'solscan' },
  { match: /(^|\.)geckoterminal\.com$/i, kind: 'geckoterminal', maybePair: true },
  { match: /(^|\.)raydium\.io$/i, kind: 'raydium' },
  { match: /(^|\.)jup\.ag$/i, kind: 'jupiter' },
];

// Link-shortener/infra domains that are never a token site worth scraping.
const IGNORED_EXTERNAL = /(^|\.)(t\.co|x\.com|twitter\.com|youtube\.com|youtu\.be|instagram\.com|tiktok\.com)$/i;

/** @param {string} str */
export function findAddresses(str) {
  const seen = new Set();
  const out = [];
  for (const match of str.matchAll(ADDRESS_RE)) {
    const candidate = match[0];
    if (!seen.has(candidate) && isSolanaAddress(candidate)) {
      seen.add(candidate);
      out.push(candidate);
    }
  }
  return out;
}

function classifyUrl(rawUrl) {
  let url;
  try {
    url = new URL(rawUrl);
  } catch {
    return null;
  }
  const hostname = url.hostname.replace(/^www\./i, '');
  const known = KNOWN_DOMAINS.find((d) => d.match.test(hostname));
  const addresses = findAddresses(decodeURIComponent(url.pathname + url.search));

  if (known) {
    return {
      url: rawUrl,
      domain: hostname,
      kind: known.kind,
      addresses,
      maybePair: Boolean(known.maybePair) && addresses.length > 0,
    };
  }
  if (IGNORED_EXTERNAL.test(hostname)) {
    return { url: rawUrl, domain: hostname, kind: 'ignored', addresses, maybePair: false };
  }
  return { url: rawUrl, domain: hostname, kind: 'external', addresses, maybePair: false };
}

/**
 * @param {string} text post text
 * @param {{ urls?: Array<{ url?: string, expanded_url?: string }> }} [entities]
 *   X API v2 tweet.entities — expanded_url resolves t.co wrappers for us.
 * @returns {{
 *   addresses: Array<{ address: string, source: string, url?: string, maybePair: boolean }>,
 *   links: Array<{ url: string, domain: string, kind: string, addresses: string[], maybePair: boolean }>,
 *   externalSites: string[],
 * }}
 */
export function extractFromPost(text, entities) {
  const rawUrls = new Set();
  for (const e of entities?.urls ?? []) {
    const expanded = e.expanded_url || e.url;
    if (expanded) rawUrls.add(expanded);
  }
  // Strip URLs from the text before scanning for raw addresses, so base58-ish
  // path segments are attributed to their link, not double-counted as text.
  let strippedText = text ?? '';
  for (const match of strippedText.matchAll(URL_RE)) rawUrls.add(match[0]);
  strippedText = strippedText.replace(URL_RE, ' ');

  const links = [];
  for (const rawUrl of rawUrls) {
    const link = classifyUrl(rawUrl);
    if (link) links.push(link);
  }

  const addresses = [];
  const seen = new Set();
  const push = (address, source, url, maybePair = false) => {
    if (seen.has(address)) return;
    seen.add(address);
    addresses.push({ address, source, url, maybePair });
  };

  for (const address of findAddresses(strippedText)) push(address, 'text');
  for (const link of links) {
    if (link.kind === 'ignored') continue;
    for (const address of link.addresses) {
      push(address, link.kind === 'external' ? 'url' : link.kind, link.url, link.maybePair);
    }
  }

  const externalSites = links
    .filter((l) => l.kind === 'external' && l.addresses.length === 0)
    .map((l) => l.url);

  return { addresses, links, externalSites };
}
