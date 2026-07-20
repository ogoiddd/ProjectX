// OPTIONAL execution module — disabled by default, and paper trading by
// default even when enabled. Safety order, checked on EVERY trade:
//   1. executor.enabled (config) must be true
//   2. kill switch must be off (env KILL_SWITCH=1 or presence of the
//      kill-switch file both block instantly, no restart needed)
//   3. hard limits: buyAmountSol <= maxSolPerTrade, slippage <= maxSlippageBps
//   4. paper mode only simulates: gets a real Jupiter quote, logs it, never
//      touches a wallet
// Live mode additionally requires BURNER_WALLET_PRIVATE_KEY in the
// environment (never in code or config files).

import { existsSync, mkdirSync, appendFileSync } from 'node:fs';
import path from 'node:path';
import { loadKeypair, signTransaction } from './signer.js';

const WSOL_MINT = 'So11111111111111111111111111111111111111112';
const LAMPORTS_PER_SOL = 1_000_000_000;

export class Executor {
  /**
   * @param {{
   *   config: typeof import('../config.js').DEFAULT_CONFIG['executor'],
   *   rpcUrl: string,
   *   getPrivateKey?: () => string | undefined,
   *   env?: NodeJS.ProcessEnv,
   *   fetchImpl?: typeof fetch,
   *   logger?: any,
   *   cwd?: string,
   * }} opts
   */
  constructor({ config, rpcUrl, getPrivateKey, env = process.env, fetchImpl = fetch, logger, cwd = process.cwd() }) {
    this.config = config;
    this.rpcUrl = rpcUrl;
    this.getPrivateKey = getPrivateKey ?? (() => env.BURNER_WALLET_PRIVATE_KEY);
    this.env = env;
    this.fetch = fetchImpl;
    this.logger = logger;
    this.killSwitchPath = path.resolve(cwd, config.killSwitchFile);
    this.tradesLogPath = path.resolve(cwd, config.tradesLogFile);
  }

  isKillSwitchActive() {
    return this.env.KILL_SWITCH === '1' || existsSync(this.killSwitchPath);
  }

  #recordTrade(record) {
    try {
      mkdirSync(path.dirname(this.tradesLogPath), { recursive: true });
      appendFileSync(this.tradesLogPath, JSON.stringify({ ts: new Date().toISOString(), ...record }) + '\n');
    } catch (err) {
      this.logger?.error('failed to write trades log', { error: err.message });
    }
  }

  /**
   * Attempts a SOL -> token buy for a validated mint.
   * @param {{ mint: string, trigger: { username?: string, tweetId?: string } }} opts
   * @returns {Promise<{ status: string, [k: string]: any }>}
   */
  async execute({ mint, trigger }) {
    const cfg = this.config;
    if (!cfg.enabled) return { status: 'disabled' };

    if (this.isKillSwitchActive()) {
      this.logger?.warn('kill switch active, trade blocked', { mint });
      return { status: 'kill_switch' };
    }

    if (cfg.buyAmountSol > cfg.maxSolPerTrade) {
      return {
        status: 'limit_exceeded',
        reason: `buyAmountSol ${cfg.buyAmountSol} > maxSolPerTrade ${cfg.maxSolPerTrade}`,
      };
    }
    if (!(cfg.maxSlippageBps > 0 && cfg.maxSlippageBps <= 10_000)) {
      return { status: 'limit_exceeded', reason: `invalid maxSlippageBps ${cfg.maxSlippageBps}` };
    }

    const amountLamports = Math.floor(cfg.buyAmountSol * LAMPORTS_PER_SOL);
    let quote;
    try {
      quote = await this.#getQuote(mint, amountLamports);
    } catch (err) {
      this.logger?.error('jupiter quote failed', { mint, error: err.message });
      return { status: 'quote_failed', error: err.message };
    }

    const summary = {
      mint,
      mode: cfg.paperTrading ? 'paper' : 'live',
      inAmountSol: cfg.buyAmountSol,
      outAmount: quote.outAmount,
      priceImpactPct: quote.priceImpactPct,
      slippageBps: cfg.maxSlippageBps,
      trigger,
    };

    if (cfg.paperTrading) {
      this.logger?.info('paper trade simulated', summary);
      this.#recordTrade({ ...summary, status: 'simulated' });
      return { status: 'simulated', ...summary };
    }

    // ---- LIVE ----
    const secret = this.getPrivateKey();
    if (!secret) return { status: 'error', error: 'BURNER_WALLET_PRIVATE_KEY not set' };
    let keypair;
    try {
      keypair = loadKeypair(secret);
    } catch (err) {
      return { status: 'error', error: `invalid burner key: ${err.message}` };
    }

    try {
      const swapTx = await this.#buildSwapTx(quote, keypair.publicKey);
      const { signedTxBase64, signatureBase58 } = signTransaction(swapTx, keypair);
      const signature = await this.#sendTransaction(signedTxBase64);
      const result = { ...summary, status: 'sent', signature: signature ?? signatureBase58 };
      this.logger?.info('live trade sent', result);
      this.#recordTrade(result);
      return result;
    } catch (err) {
      this.logger?.error('live trade failed', { mint, error: err.message });
      this.#recordTrade({ ...summary, status: 'failed', error: err.message });
      return { status: 'failed', error: err.message, ...summary };
    }
  }

  async #getQuote(outputMint, amountLamports) {
    const url = new URL(`${this.config.jupiterBaseUrl}/quote`);
    url.searchParams.set('inputMint', WSOL_MINT);
    url.searchParams.set('outputMint', outputMint);
    url.searchParams.set('amount', String(amountLamports));
    url.searchParams.set('slippageBps', String(this.config.maxSlippageBps));
    const res = await this.fetch(url, { signal: AbortSignal.timeout(8_000) });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      throw new Error(`quote HTTP ${res.status}: ${body.slice(0, 300)}`);
    }
    return res.json();
  }

  async #buildSwapTx(quoteResponse, userPublicKey) {
    const res = await this.fetch(`${this.config.jupiterBaseUrl}/swap`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        quoteResponse,
        userPublicKey,
        wrapAndUnwrapSol: true,
        dynamicComputeUnitLimit: true,
        prioritizationFeeLamports: this.config.priorityFeeLamports,
      }),
      signal: AbortSignal.timeout(10_000),
    });
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      throw new Error(`swap build HTTP ${res.status}: ${body.slice(0, 300)}`);
    }
    const body = await res.json();
    if (!body.swapTransaction) throw new Error('swap response missing swapTransaction');
    return body.swapTransaction;
  }

  async #sendTransaction(signedTxBase64) {
    const res = await this.fetch(this.rpcUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'sendTransaction',
        params: [
          signedTxBase64,
          { encoding: 'base64', skipPreflight: this.config.skipPreflight, maxRetries: 3 },
        ],
      }),
      signal: AbortSignal.timeout(10_000),
    });
    if (!res.ok) throw new Error(`sendTransaction HTTP ${res.status}`);
    const body = await res.json();
    if (body.error) throw new Error(`sendTransaction: ${body.error.message}`);
    return body.result;
  }
}
