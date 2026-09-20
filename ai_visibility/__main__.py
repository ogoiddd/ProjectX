"""Permite ``python -m ai_visibility <url>`` como atalho para a CLI."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
