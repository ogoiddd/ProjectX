# Faro — relatório da operação

Data: 2026-10-09 · Cabecilha

## Resumo

- **18 negócios** encontrados sem site (ou só com Facebook / plataforma / site morto) → 16 com pontuação ≥ 50 → **4 escolhidos**.
- **4 demos** construídas, revistas a nível legal/segurança e testadas em browser, em `sites/faro-*/`.
- **4 guiões** de chamada em `vendas/faro/guioes/`.
- **Valor em cima da mesa:** 1000 + 1000 + 1000 + 1500 = **4500€** (+ manutenção opcional 30–50€/mês por cliente).
- **Nenhum decisor confirmado pelo nome** (Racius bloqueado, Facebook pede login). Há duas pistas por confirmar na chamada: Diogo Ferreira (Cantinho, MAGG 2021) e Orlando Rosa (Cidade Velha, NiT 2020).

## Os 4 escolhidos

| # | Negócio | Setor | Decisor (confiança) | Quando ligar | Demo | Guião | Preço |
|---|---|---|---|---|---|---|---|
| 1 | **Arealauto** — 289 882 080 | Oficina multimarca desde 1996, 11–15 pessoas | gerente, nome desconhecido (baixa) | ter–qui 10:00–11:30 ou 14:30–16:30 | `sites/faro-arealauto-oficina` | `guioes/faro-arealauto-oficina.md` | **1000€** |
| 2 | **Cidade Velha** — 289 827 145 | Restaurante junto à Sé, 4,4 ★ / ~1496 | pista: Orlando Rosa (baixa) | ter–qui 15:30–17:30 | `sites/faro-restaurante-cidade-velha` (PT/EN/FR/DE) | `guioes/faro-restaurante-cidade-velha.md` | **1500€** (ou 1000€ só PT/EN) |
| 3 | **Cantinho** — 911 013 101 | Restaurante, Arco do Repouso, 4,5 ★ / 1327 | pista: Diogo Ferreira (baixa) | ter–qui 15:30–17:30 | `sites/faro-restaurante-cantinho` (PT/EN) | `guioes/faro-restaurante-cantinho.md` | **1000€** |
| 4 | **Taberna Zé-Zé** — 938 735 167 | Taberna de cataplanas, 4,7 ★ / ~963 | responsável, nome desconhecido (baixa) | ter–qui 16:00–17:30 | `sites/faro-taberna-ze-ze` (PT/EN) | `guioes/faro-taberna-ze-ze.md` | **1000€** |

Porquê estes:
1. **Arealauto** — ticket B2B mais sólido: sociedade com 30 anos e equipa, ficha Google sem fotos nem site, parece ter saído da rede TOPCAR (motivo para ter marca própria).
2. **Cidade Velha** — mais avaliações da lista, público turista, site antigo morto e 4 horários contraditórios online. Justifica o pacote multilíngue.
3. **Cantinho** — 1327 avaliações a depender de um Facebook que pede login; concorrentes diretos (O Coreto, Decanter) já têm site.
4. **Taberna Zé-Zé** — casa pequena que enche, sem forma de pedir mesa online, e uma página automática da Makro que contradiz o Google.

## Ordem de chamadas recomendada

1. **Arealauto** de manhã (10:00–11:30) — o lead mais "empresa", e o único com janela de manhã.
2. **Cidade Velha** ~15:30 — o maior ticket; ligar cedo na janela da tarde.
3. **Cantinho** ~16:15.
4. **Taberna Zé-Zé** ~17:00 — perto da abertura do jantar; o 938 pode ser telemóvel pessoal do dono, por isso chamada curta.

Terça a quinta. Se alguém pedir para não ser contactado, termina e marca `nao_contactar`. Não se liga para outros números da casa para contornar uma recusa.

## Antes de ligar (precisa da tua aprovação)

- [ ] **Publicar as 4 demos como pré-visualizações privadas** (ex.: Vercel com `noindex`) e substituir `[LINK DA DEMO]` em cada guião. Os guiões dependem disso: o gancho é mandar o link por WhatsApp durante a chamada.
- [ ] **Nome do vendedor:** os guiões da Arealauto, Cantinho e Zé-Zé (e `decisores.json`) dizem "Diogo"; o da Cidade Velha usa `[O TEU NOME]`. Confirmar e uniformizar.
- [ ] **Cidade Velha:** aprovar ou apagar a saída "só PT/EN por 1000€" para a objeção do preço.
- [ ] Atualizar o número de avaliações Google no dia (Cidade Velha e Zé-Zé já subiram).

## O que perguntar na chamada (bloqueia a entrega, não a demo)

Comum a todos: **denominação social + NIF** (DL 7/2004 e RGPD), **horário real**, **se o número tem WhatsApp**, email, fotos, domínio, entidade RAL a que aderiram.

| Negócio | Específico |
|---|---|
| Arealauto | lista real de serviços (só "multimarca" confirmado), equipa, autorização para usar o selo Ocidental, se ainda é TOPCAR (pergunta com tato) |
| Cidade Velha | ano de abertura (1982 vs ~1990), relação com o Cidade Velha Rooftop / 916 008 548, email de reservas (o botão "email" da demo ainda não tem destinatário), autorização para citar a NiT com o nome do Orlando Rosa, carta e preços |
| Cantinho | horário (Google 10:30–23:30 vs MAGG 12–22), email ainda ativo, autorização para citar a MAGG |
| Zé-Zé | horário (Google só jantar vs Makro almoço+jantar até 01:00), qual telefone é o oficial, preços |

## Qualidade e conformidade

- Todas as demos: estáticas, sem cookies nem terceiros a carregar, CSP estrita, política de privacidade, aviso RGPD nos formulários, Livro de Reclamações, RAL (CIMAAL), alergénios nos restaurantes, fallback sem JavaScript, 404, sitemap/hreflang. Lighthouse 98–100 onde foi medido.
- Nenhuma foto de terceiros: molduras `[FOTO DO CLIENTE]`. Factos com fonte no `README.md` de cada demo; o que não foi confirmado está marcado `[CONFIRMAR COM CLIENTE]`.
- Detalhe legal de cada uma em `sites/<lead>/LEGAL.md`.

## Próximos leads (reserva)

Se algum dos 4 disser que não: **Vó Bela** (4,9 ★, sem site nem redes, ter–sáb 15:00–17:30), **Cantinho da Ronha** (877 avaliações, só TripAdvisor), **Local by Góis** (5,0 ★, só Instagram, gama alta).
Retirados ou em espera: Escola de Condução da Penha (tem site, desatualizado — redesenho), Tasquinha Cruzeiro (dono faleceu em 2021, gerência desconhecida), Velha Casa (possivelmente fechou), Clínica do Alportel (gerência mudou em 08/2025).

## Riscos

- **Restaurantes = ticket mais difícil** de fechar a 1000€+ do que clínicas ou oficinas, e é fim de época. Faro tem poucos leads de setores de ticket alto sem site; numa próxima cidade, pedir ao business-finder mais clínicas, construção e alojamento.
- **Decisores por nome:** ficam por descobrir na chamada. Uma certidão permanente (paga) daria os gerentes de cada sociedade.
