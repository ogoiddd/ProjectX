import { test } from 'node:test';
import assert from 'node:assert/strict';
import { b58decode, b58encode, isSolanaAddress } from '../src/util/base58.js';
import { tweetIdToMs, msToTweetId, buildAccountQueries } from '../src/monitor/xApi.js';

test('base58 round-trips arbitrary bytes', () => {
  const cases = [
    Buffer.from([0]),
    Buffer.from([0, 0, 1, 2, 3]),
    Buffer.from('hello world'),
    Buffer.alloc(32, 7),
  ];
  for (const buf of cases) {
    assert.deepEqual(b58decode(b58encode(buf)), buf);
  }
});

test('known Solana addresses decode to 32 bytes', () => {
  assert.equal(b58decode('So11111111111111111111111111111111111111112').length, 32);
  assert.equal(isSolanaAddress('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'), true);
  assert.equal(isSolanaAddress('notbase58!!!'), false);
  assert.equal(isSolanaAddress('abc'), false);
});

test('snowflake conversion round-trips', () => {
  const ms = Date.UTC(2025, 0, 17, 22, 30, 0); // around the $TRUMP launch
  assert.equal(tweetIdToMs(msToTweetId(ms)), ms);
});

test('account queries are chunked under the length limit', () => {
  const accounts = Array.from({ length: 40 }, (_, i) => `some_long_username_${i}`);
  const queries = buildAccountQueries(accounts, { maxLen: 512 });
  assert.ok(queries.length > 1);
  for (const q of queries) {
    assert.ok(q.length <= 512, `query too long: ${q.length}`);
    assert.match(q, /^\(from:/);
    assert.match(q, /-is:retweet -is:reply$/);
  }
  const total = queries.join(' ').match(/from:/g).length;
  assert.equal(total, 40);
});
