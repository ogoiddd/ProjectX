#!/usr/bin/env node
// Entrypoint: wires config -> monitor -> pipeline and handles shutdown.

import { loadEnvFile, loadConfig } from './config.js';
import { createLogger } from './util/logger.js';
import { XApi } from './monitor/xApi.js';
import { Poller } from './monitor/poller.js';
import { StreamMonitor } from './monitor/stream.js';
import { CaValidator } from './validator/caValidator.js';
import { Notifier } from './alerts/notifier.js';
import { Executor } from './executor/executor.js';
import { Pipeline } from './pipeline.js';

async function main() {
  loadEnvFile();
  const { config, secrets } = loadConfig();
  const logger = createLogger({ level: process.env.LOG_LEVEL || config.logLevel });

  logger.info('starting solana token monitor', {
    mode: config.monitor.mode,
    accounts: config.monitor.accounts,
    executorEnabled: config.executor.enabled,
    paperTrading: config.executor.paperTrading,
  });
  if (config.executor.enabled && !config.executor.paperTrading) {
    logger.warn('LIVE TRADING IS ENABLED — real funds at risk', {
      maxSolPerTrade: config.executor.maxSolPerTrade,
      buyAmountSol: config.executor.buyAmountSol,
      killSwitchFile: config.executor.killSwitchFile,
    });
  }

  const xApi = new XApi({ bearerToken: secrets.xBearerToken, logger: logger.child('x-api') });
  const validator = new CaValidator({ rpcUrl: secrets.solanaRpcUrl, logger: logger.child('validator') });
  const notifier = new Notifier({
    telegram: config.alerts.telegram
      ? { botToken: secrets.telegramBotToken, chatId: secrets.telegramChatId }
      : null,
    discord: config.alerts.discord ? { webhookUrl: secrets.discordWebhookUrl } : null,
    logger: logger.child('alerts'),
  });
  const executor = new Executor({
    config: config.executor,
    rpcUrl: secrets.solanaRpcUrl,
    logger: logger.child('executor'),
  });
  const pipeline = new Pipeline({
    config,
    validator,
    notifier,
    executor,
    logger: logger.child('pipeline'),
  });

  const onTweet = (tweet, ctx) =>
    pipeline
      .handleTweet(tweet, ctx)
      .catch((err) => logger.error('pipeline error', { tweetId: tweet.id, error: err.message }));

  const monitorOpts = {
    xApi,
    accounts: config.monitor.accounts,
    includeReplies: config.monitor.includeReplies,
    includeRetweets: config.monitor.includeRetweets,
    onTweet,
  };
  const monitor =
    config.monitor.mode === 'stream'
      ? new StreamMonitor({ ...monitorOpts, logger: logger.child('stream') })
      : new Poller({
          ...monitorOpts,
          pollIntervalMs: config.monitor.pollIntervalMs,
          logger: logger.child('poller'),
        });

  const shutdown = (signal) => {
    logger.info('shutting down', { signal });
    monitor.stop();
    // Give in-flight work a moment, then exit.
    setTimeout(() => process.exit(0), 2_000).unref();
  };
  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));

  await monitor.run();
}

main().catch((err) => {
  console.error(`fatal: ${err.message}`);
  process.exit(1);
});
