# Cantinho — Faro (demo)

Site de uma página para o **Cantinho** (R. do Repouso 6, 8000-169 Faro · +351 911 013 101), em PT (`/`) e EN (`/en/`). Lead: `faro-restaurante-cantinho` em `vendas/faro/leads.json`.

- `public/` é o site estático pronto a publicar (sem build): `index.html`, `en/index.html`, `styles.css`, `app.js`, `fonts/`, `assets/`, `vercel.json`, `robots.txt`, `sitemap.xml`, `site.webmanifest`.
- `tools/src/index.html` é o template bilingue (`{{ português || English }}`); `python3 tools/build.py` gera as duas páginas, desenha o arco do hero (SVG gerado, pedras determinísticas, seed 1249) e insere o mapa.
- `tools/map/osm2svg.py` desenha o mapa da Vila Adentro a partir de `tools/map/osm-vila-adentro.json` (© OpenStreetMap contributors, ODbL).
- `tools/og/shoot.mjs` gera `og.jpg` e os ícones PNG; `tools/qa/*.mjs` tiram screenshots e testam o formulário (Playwright, Chromium em `/opt/pw-browsers/chromium`).
- `qa/` contém os screenshots desktop/mobile usados na revisão.
- O domínio `https://cantinho-faro.vercel.app` em canonical/OG/sitemap é provisório: trocar quando houver domínio final.

## Conceito

1. O Cantinho fica à porta do Arco do Repouso, a entrada da muralha da Vila Adentro: o site é esse arco. Atravessa-se ao fazer scroll e fica-se do lado de dentro.
2. As cores vêm da pedra da muralha, da cal das paredes e da brasa da lareira. A tipografia é de inscrição (Gloock) com texto de ementa impressa (Newsreader). Não há azulejo nem quadro de giz, para não se confundir com a demo da Taberna Zé-Zé.
3. Copy na voz da casa ("Diz a lenda que o rei descansou aqui. Hoje, janta-se."), com os pratos e as frases dos clientes tal como foram escritos.

## Factos usados e fonte

| Facto | Onde aparece | Fonte |
|---|---|---|
| Morada R. do Repouso 6, 8000-169 Faro; telefone 911 013 101 | todo o site, JSON-LD | Ficha Google via Algarve Atlas, https://algarve-hub-frontend.onrender.com/restaurantes/cantinho-faro (consultado a 2026-10-09); `vendas/faro/leads.json` |
| Horário seg–sáb 10:30–23:30, domingo fechado | horário, "aberto agora", slots de reserva, JSON-LD | Algarve Atlas (ficha Google); coincide com Wanderlog e Rankeat. **A MAGG (2021) indicava 12:00–22:00 e allaboutportugal "todos os dias"**: confirmar |
| 4,5 no Google, 1327 avaliações | hero, secção Clientes | Algarve Atlas (2026-10-09). Atualizar na entrega |
| Avaliações citadas na íntegra (Adriana Carrilho, Caio Dias, Sílvia Barros, Joana Cavaco, Maria Daniela Plesca) | secção Clientes, ementa | Excertos das avaliações Google mostrados no Algarve Atlas. As traduções EN são nossas e estão assinaladas |
| Coordenadas 37.0134441, -7.9332883 | mapa, direções, JSON-LD | Nó OSM 4832258784 "Cantinho" (bate com a ficha: 37.01345, -7.93329) |
| Diogo Ferreira, "um dos responsáveis"; citação «O que tentámos foi traduzir e interpretar…» | secção Lá dentro | MAGG, 20-09-2021, https://magg.sapo.pt/comida/restaurantes/artigos/cantinho-em-faro-comida-tradicao |
| Peixe e marisco frescos da costa algarvia; decoração tradicional; esplanada; lareira acesa no inverno | Lá dentro | MAGG 2021 |
| Pratos: chouriça assada, camarão ao alhinho, pica-pau de marisco, amêijoas, polvo à algarvia, carré de borrego, arroz de marisco e cataplana de bacalhau (para dois, "especialidades da casa") | Ementa | MAGG 2021. **Os preços de 2021 não foram usados** |
| Lulas, folhado de perdiz, espetada de tamboril; "caré de borrego"; "o famoso banoffee" | Ementa | Avaliações Google (Caio Dias, Sílvia Barros, Adriana Carrilho) via Algarve Atlas |
| Instagram @cantinhodefaro; email geral.cantinho@gmail.com | rodapé | MAGG 2021 (email por confirmar) |
| Facebook facebook.com/cantinhodefaro | rodapé, JSON-LD | leads.json / ficha Google |
| Obras de jovens artistas algarvios nas paredes | Lá dentro (marcado) | allaboutportugal.pt/en/faro/restaurants/cantinho-de-faro (ficha antiga) |
| Arco do Repouso; lenda de D. Afonso III a descansar após tomar Faro em 1249 | hero ("Diz a lenda…") | euroveloportugal.com (Muralhas de Faro), thecollector.com (10 Must-See Historic Sites in Faro). Apresentado como lenda |
| Muralha classificada Imóvel de Interesse Público desde 1993 | Onde estamos | OSM relação 7013980 (Decreto 45/93; DGPC 74878) |
| Estacionamento à superfície no Largo de São Francisco | Onde estamos, mapa | OSM via 90463207 (amenity=parking, fee=no) |

Não foram usados nem preços, nem prémios, nem datas de fundação, nem fotografias de terceiros. A Rankeat foi consultada, mas o texto deles é gerado por IA, por isso não foi usado.

## [CONFIRMAR COM CLIENTE]

- Preços e ementa atual; prato do dia.
- Horário real (e horário da cozinha). A MAGG de 2021 tinha 12:00–22:00.
- Se o 911 013 101 tem WhatsApp. Se não tiver, o formulário fica só com SMS e chamada.
- Se o email geral.cantinho@gmail.com ainda está ativo.
- Se ainda há obras de artistas algarvios nas paredes, e quantos lugares tem a sala.
- Fotografias: 6 molduras `[FOTO DO CLIENTE]` (porta e arco, sala com lareira, arroz de marisco, polvo, esplanada, banoffee).
- Entidade legal, NIF e entidade RAL para o rodapé.
- O 965 391 296 (MAGG 2021, allaboutportugal) parece ser um número antigo. Não está no site.

## Detalhes técnicos

- O "aberto agora" é calculado na hora de Lisboa (Intl, `Europe/Lisbon`), seja qual for o fuso de quem visita, e destaca o dia de hoje no horário.
- O céu dentro do arco acompanha a altitude real do sol sobre Faro (dia / fim de tarde / pôr do sol / noite). Para mostrar numa chamada pode-se forçar com `?ceu=night`, `?ceu=dusk`, `?ceu=golden` ou `?ceu=day`.
- O scroll faz atravessar o arco (CSS scroll-driven animations, só desktop, com `@supports`). A muralha do mapa desenha-se à entrada no ecrã. A mudança PT/EN usa View Transitions entre documentos. Tudo isto desliga com `prefers-reduced-motion`.
- Reservas sem backend: o formulário compõe a mensagem em tempo real, mostra-a num "talão" e abre `wa.me/351911013101?text=…` ou `sms:`. Recusa domingos e datas passadas.
- Lighthouse mobile (servidor local): PT 99/100/100/100, EN 98/100/100/100 (performance/acessibilidade/boas práticas/SEO).

## Reconstruir

```bash
python3 tools/map/osm2svg.py tools/map/osm-vila-adentro.json tools/map/map.svg
python3 tools/build.py
cd public && python3 -m http.server 8790   # depois: node tools/qa/shots.mjs qa
```
