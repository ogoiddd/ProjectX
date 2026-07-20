import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CaValidator } from '../src/validator/caValidator.js';

const USDC = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';
const TOKEN_PROGRAM = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';

const jsonResponse = (body) =>
  new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json' } });

function makeValidator(handler) {
  return new CaValidator({ rpcUrl: 'http://rpc.test', fetchImpl: handler });
}

test('valid SPL mint passes validation with dexscreener enrichment', async () => {
  const validator = makeValidator(async (url) => {
    if (String(url).startsWith('http://rpc.test')) {
      return jsonResponse({
        result: {
          value: {
            owner: TOKEN_PROGRAM,
            data: { parsed: { type: 'mint', info: { supply: '1000', decimals: 6 } } },
          },
        },
      });
    }
    return jsonResponse({
      pairs: [
        {
          chainId: 'solana',
          baseToken: { name: 'USD Coin', symbol: 'USDC', address: USDC },
          priceUsd: '1.00',
          liquidity: { usd: 5_000_000 },
          url: 'https://dexscreener.com/solana/pair',
        },
      ],
    });
  });
  const result = await validator.validate(USDC);
  assert.equal(result.valid, true);
  assert.equal(result.dex.symbol, 'USDC');
});

test('nonexistent account fails validation', async () => {
  const validator = makeValidator(async () => jsonResponse({ result: { value: null } }));
  const result = await validator.validate(USDC, { enrich: false });
  assert.equal(result.valid, false);
  assert.equal(result.reason, 'not_found_on_chain');
});

test('account that is not a token mint fails validation', async () => {
  const validator = makeValidator(async () =>
    jsonResponse({ result: { value: { owner: '11111111111111111111111111111111', data: {} } } }),
  );
  const result = await validator.validate(USDC, { enrich: false });
  assert.equal(result.valid, false);
  assert.equal(result.reason, 'not_a_token_mint');
});

test('pair address is resolved to the base token before on-chain check', async () => {
  const PAIR = '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU';
  const seen = [];
  const validator = makeValidator(async (url) => {
    seen.push(String(url));
    if (String(url).includes('/dex/pairs/solana/')) {
      return jsonResponse({ pairs: [{ baseToken: { address: USDC } }] });
    }
    if (String(url).startsWith('http://rpc.test')) {
      return jsonResponse({
        result: { value: { owner: TOKEN_PROGRAM, data: { parsed: { type: 'mint', info: {} } } } },
      });
    }
    return jsonResponse({ pairs: [] });
  });
  const result = await validator.validate(PAIR, { maybePair: true, enrich: false });
  assert.equal(result.valid, true);
  assert.equal(result.address, USDC);
  assert.ok(seen[0].includes(PAIR));
});
