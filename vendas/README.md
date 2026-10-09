# Vendas de websites

Operação para vender websites (≥1000€) a negócios locais sem site.

```
/cabecilha Faro          # dentro do Claude Code
claude --agent cabecilha # ou como agente principal, e depois dizer a cidade
```

| Agente | Ficheiro | Produz |
|---|---|---|
| Cabecilha | `.claude/agents/cabecilha.md` | `vendas/<cidade>/relatorio.md` |
| No Website Business Finder | `.claude/agents/business-finder.md` | `vendas/<cidade>/leads.json` |
| Owner Finder | `.claude/agents/owner-finder.md` | `vendas/<cidade>/decisores.json` |
| Front-end Designer | `.claude/agents/frontend-designer.md` | `sites/<lead-id>/` (demo) |
| Back-end Maker | `.claude/agents/backend-maker.md` | `sites/<lead-id>/LEGAL.md` + correções |
| Cold Call Writer | `.claude/agents/cold-call-writer.md` | `vendas/<cidade>/guioes/<lead-id>.md` |

Os agentes preparam tudo; publicar demos, enviar mensagens e fazer chamadas fica sempre para aprovação humana.
