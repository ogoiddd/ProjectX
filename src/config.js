import { readFileSync, existsSync } from 'node:fs';
import path from 'node:path';

// Minimal .env loader (KEY=VALUE lines, "#" comments). Values already present
// in process.env are never overridden, so real env wins over the file.
export function loadEnvFile(filePath = '.env', env = process.env) {
  if (!existsSync(filePath)) return;
  for (const rawLine of readFileSync(filePath, 'utf8').split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq <= 0) continue;
    const key = line.slice(0, eq).trim();
    let value = line.slice(eq + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!(key in env)) env[key] = value;
  }
}

export const DEFAULT_CONFIG = {
  monitor: {
    // "polling" (search/recent, works on Basic tier) or "stream" (filtered
    // stream, requires Pro tier).
    mode: 'polling',
    accounts: [],
    pollIntervalMs: 10_000,
    includeReplies: false,
    includeRetweets: false,
  },
  parser: {
    fetchExternalSites: true,
    maxExternalSitesPerPost: 3,
    siteFetchTimeoutMs: 5_000,
    maxSiteBytes: 1_500_000,
  },
  validation: {
    // Refuse to alert/execute on addresses that are not an on-chain SPL mint.
    requireOnChainMint: true,
    dexscreenerEnrich: true,
  },
  alerts: {
    telegram: true,
    discord: false,
  },
  executor: {
    // Both flags are intentionally conservative by default: execution off,
    // and even when enabled, paper trading unless explicitly disabled.
    enabled: false,
    paperTrading: true,
    buyAmountSol: 0.01,
    maxSolPerTrade: 0.05,
    maxSlippageBps: 300,
    priorityFeeLamports: 200_000,
    jupiterBaseUrl: 'https://lite-api.jup.ag/swap/v1',
    skipPreflight: false,
    killSwitchFile: 'KILL_SWITCH',
    tradesLogFile: 'data/trades.jsonl',
  },
  logLevel: 'info',
};

function deepMerge(base, override) {
  const out = { ...base };
  for (const [key, value] of Object.entries(override ?? {})) {
    if (
      value &&
      typeof value === 'object' &&
      !Array.isArray(value) &&
      typeof base[key] === 'object' &&
      base[key] !== null &&
      !Array.isArray(base[key])
    ) {
      out[key] = deepMerge(base[key], value);
    } else {
      out[key] = value;
    }
  }
  return out;
}

/**
 * Loads config.json + environment secrets and validates the combination.
 * Secrets live only in env; config.json holds tunables and must not contain keys.
 */
export function loadConfig({ configPath = 'config.json', env = process.env, cwd = process.cwd() } = {}) {
  const resolved = path.resolve(cwd, env.CONFIG_PATH || configPath);
  if (!existsSync(resolved)) {
    throw new Error(
      `config file not found at ${resolved} — copy config.example.json to config.json and edit it`,
    );
  }
  let parsed;
  try {
    parsed = JSON.parse(readFileSync(resolved, 'utf8'));
  } catch (err) {
    throw new Error(`config file ${resolved} is not valid JSON: ${err.message}`);
  }

  const config = deepMerge(DEFAULT_CONFIG, parsed);
  const errors = [];

  if (!Array.isArray(config.monitor.accounts) || config.monitor.accounts.length === 0) {
    errors.push('monitor.accounts must be a non-empty array of X usernames (without @)');
  }
  if (!['polling', 'stream'].includes(config.monitor.mode)) {
    errors.push(`monitor.mode must be "polling" or "stream", got "${config.monitor.mode}"`);
  }
  if (config.monitor.pollIntervalMs < 1_000) {
    errors.push('monitor.pollIntervalMs must be >= 1000 (sub-second polling only burns quota)');
  }
  if (!env.X_BEARER_TOKEN) {
    errors.push('X_BEARER_TOKEN missing from environment (.env)');
  }
  if (config.alerts.telegram && !(env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID)) {
    errors.push('alerts.telegram is on but TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID are missing');
  }
  if (config.alerts.discord && !env.DISCORD_WEBHOOK_URL) {
    errors.push('alerts.discord is on but DISCORD_WEBHOOK_URL is missing');
  }

  const ex = config.executor;
  if (ex.maxSolPerTrade <= 0) errors.push('executor.maxSolPerTrade must be > 0');
  if (ex.buyAmountSol <= 0) errors.push('executor.buyAmountSol must be > 0');
  if (ex.buyAmountSol > ex.maxSolPerTrade) {
    errors.push(
      `executor.buyAmountSol (${ex.buyAmountSol}) exceeds executor.maxSolPerTrade (${ex.maxSolPerTrade})`,
    );
  }
  if (!(ex.maxSlippageBps > 0 && ex.maxSlippageBps <= 10_000)) {
    errors.push('executor.maxSlippageBps must be in (0, 10000]');
  }
  if (ex.enabled && !ex.paperTrading && !env.BURNER_WALLET_PRIVATE_KEY) {
    errors.push(
      'executor is enabled in LIVE mode but BURNER_WALLET_PRIVATE_KEY is missing from environment',
    );
  }

  if (errors.length > 0) {
    throw new Error(`invalid configuration:\n  - ${errors.join('\n  - ')}`);
  }

  const secrets = {
    xBearerToken: env.X_BEARER_TOKEN,
    telegramBotToken: env.TELEGRAM_BOT_TOKEN,
    telegramChatId: env.TELEGRAM_CHAT_ID,
    discordWebhookUrl: env.DISCORD_WEBHOOK_URL,
    solanaRpcUrl: env.SOLANA_RPC_URL || 'https://api.mainnet-beta.solana.com',
    burnerWalletPrivateKey: env.BURNER_WALLET_PRIVATE_KEY,
  };

  return { config, secrets };
}
