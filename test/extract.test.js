import { test } from 'node:test';
import assert from 'node:assert/strict';
import { extractFromPost, findAddresses } from '../src/parser/extract.js';

// Real, well-known mints (valid 32-byte base58):
const USDC = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';
const WSOL = 'So11111111111111111111111111111111111111112';

test('pure CA in post text', () => {
  const { addresses } = extractFromPost(`Launching now! CA: ${USDC}`);
  assert.equal(addresses.length, 1);
  assert.equal(addresses[0].address, USDC);
  assert.equal(addresses[0].source, 'text');
});

test('multiple distinct CAs are all found, deduped', () => {
  const { addresses } = extractFromPost(`${USDC} and ${WSOL} and again ${USDC}`);
  assert.deepEqual(addresses.map((a) => a.address), [USDC, WSOL]);
});

test('pump.fun link: address extracted from URL path', () => {
  const { addresses, links } = extractFromPost(`GO GO GO https://pump.fun/coin/${USDC}`);
  assert.equal(addresses.length, 1);
  assert.equal(addresses[0].address, USDC);
  assert.equal(addresses[0].source, 'pump.fun');
  assert.equal(addresses[0].maybePair, false);
  assert.equal(links[0].kind, 'pump.fun');
});

test('dexscreener link: address flagged as possible pair address', () => {
  const { addresses } = extractFromPost(`chart: https://dexscreener.com/solana/${USDC}`);
  assert.equal(addresses.length, 1);
  assert.equal(addresses[0].maybePair, true);
});

test('external site link with no CA goes to externalSites for fetching', () => {
  const { addresses, externalSites } = extractFromPost(
    'My new project is live: https://gettrumpmemes.example.com',
  );
  assert.equal(addresses.length, 0);
  assert.deepEqual(externalSites, ['https://gettrumpmemes.example.com']);
});

test('t.co entities: expanded_url is used', () => {
  const { addresses } = extractFromPost('check this https://t.co/abc123', {
    urls: [{ url: 'https://t.co/abc123', expanded_url: `https://pump.fun/coin/${WSOL}` }],
  });
  assert.equal(addresses.length, 1);
  assert.equal(addresses[0].address, WSOL);
});

test('social/media links are ignored, not fetched', () => {
  const { externalSites, links } = extractFromPost(
    'watch https://youtube.com/watch?v=abc and https://x.com/foo/status/1',
  );
  assert.deepEqual(externalSites, []);
  assert.ok(links.every((l) => l.kind === 'ignored'));
});

test('post with nothing relevant yields empty result', () => {
  const result = extractFromPost('gm everyone, big things coming soon!!!');
  assert.deepEqual(result.addresses, []);
  assert.deepEqual(result.externalSites, []);
});

test('base58-looking strings that are not 32-byte pubkeys are rejected', () => {
  // right alphabet, wrong decoded length
  assert.deepEqual(findAddresses('abcdefghjkmnpqrstuvwxyz123456789ABC'), []);
  // contains 0, O, I, l — not base58
  assert.deepEqual(findAddresses('O0Il' + 'a'.repeat(40)), []);
  // too short / too long windows
  assert.deepEqual(findAddresses('abc123'), []);
});

test('no partial match inside a longer base58 run', () => {
  // a 50-char base58 run must not yield a 44-char "address" from its middle
  const longRun = 'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN' + 'abcdefg';
  assert.deepEqual(findAddresses(longRun), []);
});

test('address inside URL is not double-counted as text source', () => {
  const { addresses } = extractFromPost(`https://pump.fun/coin/${USDC}`);
  assert.equal(addresses.length, 1);
  assert.equal(addresses[0].source, 'pump.fun');
});
