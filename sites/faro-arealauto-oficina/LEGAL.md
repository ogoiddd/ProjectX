# Arealauto: legalidade, segurança e funcionamento

Revisão técnica de 9-10 out. 2026 da demo em `public/`. Não é parecer jurídico: os pontos marcados "validar" devem ser confirmados pela Arealauto e, de preferência, por um jurista antes de publicar.

Cliente: Arealauto - Oficina de Reparações, Lda., NIPC 503688894, Sítio do Brejo, Areal Gordo, 8005-409 Faro.

## 1. Legal

| Requisito | Estado | Onde / notas |
|---|---|---|
| Informação obrigatória (DL 7/2004, art. 10.º; CSC art. 171.º): denominação, NIPC, sede, contactos | Cumprido | Rodapé de `index.html`, `privacidade.html`, `404.html` |
| Conservatória do Registo Comercial e capital social (CSC art. 171.º) | Precisa do cliente | `[CONFIRMAR COM CLIENTE]` no rodapé |
| Registo profissional | Não aplicável | Oficinas de reparação não têm ordem nem alvará específico de publicitação obrigatória. Validar se há licença municipal ou certificação a mostrar |
| Email de contacto | Precisa do cliente | `arealauto@iol.pt` vem de um diretório (autonews.pt). Também é o destino do `mailto:` da folha de obra (`index.html` e `CONFIG.email` em `app.js`) |
| Livro de Reclamações Eletrónico (DL 156/2005, na redação do DL 74/2017) | Cumprido | Link no rodapé de todas as páginas. O livro físico continua obrigatório na oficina |
| RAL (Lei 144/2015, art. 18.º) | Cumprido, validar | CIMAAL (Algarve), com morada e telefone, e link para a lista no Portal do Consumidor. Confirmar se a oficina aderiu a alguma entidade (marcado `[CONFIRMAR COM CLIENTE]`) |
| CASA (Centro de Arbitragem do Sector Automóvel) | Não usado de propósito | O site arbitragemauto.pt anuncia: "foi decretada a extinção do CASA em Assembleia Geral Extraordinária do dia 10 de janeiro de 2024" e há um Despacho n.º 329/2026 no Diário da República sobre a dissolução. Indicar o CASA como RAL seria informação desatualizada. Se o cliente estiver aderente a outro centro setorial, substitui-se |
| RGPD: aviso de tratamento no formulário | Cumprido | Parágrafo `#aviso-dados` junto aos botões: responsável, finalidade, fundamento, terceiros (WhatsApp/email), link para a política |
| RGPD: política de privacidade | Cumprido, validar | `public/privacidade.html` (`/privacidade`): responsável, NIPC, contactos, finalidades, bases legais, prazos, destinatários, alojamento (Vercel, EUA, DPF), direitos e CNPD |
| Prazo de conservação dos pedidos sem reparação | Precisa do cliente | Proposto 12 meses, marcado `[CONFIRMAR]` |
| Encarregado de proteção de dados | Validar | Assumido "não obrigatório" (PME sem tratamento em grande escala) |
| Minimização de dados | Cumprido | Só nome e telemóvel obrigatórios; matrícula, carro, descrição e dia são opcionais. Sem checkboxes pré-marcadas (o rádio "Manhã" pré-selecionado é uma preferência de horário, não um consentimento) |
| Cookies / ePrivacy (Lei 41/2004) | Cumprido | Zero cookies, zero `localStorage`, zero analytics. Não há banner porque não há nada a consentir |
| Terceiros só após consentimento | Cumprido | Fontes alojadas no site; mapa em SVG local (sem iframe nem tiles). Google Maps, Waze, Apple Mapas e WhatsApp só abrem quando o utilizador clica. Teste em Chromium: zero pedidos a domínios externos ao carregar a página |
| Avaliações Google (nota 4,4) | Validar | Facto público com fonte e data; as citações estão como placeholder. Não inventar texto de avaliações |
| Marca "Ocidental / Ageas" | Validar | Menção factual à rede de oficinas recomendadas, com fonte. Confirmar com o cliente que pode ser mencionada |
| Direitos de autor | Cumprido | Fontes OFL 1.1, mapa ODbL com atribuição, restantes gráficos próprios. Registo em `README.md` |
| Acessibilidade (objetivo WCAG 2.1 AA) | Cumprido no essencial | Skip link, landmarks, labels, `aria-invalid` + mensagens de erro, foco no primeiro erro, `aria-live`, `prefers-reduced-motion`. Não é e-commerce, por isso a Lei Europeia da Acessibilidade não se aplica diretamente |
| Loja / livre resolução (DL 24/2014) | Não aplicável | Não há vendas online |

## 2. Segurança

| Ponto | Estado |
|---|---|
| Arquitetura | Estático puro, sem backend, sem base de dados, sem segredos, sem dependências npm em produção |
| `public/vercel.json` | CSP `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; manifest-src 'self'; connect-src 'self'; form-action 'self' mailto:; base-uri 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests`, sem `unsafe-inline` (o JSON-LD não é executado, por isso não precisa de hash). HSTS 2 anos (sem `includeSubDomains` até se conhecer o domínio do cliente; acrescentar com `preload` depois de verificar subdomínios). `nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`, COOP e CORP |
| CSP testada | Chromium com os cabeçalhos aplicados: zero violações em `/`, `/privacidade` e 404 |
| XSS | A pré-visualização usa `textContent`; o único `innerHTML` (conta-quilómetros) só recebe dígitos gerados pelo código. Testado com `<img src=x onerror=…>` no nome: aparece como texto |
| Links externos | Sem `target=_blank`; o WhatsApp abre com `window.open(url, "_blank", "noopener")`. Todos os URLs são construídos com `encodeURIComponent` |
| Open redirects / injeção / CSRF | Não aplicável (não há servidor nem parâmetros lidos do URL) |
| Email | Não há envio pelo site. Se a oficina passar a usar domínio próprio, configurar SPF, DKIM e DMARC nesse domínio |

## 3. Funcionamento

| Ponto | Estado |
|---|---|
| Formulário com JS | Erros por campo, foco no primeiro erro, estado de sucesso ("Pronta a enviar"), anúncio `aria-live`. WhatsApp abre `wa.me/?text=…` (o utilizador escolhe o contacto até haver número); email abre `mailto:` com assunto e corpo. Testado em desktop e mobile |
| Formulário sem JS | `action="mailto:…" method="post" enctype="text/plain"`, validação nativa (`required`) e aviso `<noscript>` com o telefone |
| `tel:`, `mailto:`, direções | `tel:+351289882080`; Google Maps (coordenadas + place id), Waze e Apple Mapas com as coordenadas 37.040886, -7.896193 |
| 404 | `public/404.html` (Vercel serve-a automaticamente), `noindex` |
| Sitemap / robots | `sitemap.xml` com `/` e `/privacidade`; `robots.txt` aponta para o sitemap. O domínio `arealauto.pt` é placeholder |
| Performance | Sem JS de terceiros, fontes woff2 locais com `font-display: swap` e preload das duas principais, fontes em cache 1 ano `immutable`, assets 1 semana, CSS/JS 1 h com revalidação (os nomes não têm hash) |

## Pendente do cliente antes de publicar

1. Email oficial (e se a folha de obra deve ir para ele).
2. Número de WhatsApp (`CONFIG.whatsapp` em `app.js`).
3. Conservatória e capital social.
4. Entidade RAL a que está aderente, se houver.
5. Prazo de conservação dos pedidos e validação da política de privacidade.
6. Domínio final (canonical, OG, JSON-LD, sitemap, robots) e confirmação do alojamento (Vercel).
7. Autorização para mencionar a Ocidental/Ageas e usar a nota Google.
