import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { Executor } from '../src/executor/executor.js';
import { DEFAULT_CONFIG } from '../src/config.js';

const USDC = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v';

function makeExecutor(overrides = {}, { env = {}, fetchImpl, cwd } = {}) {
  const dir = cwd ?? mkdtempSync(path.join(tmpdir(), 'exec-test-'));
  const executor = new Executor({
    config: { ...DEFAULT_CONFIG.executor, ...overrides },
    rpcUrl: 'http://rpc.invalid',
    env,
    fetchImpl:
      fetchImpl ??
      (async () => {
        throw new Error('unexpected network call');
      }),
    cwd: dir,
  });
  return { executor, dir };
}

test('executor is disabled by default and makes no network calls', async () => {
  const { executor } = makeExecutor();
  const result = await executor.execute({ mint: USDC, trigger: {} });
  assert.equal(result.status, 'disabled');
});

test('kill switch via env blocks trades even when enabled', async () => {
  const { executor } = makeExecutor({ enabled: true }, { env: { KILL_SWITCH: '1' } });
  const result = await executor.execute({ mint: USDC, trigger: {} });
  assert.equal(result.status, 'kill_switch');
});

test('kill switch via file blocks trades even when enabled', async () => {
  const dir = mkdtempSync(path.join(tmpdir(), 'exec-test-'));
  writeFileSync(path.join(dir, 'KILL_SWITCH'), '');
  const { executor } = makeExecutor({ enabled: true }, { cwd: dir });
  const result = await executor.execute({ mint: USDC, trigger: {} });
  assert.equal(result.status, 'kill_switch');
  rmSync(dir, { recursive: true, force: true });
});

test('buy amount above per-trade limit is rejected before any network call', async () => {
  const { executor } = makeExecutor({ enabled: true, buyAmountSol: 1, maxSolPerTrade: 0.05 });
  const result = await executor.execute({ mint: USDC, trigger: {} });
  assert.equal(result.status, 'limit_exceeded');
});

test('paper mode gets a quote, records the trade, and never builds a swap', async () => {
  const calls = [];
  const fetchImpl = async (url) => {
    calls.push(String(url));
    assert.match(String(url), /\/quote\?/, 'paper mode must only hit /quote');
    return new Response(
      JSON.stringify({ outAmount: '123456', priceImpactPct: '0.01' }),
      { status: 200, headers: { 'content-type': 'application/json' } },
    );
  };
  const { executor } = makeExecutor({ enabled: true, paperTrading: true }, { fetchImpl });
  const result = await executor.execute({ mint: USDC, trigger: { username: 'test' } });
  assert.equal(result.status, 'simulated');
  assert.equal(result.mode, 'paper');
  assert.equal(result.outAmount, '123456');
  assert.equal(calls.length, 1);
});

test('live mode without a burner key fails safely', async () => {
  const fetchImpl = async () =>
    new Response(JSON.stringify({ outAmount: '1', priceImpactPct: '0' }), { status: 200 });
  const { executor } = makeExecutor(
    { enabled: true, paperTrading: false },
    { fetchImpl, env: {} },
  );
  const result = await executor.execute({ mint: USDC, trigger: {} });
  assert.equal(result.status, 'error');
  assert.match(result.error, /BURNER_WALLET_PRIVATE_KEY/);
});
