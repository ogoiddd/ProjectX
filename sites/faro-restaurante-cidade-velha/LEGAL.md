# Restaurante Cidade Velha · Faro: legalidade, segurança e funcionamento

Revisão de 2026-10-09 sobre `public/` (demo para cold call, não publicada). Não somos advogados: o que está marcado "validar" deve ser confirmado pelo cliente ou pelo contabilista/jurista dele antes de publicar.

Legenda: ✅ cumprido · ⚠️ precisa de dados/decisão do cliente · ❌ bloqueia a publicação (não a demo)

Todas as alterações de texto/HTML foram feitas nas fontes (`tools/i18n.py`, `tools/legal.py`, `tools/build.py`) e o site foi regenerado com `python3 tools/build.py`.

## 1. RGPD (Reg. UE 2016/679, Lei 58/2019)

| Ponto | Estado | Notas |
|---|---|---|
| Política de privacidade PT + EN | ✅ | `/privacidade/` e `/en/privacy/` (texto em `tools/legal.py`). Responsável, finalidades, bases legais (art. 6.º/1 b) para a reserva; art. 9.º/2 a) para alergias, que são dados de saúde; art. 6.º/1 f) para os registos do alojamento), prazos, partilha (WhatsApp/Meta, fornecedores de email, Vercel), transferências (DPF/CCT), direitos, CNPD, ausência de decisões automatizadas. FR e DE ligam para a versão EN, com a indicação "(en anglais)" / "(auf Englisch)". |
| Identificação do responsável (denominação social, NIF) | ❌ | `[CONFIRMAR COM CLIENTE]` na política e no rodapé das 4 línguas. Sem isto a política não é válida: bloqueia a publicação, não a demo. |
| Aviso de tratamento no formulário (4 línguas) | ✅ | Junto aos botões: o site não recebe nem guarda dados; a mensagem é escrita no aparelho e é o visitante que a envia; uso só para a reserva; alergias só para preparar a refeição; regras da Meta no WhatsApp; link para a política. |
| Minimização | ✅ | Nome, dia, hora, pessoas, lugar, telefone (opcional, útil para quem envia por email) e notas (opcional). Limites: nome 80, telefone 30, notas 300 caracteres. Sem checkboxes pré-marcadas (o rádio "Tanto faz" é uma preferência, não um consentimento). |
| Dados de saúde (alergias nas notas) | ⚠️ | Coberto por consentimento explícito na política. Validar o prazo proposto (apagar mensagens até 30 dias depois da reserva) e que a equipa o cumpre no telemóvel/WhatsApp/email. |
| Avaliações de terceiros | ✅ / ⚠️ | Os 4 excertos foram confirmados verbatim (Algarve Atlas para os do Google; Trip.com para os do TheFork). Aparecem **sem nome de autor** ("Avaliação Google", "Cliente TheFork (via Trip.com)"). A atribuição passou a indicar que os do TheFork foram lidos no Trip.com. A avaliação "Atendimento ágil e atencioso." está em português do Brasil e passou a `lang="pt"`. Validar com o cliente a autorização/escolha final (selo já no site). |
| Citação da NiT | ✅ / ⚠️ | Verbatim confirmado (Adriano Guerreiro, NiT, 11/08/2020). Citação curta, com autor, data e "(traduzido do português)" em EN/FR/DE. Nomeia Orlando Rosa porque o artigo o nomeia como responsável pela casa: confirmar com ele que concorda. |
| Registos do alojamento (Vercel) | ⚠️ | Descrito na política. Na publicação: aceitar o DPA da Vercel na conta do cliente, ou trocar o texto se o alojamento for outro. |

## 2. Cookies e terceiros (Lei 41/2004)

| Ponto | Estado | Notas |
|---|---|---|
| Cookies / armazenamento local | ✅ | Nenhum (testado: `document.cookie` vazio, `localStorage` e `sessionStorage` vazios). Sem analytics nem pixels, por isso não há banner (não é exigido). Se o cliente quiser estatísticas: Plausible/Umami sem cookies, e atualizar a política e a CSP. |
| Pedidos a terceiros ao carregar | ✅ | Zero (testado no Chromium em todas as páginas). Fontes auto-alojadas; mapa SVG desenhado a partir do OSM, sem iframe. Google Maps, Apple Maps, WhatsApp, Facebook, Instagram, Livro de Reclamações e CIMAAL são só links. |

## 3. Informação obrigatória e consumidor

| Ponto | Estado | Notas |
|---|---|---|
| DL 7/2004 (art. 10.º): denominação, NIF, morada, contactos | ⚠️ | Morada e telefone no rodapé e na política. Denominação social, NIF e email `[CONFIRMAR COM CLIENTE]`. A restauração não precisa de registo profissional. |
| Livro de Reclamações Eletrónico (DL 156/2005, red. DL 74/2017) | ✅ | Link `https://www.livroreclamacoes.pt/Inicio/` no rodapé das 4 línguas, na política e na 404. Validar: o cliente tem de estar registado na plataforma e ter o livro físico na sala. |
| RAL (Lei 144/2015, art. 18.º) | ✅ / validar | Rodapé ("Litígios de consumo: CIMAAL" → consumoalgarve.pt) e política (CIMAAL, Av. 5 de Outubro, 55, r/c, 8000-075 Faro, 289 823 135) + Portal do Consumidor. Confirmar se o restaurante aderiu a outra entidade. A plataforma ODR da UE foi encerrada em julho de 2025, por isso não leva link. |
| Alergénios (Reg. UE 1169/2011, art. 44.º; DL 26/2016) | ⚠️ | Aviso novo na carta (4 línguas): os pratos listados incluem peixe, crustáceos, moluscos, ovos, leite, frutos de casca rija e glúten; a informação escrita sobre os 14 alergénios por prato está disponível na sala. O cliente tem de ter essa tabela de facto. Se publicar a carta completa no site, indicar os alergénios por prato. |
| Preços (DL 138/90) | ✅ / ⚠️ | Nenhum preço inventado. Cada "— €" é decorativo (`aria-hidden`) e os leitores de ecrã ouvem "preço a confirmar" (antes era só um `title`, que não é anunciado de forma fiável). O selo `[CONFIRMAR COM CLIENTE: carta completa e preços]` está no topo da carta e há a nota "Preços: os da carta da casa, com IVA incluído". O JSON-LD não tem `priceRange` nem `offers`. Quando houver preços: finais, com IVA, iguais aos da carta afixada. |
| Horário | ⚠️ | Seg–sáb 11:00–22:00 (Google), mas há 4 fontes em conflito (ver README). O site mostra "Aberto agora" e valida o formulário com base nele: confirmar antes de publicar. |
| Número de avaliações | ⚠️ | 1458 (Algarve Atlas, revisto hoje); o Wanderlog já mostra 1496. Atualizar antes de publicar. |
| WhatsApp 916 008 548 e email de reservas | ❌ | O número aparece também no Cidade Velha Rooftop e não se sabe se tem WhatsApp. O email não existe: o botão "Enviar por email" abre um `mailto:` sem destinatário. Para a demo serve; para publicar, confirmar o número e o email, ou retirar o botão. |

## 4. Direitos de autor e acessibilidade

| Ponto | Estado | Notas |
|---|---|---|
| Tipos de letra | ✅ | Bodoni Moda, Marcellus SC, Jost: SIL OFL, auto-alojadas. Registado no README e na política. |
| Mapa | ✅ | © colaboradores do OpenStreetMap (ODbL), no mapa e no rodapé. |
| Imagens | ✅ / ⚠️ | Só desenhos SVG originais. Fotos são molduras `[FOTO DO CLIENTE]`: o cliente fornece fotos com direitos (e autorização das pessoas reconhecíveis). |
| Acessibilidade (objetivo WCAG 2.1 AA) | ✅ | Lighthouse a11y 100 (README). Nesta revisão: erro de hora com `aria-invalid` e `aria-live`, estado de envio com `role="status"`, preço com texto acessível, `lang` correto nas citações. Não é e-commerce, a Lei Europeia da Acessibilidade não se aplica diretamente. |

## 5. Segurança

| Ponto | Estado | Notas |
|---|---|---|
| Arquitetura | ✅ | 100 % estático, sem servidor, sem dependências npm em produção, sem segredos. |
| Cabeçalhos (`public/vercel.json`) | ✅ | Antes só havia `nosniff`, `Referrer-Policy` e `Permissions-Policy`. Agora: CSP `default-src 'none'` sem `unsafe-inline` (`script-src 'self'` + sha256 do único script inline, o que acrescenta a classe `js`; os `<script type="application/json">` / `ld+json` são dados e não executam), `style-src 'self'`, `img-src/font-src/manifest-src/connect-src 'self'`, `frame-ancestors 'none'`, `form-action 'self'`, `base-uri 'none'`, `object-src 'none'`, `upgrade-insecure-requests`; HSTS 2 anos; `X-Frame-Options: DENY`; `Referrer-Policy: strict-origin-when-cross-origin`; `Permissions-Policy` alargada; COOP e CORP `same-origin`. |
| Estilos inline | ✅ | Havia 12 atributos `style=` no HTML, que a CSP bloquearia. Passaram a classes em `styles.css` (screenshots antes/depois idênticos na primeira dobra). `build.py` agora falha se aparecer um `<script>` inline sem hash, um `style=` ou um `on*=`. |
| XSS | ✅ | Sem `innerHTML`; a pré-visualização e o estado do envio usam `textContent`; o texto vai para o URL com `encodeURIComponent`. Testado nas 4 línguas com `<img src=x onerror=…>"><script>…</script>` no nome e nas notas: aparece como texto, não cria nós, não executa, sem diálogos. |
| Links externos / `target=_blank` | ✅ | Todos os externos têm `rel="noopener"`; o WhatsApp abre com `window.open(..., "noopener")` (testado: `window.opener === null`). Sem redirects abertos. |
| Email / SPF / DKIM / DMARC | n/a | O site não envia email. |
| HSTS `includeSubDomains` | ⚠️ | Ao ligar o domínio final, confirmar que todos os subdomínios têm HTTPS (ou retirar `includeSubDomains`). |
| Root Directory | ⚠️ | `vercel.json` está em `public/`: o projeto Vercel tem de usar `public` como Root Directory, senão os cabeçalhos não são aplicados. |

## 6. Funcionamento

| Ponto | Estado | Notas |
|---|---|---|
| Formulário: estados | ✅ | Erros visíveis + `aria-invalid` para nome vazio, data passada, domingo e (novo) hora já passada hoje ("Para hoje já não há horas: escolha outro dia ou ligue-nos"). Novo estado de envio nas 4 línguas ("A abrir o WhatsApp com a mensagem pronta… A mesa fica reservada quando a casa responder.") com link de recurso se a janela não abrir. Mensagem para a sala sempre em PT, com a língua do cliente (testado: chega `wa.me/351916008548?text=…` com todos os campos). |
| Fallback sem JS | ✅ | `<noscript>` (4 línguas) com telefone e WhatsApp; sem JS ficam escondidos os campos, os botões de envio, a pré-visualização e os botões de rota (que não funcionariam). Horário, morada, mapa e direções continuam visíveis. Testado com JS desligado. |
| tel / WhatsApp / direções | ✅ / ⚠️ | `tel:+351289827145` em todo o lado; Google Maps (`dir/?api=1&destination=37.0135551,-7.9345962&travelmode=walking`) e Apple Maps com as coordenadas OSM. WhatsApp: ver ponto 3. |
| 404 | ✅ | `public/404.html` em PT/EN/FR/DE, `noindex`, links para as 4 versões e telefone. Testado com resposta 404. |
| sitemap / robots / hreflang | ✅ | `sitemap.xml` com as 4 línguas (pt-PT, en, fr, de + x-default → /en/) e as 2 páginas de privacidade (pt-PT/en). Canonical por página. `robots.txt` permite tudo. Domínio de demo `cidade-velha-faro.vercel.app`: trocar `BASE` em `tools/build.py` e o `robots.txt`. Para um deploy de demonstração público, considerar `noindex` para não competir com a ficha Google da casa. |
| Cache / performance | ✅ | Fontes 1 ano `immutable` (nomes estáveis: se mudarem, mudar o nome); assets 7 dias com `stale-while-revalidate`; CSS/JS 1 h com `must-revalidate` (não têm hash). Fontes com preload e `font-display: swap`. Compressão feita pelo Vercel. |
| Teste de fumo (Chromium) | ✅ | Servidor local que aplica os cabeçalhos de `vercel.json`: `/`, `/en/`, `/fr/`, `/de/`, `/privacidade/`, `/en/privacy/` 200, 0 erros de consola, 0 violações de CSP, 0 pedidos a terceiros; links internos e âncoras válidos; formulário testado nas 4 línguas. |

## Bloqueia a publicação (não a demo)

- Denominação social, NIF e email (DL 7/2004 e responsável RGPD).
- Número de WhatsApp confirmado e email de reservas (ou retirar o botão de email).
- Horário confirmado (o "Aberto agora" e a validação dependem dele).
- Prazo de conservação das mensagens e validação jurídica da política.
- Domínio final no `BASE` de `tools/build.py` e no `robots.txt`.
