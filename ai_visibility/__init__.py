"""Auditoria de visibilidade em AI (ChatGPT/Perplexity/etc.) para negócios locais.

Ideia: dado o URL de um negócio, corre um conjunto de queries realistas de
comprador contra um LLM (ex.: OpenAI ChatGPT) e verifica se o negócio aparece
nas respostas. Devolve um *score* /100, um relatório HTML/PDF pronto a enviar
por email como *lead magnet* e uma *directory page* SEO/GEO otimizada para AI
que pode ser vendida como serviço recorrente.

Módulos
-------
- :mod:`ai_visibility.fetch`     — obtém e analisa o site do negócio.
- :mod:`ai_visibility.queries`   — gera queries de comprador a testar.
- :mod:`ai_visibility.llm_check` — corre as queries no LLM (com modo mock).
- :mod:`ai_visibility.score`     — cálculo do Score /100.
- :mod:`ai_visibility.audit`     — orquestra a auditoria completa.
- :mod:`ai_visibility.report`    — relatório HTML imprimível.
- :mod:`ai_visibility.directory` — página *directory* AI-friendly.
- :mod:`ai_visibility.cli`       — interface de linha de comandos.
- :mod:`ai_visibility.web`       — web app (stdlib) para uso em qualquer sítio.

Só usa a biblioteca-padrão do Python + ``requests`` — sem dependências pesadas.
"""

from .audit import AuditResult, run_audit
from .fetch import BusinessProfile, fetch_business
from .score import ScoreBreakdown, compute_score

__all__ = [
    "AuditResult",
    "BusinessProfile",
    "ScoreBreakdown",
    "compute_score",
    "fetch_business",
    "run_audit",
]

__version__ = "0.1.0"
