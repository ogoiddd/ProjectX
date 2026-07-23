"""Persistência de estado: deduplicação de trades e controlo de gasto diário.

Guardado num ficheiro JSON simples para sobreviver a reinícios.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Set

from .logger import get_logger

log = get_logger("state")


class State:
    def __init__(self, path: str):
        self.path = path
        self.seen_keys: Set[str] = set()
        self.bootstrapped: bool = False
        self.spend_date: str = self._today()
        self.spent_today: float = 0.0
        self._load()

    @staticmethod
    def _today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _load(self) -> None:
        if not os.path.exists(self.path):
            log.info("Sem estado prévio — a começar do zero (%s)", self.path)
            return
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.seen_keys = set(data.get("seen_keys", []))
            self.bootstrapped = bool(data.get("bootstrapped", False))
            self.spend_date = data.get("spend_date", self._today())
            self.spent_today = float(data.get("spent_today", 0.0))
            log.info(
                "Estado carregado: %d trades vistos, gasto hoje=%.2f USDC",
                len(self.seen_keys),
                self.spent_today if self.spend_date == self._today() else 0.0,
            )
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            log.warning("Não foi possível ler o estado (%s): a recomeçar", exc)

    def save(self) -> None:
        # Mantém o ficheiro pequeno: guarda no máximo os últimos 5000 keys.
        keys = list(self.seen_keys)
        if len(keys) > 5000:
            keys = keys[-5000:]
            self.seen_keys = set(keys)
        data = {
            "seen_keys": keys,
            "bootstrapped": self.bootstrapped,
            "spend_date": self.spend_date,
            "spent_today": self.spent_today,
        }
        tmp = f"{self.path}.tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            os.replace(tmp, self.path)
        except OSError as exc:  # pragma: no cover
            log.error("Falha ao guardar estado: %s", exc)

    # ---- deduplicação -----------------------------------------------------

    def has_seen(self, key: str) -> bool:
        return key in self.seen_keys

    def mark_seen(self, key: str) -> None:
        self.seen_keys.add(key)

    # ---- gasto diário -----------------------------------------------------

    def _roll_day_if_needed(self) -> None:
        today = self._today()
        if today != self.spend_date:
            log.info("Novo dia (%s) — a repor contador de gasto diário", today)
            self.spend_date = today
            self.spent_today = 0.0

    def remaining_daily_budget(self, max_daily: float) -> float:
        """USDC ainda disponível hoje. Retorna infinito se max_daily <= 0."""
        self._roll_day_if_needed()
        if max_daily <= 0:
            return float("inf")
        return max(0.0, max_daily - self.spent_today)

    def record_spend(self, amount: float) -> None:
        self._roll_day_if_needed()
        self.spent_today += amount
