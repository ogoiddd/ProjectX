"""Pipeline de leads da Zarpa: clínicas em Portugal para cold email.

Etapas (cada uma lê e reescreve ``vendas/email/campanhas/<id>/leads.json``):

1. **recolher**: Google Maps (Outscraper), AI Ark e CSVs exportados de
   outras ferramentas (Get Leads, ...).
2. **juntar**: normaliza e junta os duplicados das várias fontes.
3. **verificar**: emails no MillionVerifier e telefones pelo formato.
4. **filtrar**: regras legais (só sociedades, lista de oposição, supressão).
5. **auditar**: visita o site de cada lead e recolhe evidências para o
   icebreaker (que é escrito pelo agente ``icebreaker-writer``).
6. **exportar / enviar**: ``envio.csv`` e envio para o Smartlead.
7. **sincronizar / funil**: resultados do Smartlead e métricas.

As chaves das APIs vêm sempre de variáveis de ambiente, nunca do código.
"""

__version__ = "0.1.0"
