# Restaurante Cidade Velha — Faro (demo)

Site de uma página, em 4 línguas, para o **Restaurante Cidade Velha** (R. Domingos Guieiro 19, 8000-311 Faro, na esquina do Largo da Sé · 289 827 145).

- `public/`: o site estático, pronto a publicar (sem build): `/` (PT), `/en/`, `/fr/`, `/de/`, `styles.css`, `app.js`, `fonts/`, `assets/`, `sitemap.xml`, `robots.txt`, `vercel.json`.
- `tools/build.py`: gera as 4 páginas e o `sitemap.xml` a partir de `tools/i18n.py` (todo o texto, por língua) e `tools/art.py` (desenhos SVG). Depois de editar texto: `python3 tools/build.py`.
- `tools/map/osm2svg.py`: desenha o mapa da Vila Adentro e calcula os percursos a pé a partir de um extrato OpenStreetMap (ver abaixo).
- `tools/og/`: imagem de partilha (`og.jpg`) e ícones. `python3 tools/og/og.py && node tools/og/render.mjs http://localhost:PORT`.
- `tools/qa/shots.mjs`: screenshots desktop e mobile por língua para `qa/` (`LANGS=pt,en,fr,de node shots.mjs http://localhost:PORT ../../qa`).

## Conceito

Uma estampa antiga do Largo da Sé impressa numa carta de restaurante. Cal das paredes, pedra da Sé, tinto do Porto que acompanha o Dom Rodrigo, e a noite cor de vinho da Vila Adentro.
Tipografia de carta: Bodoni Moda (títulos e pratos), Marcellus SC (inscrição em pedra: botões, rubricas), Jost (texto). Linhas retas e filetes duplos. Não há arcos em lado nenhum, para não se confundir com a demo do Cantinho (arco/muralha) nem com a da Taberna Zé-Zé (azulejo/cataplana).
Elementos com movimento: o título entra palavra a palavra, o sol da estampa põe-se com o scroll, a linha do tempo vai-se desenhando, a rota a pé desenha-se no mapa, o estado "aberto agora" é calculado na hora de Lisboa e a pré-visualização do pedido de reserva atualiza-se enquanto se escreve. Tudo isto respeita `prefers-reduced-motion`.

## Factos usados e fontes

Verificados de novo a 9-10/10/2026. Tudo o que não se conseguiu comprovar aparece no site com o selo amarelo `[CONFIRMAR COM CLIENTE]`.

| Facto no site | Fonte |
|---|---|
| Nome, morada R. Domingos Guieiro 19, 8000-311 Faro, telefone 289 827 145 | Ficha Google (via [Algarve Atlas](https://algarve-hub-frontend.onrender.com/restaurantes/cidade-velha-faro) e [Wanderlog](https://wanderlog.com/place/details/2551479)); morada e CP também em [portugaldenorteasul.pt](https://www.portugaldenorteasul.pt/3018/cidade-velha), [allaboutportugal.pt](https://www.allaboutportugal.pt/en/faro/restaurants/cidade-velha) e [Trip.com](https://www.trip.com/restaurant/portugal/faro/detail/cidade-velha-34909383/) |
| Horário seg-sáb 11:00-22:00, domingo fechado (usado no "aberto agora" e na validação do formulário) | Ficha Google (Algarve Atlas e Wanderlog, iguais). Ver conflitos abaixo |
| 4,4 no Google, 1458 avaliações | Ficha Google (Algarve Atlas; `vendas/faro/leads.json`). O Wanderlog já mostra 1496: atualizar o número antes de publicar |
| Coordenadas 37.0135551, -7.9345962 e a esquina com o Largo da Sé | Nó OSM 4998717122 "Restaurante Cidade Velha" (OpenStreetMap) |
| Pratos da carta: sopa de peixe, folhado de queijo de cabra, polvo à lagareiro, bife de atum, lulas grelhadas, secreto de porco preto com batata frita e salada, nacos na pedra, Dom Rodrigo com vinho do Porto | Avaliações Google citadas no Algarve Atlas |
| Pratos da carta: arroz de marisco com lagosta, camarão tigre grelhado, camarão frito com alho, cataplana de peixe, bife (com molho de) pimenta, bife à portuguesa, lombo de porco | portugaldenorteasul.pt ("sublinhando-se o arroz de marisco com lagosta, o camarão tigre grelhado, o camarão frito com alho, o arroz ou a cataplana de peixe, o bife pimenta, o bife à portuguesa ou até o lombo de porco") |
| Preços: nenhum. Cada prato mostra "— €" e o selo `[CONFIRMAR COM CLIENTE: carta completa e preços]` | Não publicados pelo restaurante |
| Opções vegetarianas e sem glúten; esplanada ("outdoor seating"); aceita reservas | Trip.com, secção "Good to know" e "Amenities". Ficam com `[CONFIRMAR COM CLIENTE]` |
| "Cozinha regional com alguns toques de fora" | portugaldenorteasul.pt ("comida regional com apontamentos de cozinha internacionais") e allaboutportugal.pt ("Portuguese dishes and some innovations") |
| Citação "O espaço funcionou como pastelaria, mas há algum tempo que tem um menu baseado em comida regional." e Orlando Rosa, "responsável pelo restaurante Cidade Velha, perto do Largo da Sé, há quase 30 anos" | [NiT, Adriano Guerreiro, 11/08/2020](https://www.nit.pt/comida/cafes-e-bares/cidade-velha-rooftop-o-novo-terraco-do-algarve-com-cocktails-de-autor) (artigo sobre o Cidade Velha Rooftop, da mesma família) |
| Avaliação "Everything here is exceptional. Great food, great service, great location. We've been here twice and will be back for more." (12/03/2025) | TheFork, reproduzida no Trip.com como "TheForkUser" |
| Avaliação "…it’s in a beautiful location at the foot of the cathedral, in the old town." e dica "Don’t forget to request a table outside if you’re booking this restaurant" (29/09/2024) | TheFork, reproduzida no Trip.com |
| Avaliação "Atendimento ágil e atencioso." | Avaliação Google (Julia Braga) citada no Algarve Atlas |
| Avaliação "Restaurant sympa près de la cathédrale et du musée de faro, service rapide et serveurs efficaces." | Avaliação Google (Patricia Cossao) citada no Algarve Atlas |
| Facebook `facebook.com/restaurantecidadevelha` e Instagram `@restaurantecidadevelha` | Links publicados em allaboutportugal.pt |
| Telemóvel 916 008 548 (e destino do botão WhatsApp) | Trip.com e allaboutportugal.pt. É **também** o número do Cidade Velha Rooftop (Wanderlog). Tem `[CONFIRMAR]` no site |
| Linha do tempo do Largo: Sé começada em 1251, dois anos depois da conquista cristã; sede da Diocese do Algarve vinda de Silves (1577); saque e incêndio pelas tropas do Conde de Essex (1596); sismo de 1755 destrói grande parte da catedral e a torre sineira sobrevive | [Wikipédia, Sé de Faro](https://pt.wikipedia.org/wiki/S%C3%A9_de_Faro) |
| Arco da Vila inaugurado em 1812, projeto de Francisco Xavier Fabri | [Archiseek](https://www.archiseek.com/arco-da-vila-faro/) e [algarvetips.com](https://www.algarvetips.com/?p=6222) (encomenda do bispo D. Francisco Gomes do Avelar) |
| Percursos a pé: Arco da Vila → restaurante 159 m (no site: 160 m, ~2 min, pela Rua do Município); Arco do Repouso → restaurante 205 m (no site: 200 m, ~3 min, pela Rua do Repouso, Praça Afonso III e Rua Domingos Guieiro) | Calculados no grafo de ruas OpenStreetMap por `tools/map/osm2svg.py` |
| Descrição do Dom Rodrigo (fios de ovos e amêndoa, embrulhado em papel metalizado torcido) | Conhecimento geral sobre o doce algarvio. Não é uma afirmação sobre a receita da casa |

**Desenhos:** a estampa da torre da Sé (com cegonha e mesa de esplanada), o Dom Rodrigo e o logótipo são SVG desenhados de propósito para esta demo. Não usei fotografias de terceiros: todas as fotos são molduras `[FOTO DO CLIENTE]`.

### Conflitos encontrados (perguntar ao cliente)

- **Horário.** O Google dá seg-sáb 11:00-22:00. O OSM dá todos os dias 09:00-22:00. O Trip.com dá 11:30-22:30. O allaboutportugal dá 09:00/10:00-23:00 todos os dias. Um diretório antigo diz "almoço todo o ano, jantar maio-setembro" (`vendas/faro/decisores.json`). O site usa o horário do Google e mostra `[CONFIRMAR COM CLIENTE: jantares todo o ano?]`.
- **Ano de abertura.** O allaboutportugal diz "Back in 1982, a couple who had lived and worked in restaurants in London, decided to open this restaurant". A NiT (2020) dizia que Orlando Rosa estava à frente da casa "há quase 30 anos". Como as datas não batem, nenhuma vai para o site: fica `[CONFIRMAR COM CLIENTE: ano de abertura]`.
- **Pastelaria.** O OSM tem um segundo nó, "Restaurante Cidade Velha - Pastelaria". A NiT fala da pastelaria no passado. Confirmar se o balcão de pastelaria ainda funciona.
- **Código postal.** O Google e os diretórios dizem 8000-311; o OSM diz 8000-202. O site usa 8000-311.
- **Telefone antigo.** Um diretório de 2007 dá 289 815 851 e o site morto `sdias.pt/cvelha` (404). Não são usados.

### Retirado nesta revisão (não comprovado)

- "Frango piri-piri: picante a sério, avisa quem já provou": nenhuma fonte o liga a este restaurante. Foi substituído por "Lombo de porco" (portugaldenorteasul.pt).
- "Bife na pedra… chega à mesa a crepitar": as avaliações falam em "nacos na pedra". Passou a "Nacos na pedra", servidos na pedra quente.
- "Mesas … de frente para a catedral" e "Mesa no Largo": a esplanada está confirmada, mas não onde fica exatamente. Passou a "mesas cá fora".
- "Opções … indicadas no TheFork": não foi possível abrir o TheFork (403), por isso a fonte passou a Trip.com.

## Placeholders `[CONFIRMAR COM CLIENTE]` no site

Carta completa e preços · número de WhatsApp e email de reservas (o botão de email abre um `mailto:` sem destinatário) · horário de jantar ao longo do ano · ano de abertura e a história contada pelo dono, quem cozinha, de onde vem o peixe · estacionamento · autorização para citar as avaliações (e uma em alemão) · opções vegetarianas/sem glúten · telemóvel · todas as fotografias (esplanada, sala, nacos na pedra, Dom Rodrigo, porta do n.º 19).

## Mapa

```bash
curl -o osm.json "https://api.openstreetmap.org/api/0.6/map.json?bbox=-7.9380,37.0115,-7.9300,37.0165"
python3 tools/map/osm2svg.py osm.json tools/map/map.svg   # imprime os metros de cada percurso
python3 tools/build.py
```

Dados © colaboradores do OpenStreetMap (ODbL). A atribuição está no mapa e no rodapé.

## Fontes tipográficas

Bodoni Moda, Marcellus SC e Jost, todas auto-alojadas em `public/fonts/` e com licença SIL Open Font License.

## QA (10/10/2026)

- Lighthouse 12, servidor local: PT mobile 98/100/100/100 (performance/acessibilidade/boas práticas/SEO), DE desktop 100/100/100/100, FR mobile 98/100/100/100. Os avisos de compressão e cache vêm do servidor local; no Vercel não aparecem.
- Formulário testado: rejeita domingos e datas passadas, e gera a mensagem WhatsApp sempre em português, com a indicação da língua do cliente (ver `qa/fr-booking-ticket.png`).
- Screenshots de todas as línguas, desktop e mobile, em `qa/`.
- Domínio de demo usado no canonical, hreflang e sitemap: `https://cidade-velha-faro.vercel.app`. Trocar `BASE` em `tools/build.py` se o domínio mudar.
