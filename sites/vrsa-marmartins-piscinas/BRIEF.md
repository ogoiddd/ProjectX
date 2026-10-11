# Brief — Mar Martins (piscinas) · Vila Real de Santo António

Brief para o `frontend-designer`. Junta (1) factos verificados do negócio e (2) direção de design tirada dos design systems públicos do BYQ Supply (plano Free: só pré-visualização, sem download dos `DESIGN.md`).

## 1. Factos do negócio

| Facto | Valor | Fonte | Estado |
|---|---|---|---|
| Firma | Marmartins, Lda (sociedade por quotas) | racius.com/marmartins-lda | verificado |
| NIF | 513526269 | Racius | verificado |
| Constituição | 29/04/2015 | Racius | verificado |
| Sede | Vila Real de Santo António | Racius | morada exata `[CONFIRMAR COM CLIENTE]` |
| Capital social | 2 000 € | Racius | verificado (não usar no site) |
| Atividade registada | CAE "Construção de edifícios" | Racius | verificado |
| Empresa ligada | Vítor Manuel Martins – Construção de Piscinas, Unipessoal Lda (NIF 508763517) | Racius ("empresas relacionadas") | relação exata `[CONFIRMAR COM CLIENTE]` |
| "Mar Martins" = Marmartins? | Provável (nome + piscinas + Algarve) | inferência | `[CONFIRMAR COM CLIENTE]` |
| Website / redes / Google Maps | Nada encontrado | pesquisas web | presença online inexistente → bom lead |
| Serviços, anos de experiência, telefone, fotos de obras, reviews | — | — | tudo `[CONFIRMAR COM CLIENTE]` |

Nunca inventar serviços, preços, nº de piscinas feitas ou testemunhos. Pedir ao cliente: 10–20 fotos de obras (antes/depois), lista de serviços, zona servida (VRSA, Castro Marim, Tavira, Monte Gordo…), contactos e WhatsApp.

## 2. Referências BYQ analisadas

| Design system | Porque serve | O que tirar |
|---|---|---|
| **Reforma** (base principal) | Negócio estabelecido que deve *transmitir confiança sem exagerar* | Fundo claro quente, serif editorial leve (peso 300) + sans neutra, palavra em itálico no título do hero, labels em mono maiúsculas, nav em pílula fixa, secções com padding 80/120/160px, profundidade dada por cor de fundo e não por sombras, raio 20px nos cards e 32px nos botões |
| **Vluna** (secundário) | Arquitetura em que a fotografia carrega a emoção | Fotografia full-bleed sem cortes apertados, UI monocromática + 1 acento, linhas finas por opacidade, wordmark serif gigante no rodapé |
| **Sparkles** (padrões de serviço) | Template de empresa de serviços ao domicílio | Fluxo de pedido em painel dividido (formulário à esquerda, cara/foto real à direita), FAQ em acordeão, marquee de serviços |
| LunaArc | Mesma família da Vluna, escuro e cinematográfico | Só como alternativa se o cliente quiser registo "luxo noturno" |

## 3. Direção proposta (adaptada, não copiada)

**Conceito (3 linhas):**
1. Água do Algarve sobre pedra calcária: a piscina é o produto, a fotografia da obra é o herói.
2. Editorial e calmo como a Reforma, mas com a paleta tirada da obra real: azul da água, pedra, areia, cal.
3. Conversão local acima de tudo: pedir orçamento e WhatsApp visíveis no primeiro ecrã em mobile.

**Tokens iniciais (substituir quando houver fotos/logótipo reais):**

| Token | Hex | Papel (equivalente Reforma) |
|---|---|---|
| canvas | `#F6F4EF` (cal) | Antique Linen — fundo da página |
| surface | `#FFFFFF` | Lifted White — nav e cards |
| inset | `#E6E2DA` (pedra calcária) | Pale Stone — inputs |
| ink | `#0E2A33` (azul-petróleo profundo) | Deep Burgundy — texto e botões |
| accent | `#1F7A8C` (água) | Ink Pool — links, ícones, focus |
| wash-1 | `#DCEBEE` (água rasa) | Morning Sky |
| wash-2 | `#F2E8D8` (areia) | Candlelit Cream |
| ok / erro | `#4F9D69` / `#C65D4F` | Estados |

Verificar contraste AA de `accent` sobre `canvas` antes de usar em texto pequeno.

**Tipografia:** serif editorial leve para títulos (ex.: Fraunces ou Newsreader a 300, auto-alojadas), sans humanista para texto (ex.: Hanken Grotesk), mono para labels (ex.: JetBrains Mono a 500, maiúsculas). Evitar Inter/Poppins (regra anti "AI look").

**Estrutura de página:**
1. Nav em pílula: logótipo · Serviços · Obras · Processo · Contactos · botão "Pedir orçamento".
2. Hero: título serif com uma palavra em itálico (ex.: "Piscinas construídas *para durar*" `[CONFIRMAR COPY]`), foto real de obra full-bleed com cantos de 20px, CTA de telefone e WhatsApp.
3. Obras: galeria antes/depois com slider tátil (é este o elemento a mostrar na chamada).
4. Processo em 4 passos com tabs (padrão "How It Works Tabbed" da Reforma): visita → projeto → construção → manutenção `[CONFIRMAR]`.
5. Serviços em lista empilhada (cards largos com imagem + texto, não 3 colunas iguais).
6. Zona servida: mapa desenhado do Sotavento algarvio.
7. Pedido de orçamento em painel dividido (padrão Sparkles): tipo de piscina, dimensões aproximadas, localidade, fotos do terreno.
8. FAQ em acordeão (licenciamento, prazos, época ideal para construir).
9. Rodapé com wordmark "Mar Martins" em serif gigante (gesto da Vluna), NIF, Livro de Reclamações.

**Movimento:** entrada das secções com translateY(50px)→0 e opacidade 0→1 (Reforma), sempre com `prefers-reduced-motion`.

## 4. Limites desta análise
- Plano Free do BYQ: os `DESIGN.md` / `tokens.json` estão bloqueados; os valores acima vêm das páginas públicas de pré-visualização (cores, tipos, espaçamentos, do's & don'ts).
- Não foi possível confirmar a presença online da empresa (sem site, sem redes encontradas).
