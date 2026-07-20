// Validates a candidate contract address before any alert or trade:
//  1. on-chain: the account must exist and be an SPL token mint
//     (Token Program or Token-2022) — via Solana JSON-RPC getAccountInfo;
//  2. enrichment: Dexscreener pair data (name, liquidity, price) when it
//     already exists. Right after a launch Dexscreener may still be empty,
//     so "no pairs yet" is NOT a validation failure.
// Also resolves Dexscreener/Gecko *pair* addresses to the underlying mint.

const TOKEN_PROGRAM = 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA';
const TOKEN_2022_PROGRAM = 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb';

export class CaValidator {
  /**
   * @param {{ rpcUrl: string, fetchImpl?: typeof fetch, logger?: any }} opts
   */
  constructor({ rpcUrl, fetchImpl = fetch, logger }) {
    this.rpcUrl = rpcUrl;
    this.fetch = fetchImpl;
    this.logger = logger;
  }

  async #rpc(method, params) {
    const res = await this.fetch(this.rpcUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
      signal: AbortSignal.timeout(8_000),
    });
    if (!res.ok) throw new Error(`RPC HTTP ${res.status}`);
    const body = await res.json();
    if (body.error) throw new Error(`RPC error: ${body.error.message}`);
    return body.result;
  }

  /**
   * @param {string} address
   * @returns {Promise<{ exists: boolean, isMint: boolean, program?: string, supply?: string, decimals?: number }>}
   */
  async checkOnChain(address) {
    const result = await this.#rpc('getAccountInfo', [
      address,
      { encoding: 'jsonParsed', commitment: 'processed' },
    ]);
    const account = result?.value;
    if (!account) return { exists: false, isMint: false };

    const owner = account.owner;
    const parsed = account.data?.parsed;
    const isMint =
      (owner === TOKEN_PROGRAM || owner === TOKEN_2022_PROGRAM) &&
      parsed?.type === 'mint';
    return {
      exists: true,
      isMint,
      program: owner,
      supply: parsed?.info?.supply,
      decimals: parsed?.info?.decimals,
    };
  }

  /**
   * @param {string} address token mint
   * @returns {Promise<{ pairs: Array<object> }>} best pairs first (by liquidity)
   */
  async dexscreenerToken(address) {
    const res = await this.fetch(
      `https://api.dexscreener.com/latest/dex/tokens/${encodeURIComponent(address)}`,
      { signal: AbortSignal.timeout(8_000) },
    );
    if (!res.ok) throw new Error(`Dexscreener HTTP ${res.status}`);
    const body = await res.json();
    const pairs = (body.pairs ?? [])
      .filter((p) => p.chainId === 'solana')
      .sort((a, b) => (b.liquidity?.usd ?? 0) - (a.liquidity?.usd ?? 0));
    return { pairs };
  }

  /**
   * Dexscreener/Gecko links often point at the *pair* address, not the token.
   * Resolve it to the base token mint; returns null if unknown to Dexscreener.
   * @param {string} pairAddress
   */
  async resolvePairToToken(pairAddress) {
    const res = await this.fetch(
      `https://api.dexscreener.com/latest/dex/pairs/solana/${encodeURIComponent(pairAddress)}`,
      { signal: AbortSignal.timeout(8_000) },
    );
    if (!res.ok) throw new Error(`Dexscreener HTTP ${res.status}`);
    const body = await res.json();
    return body.pairs?.[0]?.baseToken?.address ?? null;
  }

  /**
   * Full validation used by the pipeline.
   * @param {string} address
   * @param {{ maybePair?: boolean, enrich?: boolean }} [opts]
   * @returns {Promise<{
   *   address: string, valid: boolean, reason?: string,
   *   onChain?: object, dex?: { name?: string, symbol?: string, priceUsd?: string, liquidityUsd?: number, url?: string } | null,
   * }>}
   */
  async validate(address, { maybePair = false, enrich = true } = {}) {
    let resolved = address;

    if (maybePair) {
      try {
        const token = await this.resolvePairToToken(address);
        if (token) resolved = token;
      } catch (err) {
        this.logger?.warn('pair resolution failed, treating as token address', {
          address,
          error: err.message,
        });
      }
    }

    let onChain;
    try {
      onChain = await this.checkOnChain(resolved);
    } catch (err) {
      return { address: resolved, valid: false, reason: `rpc_error: ${err.message}` };
    }
    if (!onChain.exists) return { address: resolved, valid: false, reason: 'not_found_on_chain', onChain };
    if (!onChain.isMint) return { address: resolved, valid: false, reason: 'not_a_token_mint', onChain };

    let dex = null;
    if (enrich) {
      try {
        const { pairs } = await this.dexscreenerToken(resolved);
        const best = pairs[0];
        if (best) {
          dex = {
            name: best.baseToken?.name,
            symbol: best.baseToken?.symbol,
            priceUsd: best.priceUsd,
            liquidityUsd: best.liquidity?.usd,
            url: best.url,
          };
        }
      } catch (err) {
        this.logger?.warn('dexscreener enrichment failed', { address: resolved, error: err.message });
      }
    }

    return { address: resolved, valid: true, onChain, dex };
  }
}
