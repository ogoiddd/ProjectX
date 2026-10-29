"""Pedidos HTTP com novas tentativas em 429/5xx."""

from __future__ import annotations

import time
from typing import Any

import requests

TENTATIVAS = 4
PAUSA_BASE = 2.0  # segundos; duplica a cada tentativa


class ErroApi(RuntimeError):
    def __init__(self, servico: str, estado: int, corpo: str):
        super().__init__(f"{servico}: HTTP {estado}: {corpo[:300]}")
        self.estado = estado


def pedido(servico: str, metodo: str, url: str, *, sessao: requests.Session | None = None,
           timeout: float = 60, **kwargs: Any) -> Any:
    """Faz o pedido e devolve o JSON. Repete em 429 e 5xx com backoff."""
    s = sessao or requests
    for tentativa in range(TENTATIVAS):
        r = s.request(metodo, url, timeout=timeout, **kwargs)
        if r.status_code == 429 or r.status_code >= 500:
            if tentativa < TENTATIVAS - 1:
                time.sleep(PAUSA_BASE * 2 ** tentativa)
                continue
        if not r.ok:
            raise ErroApi(servico, r.status_code, r.text)
        return r.json() if r.content else None
    raise ErroApi(servico, r.status_code, r.text)
