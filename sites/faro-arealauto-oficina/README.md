# Arealauto, Faro: demo do site

Site de uma página para a **Arealauto - Oficina de Reparações, Lda.** (Sítio do Brejo, Areal Gordo, 8005-409 Faro, +351 289 882 080). Ainda não está publicado.

- `public/`: o site estático, sem build (`index.html`, `styles.css`, `app.js`, `fonts/`, `assets/`, `vercel.json`, `robots.txt`, `sitemap.xml`, `site.webmanifest`).
- `tools/map/osm2svg.py`: desenha o mapa a partir do OpenStreetMap e injeta-o no `index.html`.
- `tools/og/`: imagem OG (`og.html` mais `render.mjs`) e ícones PNG gerados a partir de `assets/favicon.svg`.
- `tools/qa/shots.mjs`: screenshots para desktop e mobile, guardados em `qa/`.

## Conceito

1. A oficina é contada como um caderno de bairro com 30 anos: folha de obra, carimbo, talão, quadro de ferramentas e nomes bordados no fato-macaco.
2. As cores vêm do sítio e do ofício: areia (de "Areal Gordo"), cal algarvia, tinta azul de folha de obra e vermelho de carimbo. Os títulos usam um condensado de letreiro pintado (Big Shoulders); o texto corrido usa uma serifa de jornal (Literata); os dados usam mono (Plex Mono).
3. O site faz o trabalho da receção: diz se a oficina está aberta agora, preenche a folha de obra e transforma-a numa mensagem de WhatsApp ou email, e mostra o caminho desde Faro.

Diferenças em relação a `sites/chaveca-janeira` (também é uma oficina de Faro): fundo claro e não escuro, sem vídeo, sem three.js, sem roda e sem porta de garagem. A grelha é editorial e assimétrica e o tom é "casa com 30 anos" em vez de "marca de rede".

## Factos usados e fontes

| Facto | Fonte |
|---|---|
| Nome legal "Arealauto - Oficina de Reparações, Lda.", NIPC 503688894, sociedade por quotas, constituída a 14-06-1996, 11 a 15 empregados, sede no Sítio do Brejo/Areal Gordo, 8005-409 Faro | Iberinform, https://www.iberinform.pt/empresa/21171636/arealauto-oficina-de-reparacoes-lda (via `vendas/faro/decisores.json`) |
| Telefone 289 882 080 | Google Maps, Waze, rotanacional.pt, autonews.pt e a lista Ocidental |
| Nome na ficha Google "Arealauto", nota **4,4**, Plus Code 24R3+9G, coordenadas 37.040886, -7.896193, place id ChIJkREmmcmsGg0R28XofdkM01o | Google Maps, consultado a 9-10 out. 2026 (vista limitada) |
| Entrada e estacionamento acessíveis a cadeiras de rodas | Google Maps, separador "Acerca de" |
| Horário seg–sex 08:30–12:30 e 14:00–18:00; sábado e domingo fechado | Waze (https://www.waze.com/live-map/directions/pt/faro/faro/topcar-arealauto?to=place.ChIJkREmmcmsGg0R28XofdkM01o). O Google Maps mostra sexta-feira com o mesmo horário e, numa sexta à noite, indica "abre às 08:30 de segunda" |
| "Multimarca" e presença na Rede de Oficinas Recomendadas da Ocidental (Ageas Portugal), como "Areal Auto, Lda., Sitio Areal Gordo, 8005-409 Faro, 289882080" | PDF público https://www.ocidental.pt/Umbraco/Surface/Services/GetWorkshopsReport/?type=A, gerado a 9 out. 2026 |
| Email arealauto@iol.pt (**a confirmar**) | autonews.pt, https://www.autonews.pt/oficinas-auto/dir/d/faro/c/faro/p-12856/arealauto-oficina-de-reparacoes/ |
| Mapa (estradas, EN 125, EN 2, nomes de lugares) | © contribuidores OpenStreetMap (ODbL), API 0.6, bbox -7.950..-7.880 / 37.005..37.052 |
| RAL CIMAAL e Livro de Reclamações | Obrigações legais genéricas para o consumo no Algarve, iguais às da demo Chaveca & Janeira |

Não há preços, prémios, história, avaliações nem fotos de terceiros. Os ícones das ferramentas, o mapa, o conta-quilómetros e a imagem OG são composições próprias em SVG/CSS.

## Marcado [CONFIRMAR COM CLIENTE] no site

- Serviços 02 a 06 (revisões, travões e suspensão, diagnóstico, motor e embraiagem, pré-inspeção). Só "reparação multimarca" tem confirmação. A categoria da ficha Google é "Serviços de usinagem automotiva": vale a pena perguntar se fazem retificação ou trabalhos de torno.
- História da casa, número exato de pessoas, nomes e funções (os emblemas bordados).
- Número de avaliações Google e duas citações verbatim (a vista limitada do Google não mostra o texto das avaliações).
- WhatsApp: `CONFIG.whatsapp` em `app.js` está `null`. Enquanto não houver número, o WhatsApp abre com a mensagem pronta e o cliente escolhe o contacto.
- Email, feriados e férias de agosto, outras seguradoras ou acordos, e o domínio (`arealauto.pt` está como placeholder em canonical, OG, sitemap e JSON-LD).
- Fotos: 3 molduras `[FOTO DO CLIENTE]` com a descrição do que fotografar (equipa à porta, portão com letreiro, mãos no motor), mais um quadro de ferramentas real, se existir.

## Notas para o vendedor

- O Google e o Waze já usaram o nome **"TOPCAR - Arealauto"**. A lista atual de oficinas TOPCAR (topcar.com.pt/oficinas, out. 2026) já não inclui a Arealauto, e a página `topcar.com.pt/oficina/topcar-arealauto` dá erro 500. Pela ficha Google atual, parece que a oficina saiu da rede: é um bom motivo para ter um site próprio. Confirmar na chamada. O site não usa a marca TOPCAR.
- Faltam fotos na ficha Google ("Adicione fotos") e não há website ("Adicionar website").

## Comportamento (app.js)

- Estado "aberto agora" calculado na hora de Lisboa (`Intl`, `Europe/Lisbon`): aberto, fecha em breve, almoço, fechado ou feriado, com a próxima abertura. Considera os feriados nacionais, a Páscoa móvel e o 7 de setembro (Faro). Atualiza a cada 30 s.
- O conta-quilómetros passa de 1996 para o ano atual quando entra no ecrã. Os anos de casa são calculados a partir de 14-06-1996.
- No quadro de ferramentas, cada ferramenta é um `<button aria-pressed>` ligado à linha do serviço.
- Folha de obra: valida nome e telemóvel, formata a matrícula (AA-00-AA), lista os próximos 10 dias úteis e gera uma referência FO-AAMMDD-XXXX. Mostra a pré-visualização em "cópia químico" e envia por WhatsApp (`wa.me`), `mailto:` ou cópia. Não tem backend nem guarda dados.
- `prefers-reduced-motion` desliga todas as animações. O desenho do mapa ao fazer scroll só corre onde há `animation-timeline: view()`.

## Regenerar

```bash
# mapa (4 tiles da API OSM)
for b in "-7.950,37.005,-7.915,37.028" "-7.950,37.028,-7.915,37.052" "-7.915,37.005,-7.880,37.028" "-7.915,37.028,-7.880,37.052"; do
  curl -o "t_${b}.json" "https://api.openstreetmap.org/api/0.6/map.json?bbox=$b"; done
python3 -I tools/map/osm2svg.py public/index.html t_*.json
node tools/og/render.mjs           # og.jpg e ícones
(cd public && npx http-server -p 8611 -s .) & node tools/qa/shots.mjs
```
