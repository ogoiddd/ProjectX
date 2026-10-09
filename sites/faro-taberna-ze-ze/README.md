# Taberna Zé-Zé, Faro (demo)

Site de uma página para a **Taberna Zé-Zé** (Travessa do Alportel 15, 8000-448 Faro, tel. +351 938 735 167). Lead `faro-taberna-ze-ze`. **Demo: não está publicada.**

- `public/`: site estático, sem build: `index.html`, `privacidade.html` / `privacy.html` (política PT/EN), `404.html`, `styles.css`, `app.js`, `fonts/` (Young Serif + Hanken Grotesk, OFL, auto-alojadas), `assets/` (azulejo e logótipo em SVG desenhados à mão, OG e ícones), `vercel.json`, `robots.txt`, `sitemap.xml`, `site.webmanifest`.
- `tools/map/osm2svg.py`: desenha o mapa a partir de um extrato do OpenStreetMap (© OpenStreetMap contributors, ODbL).
- `tools/og/`: `og.html`/`icon.html` + `shoot.mjs` geram `og.jpg` e os PNG dos ícones.
- `tools/qa/`: `shots.mjs` (screenshots desktop/mobile/EN), `interact.mjs` (preenche o pedido de mesa, testa o EN e o teclado), `mapshot.mjs`.
- `qa/`: screenshots da última revisão.

URL canónico usado nas meta tags: `https://taberna-ze-ze-faro.vercel.app/`. É um placeholder; trocar quando houver domínio.

## Conceito

1. Uma casa caiada do Carmo: parede de cal, barra de azulejo azul-cobalto e o cobre da cataplana aberta na mesa.
2. A ementa lê-se como a ardósia da taberna: pratos e ingredientes reais em letra pesada e quente, sem fotos de banco de imagens.
3. Tudo leva a uma coisa: pedir mesa em 3 toques. O pedido sai como uma "comanda" que já vem escrita e segue por WhatsApp ou SMS.

## Factos usados e fontes

| Facto | Fonte |
|---|---|
| Nome, morada `Tv. do Alportel 15, 8000-448 Faro`, telefone `938 735 167` | Ficha do lead (`vendas/faro/leads.json`); Algarve Atlas (espelho da ficha Google): https://algarve-hub-frontend.onrender.com/restaurantes/taberna-ze-ze-faro |
| Google **4,7 · 963 opiniões** | Algarve Atlas (acima), consultado a 2026-10-09. Wanderlog já mostrava 976, por isso o número tem de ser atualizado antes de publicar |
| Horário **seg–sáb 18:00–23:00, domingo fechado** | Algarve Atlas (Google). A pesquisa web cita o mesmo horário do Tripadvisor. **Fontes em conflito, ver abaixo** |
| Coordenadas 37.020463, -7.933839 | JSON-LD da página DISH da casa (bate com o Google) |
| Ementa: 4 cataplanas, 3 arrozes, T-bone Black Angus 500 g, ingredientes copiados tal como estão | Página da casa na plataforma DISH/Makro: https://tabernaze-ze.makro.rest/ (sem preços) |
| "Para 2 pessoas" nas cataplanas e arrozes | Página DISH (acima) |
| Petiscos: lingueirão à Bulhão Pato, amêijoas, lulinhas fritas | Opiniões Google de Helena Pereira e Sandra Chão (Algarve Atlas) |
| Feijoada de lulas com gambas | Resumo de opiniões no Wanderlog: https://wanderlog.com/place/details/1323213/taberna-zé-zé (fonte fraca, confirmar) |
| Arroz de marisco servido com pão frito | Opinião Google de Helena Pereira |
| Casa de família, sala pequena, convém reservar sobretudo no verão | Wanderlog ("family-run", "make reservations in advance"); Airial: https://www.airial.travel/restaurants/portugal/faro/taberna-z%C3%A9-z%C3%A9-aRGnsWit ("room is small"); `decisores.json` |
| Fica junto ao Largo do Carmo, a ~70 m da Igreja do Carmo / Capela dos Ossos, a ~115 m da Praça Silva Porto | Calculado a partir do OpenStreetMap com a coordenada acima |
| Ar condicionado, take-away, eventos privados, pagamento em numerário e cartão de débito | Página DISH (texto de modelo da plataforma: **confirmar**) |
| Facebook `facebook.com/tabernazezefaro`, Tripadvisor d12524292 | Links na página DISH |
| 5 citações de opiniões (Helena Pereira, Joao Viegas, Sandra Chão, Fernando Alves, Luis Soares) | Opiniões Google mostradas no Algarve Atlas. Estão copiadas tal como foram escritas, só com frases inteiras antes do corte "Ler mais". Tirei o emoji do fim da de Helena Pereira. As traduções EN são nossas e estão marcadas como tradução |

Não há preços, prémios, história, datas de fundação nem nomes de pessoas inventados.

## [CONFIRMAR COM CLIENTE]

- **Preços** de todos os pratos. No site aparecem como `€ —`.
- **Horário.** O Google/Tripadvisor dá seg–sáb 18–23. A página DISH dá seg–sáb 12–15 e 18–01. O Wanderlog dá ter–sáb 18–24 com segunda fechada. O site usa o do Google, que está num só sítio: `HOURS` em `app.js` e no JSON-LD.
- **Telefones.** O Google tem 938 735 167. A página DISH tem 910 344 728 (reservas), 289 825 056 (fixo) e o email taberna-barzeze@hotmail.com. Falta saber qual é o número das reservas e **se tem WhatsApp**.
- Horas aceites para reserva. O site oferece 18:30–22:00 de 30 em 30 minutos; foi uma escolha de interface, não uma regra da casa (`SLOTS` em `app.js`).
- Pagamento. A DISH diz numerário e débito; uma listagem diz "cash only".
- Ar condicionado, take-away e eventos privados.
- Nome legal da empresa e NIPC, para o rodapé e para o Livro de Reclamações.
- Nome do dono e da cozinheira. Uma review fala num "Eldu" e o Wanderlog fala numa "Palmira". Não foram usados.
- **Fotos.** Há 3 molduras `[FOTO DO CLIENTE]`: cataplana a abrir na mesa, porta da Travessa do Alportel, sala cheia. Não usei fotos do Google, do Tripadvisor nem do Facebook.

## Nota de vendas

A lead diz "sem website", mas a casa tem uma página automática da DISH (Makro) em `tabernaze-ze.makro.rest`: tem um modelo genérico, horários e telefones que não batem com o Google e nenhum preço. Este é o argumento: "já tem uma página, mas diz coisas diferentes do Google e não converte reservas".

## Re-gerar

```bash
curl -o osm.json "https://api.openstreetmap.org/api/0.6/map.json?bbox=-7.9400,37.0172,-7.9280,37.0240"
python3 tools/map/osm2svg.py osm.json map.svg   # colar o <svg> dentro de .map-crop em index.html
cd tools/og && node shoot.mjs                   # og.jpg + ícones (Playwright + Chromium em /opt/pw-browsers)
cd tools/qa && node shots.mjs ../../qa && node interact.mjs ../../qa   # precisa de: (cd public && python3 -m http.server 8791)
```

`tools/node_modules` é um symlink local para o Playwright global (ignorado no git).

## QA (2026-10-09)

Lighthouse local: mobile 99 / 100 / 100 / 100 e desktop 100 / 100 / 100 / 100 (performance / acessibilidade / boas práticas / SEO), CLS 0. Os avisos de compressão e cache vêm do servidor local; no Vercel não se aplicam. Sem erros de consola. O botão do WhatsApp chega-se por teclado. O movimento (tampa da cataplana, vapor, revelações ao fazer scroll) desliga-se com `prefers-reduced-motion`.

Revisão legal, segurança e funcionamento: ver `LEGAL.md`. O hash CSP do script inline do `<head>` está em `public/vercel.json`: se esse script mudar, recalcular o hash.
