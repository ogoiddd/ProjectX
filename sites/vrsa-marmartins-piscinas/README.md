# Mar Martins, Vila Real de Santo António: demo do site

Site de uma página para a **Marmartins, Lda** (marca "Mar Martins"), construção de piscinas em Vila Real de Santo António. Ainda não está publicado. Ver também `BRIEF.md` (factos e referências BYQ).

- `public/`: o site estático, sem build (`index.html`, `privacidade.html`, `404.html`, `styles.css`, `app.js`, `fonts/`, `assets/`, `vercel.json`, `robots.txt`, `sitemap.xml`, `site.webmanifest`).
- `tools/qa/shots.mjs`: screenshots desktop e mobile (primeiro ecrã, página inteira, simulador e orçamento preenchido) para `qa/`. Servir antes com `python3 -m http.server 8612` dentro de `public/`.

## Conceito

1. Água do Guadiana sobre pedra calcária: a piscina é o produto, por isso o herói é um corte técnico desenhado (betão armado, revestimento, bordadura) com a água a ondular, e as cotas acompanham o simulador.
2. Estrutura editorial e calma (ref. BYQ "Reforma": serif leve com itálico no título, labels em mono, nav em pílula, profundidade por cor e não por sombra), com a paleta tirada da obra: cal, pedra, areia e água.
3. O site faz a primeira conversa: o simulador calcula volume, litros, espelho de água, bordadura e revestimento, e passa as medidas para o pedido de orçamento, que vira mensagem de WhatsApp ou email.

## Elementos para mostrar na chamada

1. **Simulador**: o dono mexe nas medidas e vê o volume em m³ e litros a mudar e a planta à escala.
2. **Antes e depois**: a linha arrastável. Explicar que, com as fotos das obras dele, este quadro fica com obras reais.
3. **Pedido de orçamento**: "Usar estas medidas no orçamento" preenche o pedido; o cliente final manda tudo por WhatsApp de uma vez.

## Factos usados e fontes

| Facto | Fonte |
|---|---|
| Firma Marmartins, Lda, sociedade por quotas, NIPC 513526269, constituída a 29-04-2015, sede em Vila Real de Santo António | Racius, https://www.racius.com/marmartins-lda/ (consultado a 11 out. 2026) |
| Ligação ao negócio de piscinas (empresa relacionada "Vítor Manuel Martins - Construção de Piscinas, Unipessoal Lda", NIPC 508763517) e confirmação de que "Mar Martins" é a Marmartins | Racius e confirmação do utilizador a 11 out. 2026 |
| RAL: CIMAAL, Centro de Arbitragem de Conflitos de Consumo do Algarve, 289 823 135 | igual a `sites/faro-arealauto-oficina` (consumoalgarve.pt) |

## Por confirmar com o cliente (`[CONFIRMAR]` no site)

- Morada completa, telefone, email e número de WhatsApp. Quando houver, preencher `CONTACT` no início de `public/app.js`; até lá o formulário mostra a mensagem mas não a envia.
- Lista de serviços, fases do processo, zona servida e número de obras.
- Fotografias de obras reais, para substituir a planta desenhada do antes e depois.
- Texto da política de privacidade, prazo de conservação e alojamento final.
- Domínio (`marmartins.pt` é um placeholder nos canonical/OG/sitemap) e imagem OG (`/assets/og.png` ainda não existe).

## Notas sobre o simulador

As contas são geometria simples: volume = comprimento × largura × (rasa + funda) / 2; revestimento = fundo inclinado + topos + laterais. Não dá preços.

## Licenças

| Recurso | Licença |
|---|---|
| Newsreader (Production Type) | SIL Open Font License 1.1, via @fontsource |
| Hanken Grotesk (Alfredo Marco Pradil) | SIL Open Font License 1.1, via @fontsource |
| JetBrains Mono | SIL Open Font License 1.1, via @fontsource |
| Desenhos SVG, favicon | desenho próprio para este site |
