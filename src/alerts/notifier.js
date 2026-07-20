// Instant notifications: Telegram bot (primary) and Discord webhook
// (optional). Both are fired in parallel; alert latency is logged.

const esc = (s) =>
  String(s ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

export class Notifier {
  /**
   * @param {{
   *   telegram?: { botToken: string, chatId: string } | null,
   *   discord?: { webhookUrl: string } | null,
   *   fetchImpl?: typeof fetch,
   *   logger?: any,
   * }} opts
   */
  constructor({ telegram = null, discord = null, fetchImpl = fetch, logger }) {
    this.telegram = telegram;
    this.discord = discord;
    this.fetch = fetchImpl;
    this.logger = logger;
  }

  /**
   * @param {{
   *   username: string, tweetId: string, address: string, source: string,
   *   sourceUrl?: string, detectionLatencyMs: number, validation: object,
   * }} alert
   */
  async sendTokenAlert(alert) {
    const startedAt = Date.now();
    const postUrl = `https://x.com/${alert.username}/status/${alert.tweetId}`;
    const dex = alert.validation?.dex;

    const lines = [
      `🚨 <b>Token Solana detectado</b>`,
      `Conta: @${esc(alert.username)}`,
      `CA: <code>${esc(alert.address)}</code>`,
      `Fonte: ${esc(alert.source)}${alert.sourceUrl ? ` (${esc(alert.sourceUrl)})` : ''}`,
      dex
        ? `Token: ${esc(dex.name)} (${esc(dex.symbol)}) — liq $${Math.round(dex.liquidityUsd ?? 0).toLocaleString('en-US')}`
        : `Dexscreener: sem pares ainda (possível lançamento recém-saído)`,
      `Validação on-chain: ${alert.validation?.valid ? '✅ mint existe' : `❌ ${esc(alert.validation?.reason)}`}`,
      `Post: ${esc(postUrl)}`,
      `Latência de detecção: ${alert.detectionLatencyMs}ms`,
      `Links: https://dexscreener.com/solana/${esc(alert.address)} | https://pump.fun/coin/${esc(alert.address)} | https://solscan.io/token/${esc(alert.address)}`,
    ];
    const html = lines.join('\n');
    const plain = html.replaceAll(/<\/?[a-z]+>/g, '');

    const tasks = [];
    if (this.telegram) tasks.push(this.#sendTelegram(html));
    if (this.discord) tasks.push(this.#sendDiscord(plain));
    const results = await Promise.allSettled(tasks);

    const alertLatencyMs = Date.now() - startedAt;
    for (const r of results) {
      if (r.status === 'rejected') {
        this.logger?.error('alert delivery failed', { error: r.reason?.message });
      }
    }
    this.logger?.info('alert dispatched', {
      address: alert.address,
      detectionLatencyMs: alert.detectionLatencyMs,
      alertLatencyMs,
      totalLatencyMs: alert.detectionLatencyMs + alertLatencyMs,
    });
    return { alertLatencyMs };
  }

  /** Free-form operational message (e.g. trade executed, kill switch hit). */
  async sendText(text) {
    const tasks = [];
    if (this.telegram) tasks.push(this.#sendTelegram(esc(text)));
    if (this.discord) tasks.push(this.#sendDiscord(text));
    const results = await Promise.allSettled(tasks);
    for (const r of results) {
      if (r.status === 'rejected') {
        this.logger?.error('alert delivery failed', { error: r.reason?.message });
      }
    }
  }

  async #sendTelegram(html) {
    const res = await this.fetch(
      `https://api.telegram.org/bot${this.telegram.botToken}/sendMessage`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          chat_id: this.telegram.chatId,
          text: html,
          parse_mode: 'HTML',
          disable_web_page_preview: true,
        }),
        signal: AbortSignal.timeout(8_000),
      },
    );
    if (!res.ok) {
      const body = await res.text().catch(() => '');
      throw new Error(`telegram ${res.status}: ${body.slice(0, 300)}`);
    }
  }

  async #sendDiscord(content) {
    const res = await this.fetch(this.discord.webhookUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ content: content.slice(0, 1_900) }),
      signal: AbortSignal.timeout(8_000),
    });
    if (!res.ok && res.status !== 204) {
      const body = await res.text().catch(() => '');
      throw new Error(`discord ${res.status}: ${body.slice(0, 300)}`);
    }
  }
}
