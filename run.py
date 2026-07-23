#!/usr/bin/env python3
"""Ponto de entrada do bot de copytrading da Polymarket.

Uso:
    python run.py            # corre o bot (respeita DRY_RUN do .env)
    python run.py --check    # valida config e conectividade, depois sai
"""

import sys

from copybot.bot import CopyBot
from copybot.config import Config, ConfigError
from copybot.logger import get_logger

log = get_logger("run")


def check(cfg: Config) -> int:
    """Valida config + testa a Data API. Não envia ordens."""
    from copybot.data_api import DataAPI

    log.info("%s", cfg.summary())
    data = DataAPI(cfg.data_api_host)
    ok = True
    for wallet in cfg.target_wallets:
        trades = data.get_user_trades(wallet, limit=5)
        if trades:
            log.info("Alvo %s: %d trades recentes lidos com sucesso.", wallet, len(trades))
            log.info("   Último: %s", trades[-1].describe())
        else:
            log.warning("Alvo %s: sem trades lidos (carteira errada ou sem atividade?).", wallet)
            ok = False

    if not cfg.dry_run:
        log.info("A testar autenticação CLOB…")
        try:
            CopyBot(cfg).executor.preflight()
            log.info("Autenticação CLOB OK.")
        except Exception as exc:  # noqa: BLE001
            log.error("Falha na autenticação CLOB: %s", exc)
            ok = False

    log.info("Verificação %s.", "OK" if ok else "com avisos")
    return 0 if ok else 1


def main() -> int:
    try:
        cfg = Config.from_env()
    except ConfigError as exc:
        log.error("Configuração inválida: %s", exc)
        log.error("Copia .env.example para .env e preenche os valores.")
        return 2

    if "--check" in sys.argv:
        return check(cfg)

    try:
        CopyBot(cfg).run()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
