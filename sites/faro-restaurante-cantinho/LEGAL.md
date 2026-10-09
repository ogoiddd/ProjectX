# Cantinho · Faro: legalidade, segurança e funcionamento

Revisão de 2026-10-09 (demo para cold call, não publicada). Não somos advogados: os pontos marcados "validar" devem ser confirmados pelo cliente ou pelo seu contabilista/jurista antes de publicar.

Legenda: ✅ cumprido · ⚠️ precisa de dados/decisão do cliente · ❌ bloqueia a entrega

## 1. RGPD (Reg. UE 2016/679, Lei 58/2019)

| Ponto | Estado | Notas |
|---|---|---|
| Política de privacidade PT + EN | ✅ | `/privacidade/` e `/en/privacy/` (template `tools/src/privacidade.html`). Responsável, finalidades, base legal (art. 6.º/1 b) e f); art. 9.º/2 a) para alergias), prazos, partilha (WhatsApp/Meta, operadores SMS, Vercel), transferências (DPF/CCT), direitos, CNPD. |
| Identificação do responsável (denominação, NIF) | ❌ | `[CONFIRMAR COM CLIENTE]` na política e no rodapé. Sem isto a política não é válida: bloqueia a publicação, não a demo. |
| Formulário de reserva: aviso de tratamento | ✅ | Texto junto ao botão: o site não recebe nem guarda dados; seguem na mensagem do próprio utilizador; uso só para a reserva; alergias só para preparar a refeição; link para a política. |
| Minimização | ✅ | Só nome, dia, hora, pessoas, lugar, notas (opcional). Sem telefone/email no formulário (o canal já o identifica). `maxlength` em nome (80) e notas (200). Sem checkboxes pré-marcadas (o rádio "Na sala" é preferência, não consentimento). |
| Dados de saúde (alergias nas notas) | ⚠️ | Coberto por consentimento explícito na política. Validar com o cliente o prazo de conservação proposto (apagar mensagens até 30 dias após a reserva) e que a equipa cumpre isso no telemóvel/WhatsApp. |
| Avaliações de terceiros | ✅/⚠️ | Nomes reduzidos a nome próprio + inicial. Excertos curtos com fonte (Google). Validar: se o cliente preferir, substituir por avaliações que ele próprio possa usar. |
| Citação MAGG (Diogo Ferreira) | ⚠️ | Citação curta com fonte (direito de citação). Confirmar que o Diogo concorda em aparecer com nome. |
| Registos do alojamento (Vercel) | ⚠️ | Descrito na política. Na publicação: aceitar o DPA da Vercel na conta do cliente. |

## 2. Cookies e terceiros (Lei 41/2004)

| Ponto | Estado | Notas |
|---|---|---|
| Cookies / localStorage | ✅ | Nenhum. Sem analytics, sem pixels. Por isso não há banner (não é exigido). Se o cliente quiser estatísticas, usar Plausible/Umami sem cookies e atualizar a política e a CSP. |
| Conteúdos de terceiros embebidos | ✅ | Nenhum: tipos de letra locais, mapa desenhado em SVG a partir do OSM (sem iframe Google Maps). Google Maps, Apple Maps, WhatsApp, Instagram e Facebook são só links. |

## 3. Informação obrigatória e consumidor

| Ponto | Estado | Notas |
|---|---|---|
| DL 7/2004 (art. 10.º): denominação, NIF, morada, contactos | ⚠️ | Morada e contactos no rodapé e na política; denominação e NIF `[CONFIRMAR COM CLIENTE]`. Email geral.cantinho@gmail.com `[CONFIRMAR]` (fonte de 2021). |
| Livro de Reclamações Eletrónico (DL 156/2005, DL 74/2017) | ✅ | Link `https://www.livroreclamacoes.pt/Inicio/` no rodapé e na política. O livro físico na sala continua obrigatório. Validar: o cliente tem de estar registado na plataforma. |
| RAL (Lei 144/2015, art. 18.º) | ⚠️ | Indicada a entidade competente para Faro: CIMAAL (Av. 5 de Outubro, 55, r/c, 8000-075 Faro, 289 823 135, consumoalgarve.pt) + Portal do Consumidor. Confirmar se o restaurante aderiu a outra entidade. |
| Alergénios (Reg. UE 1169/2011, art. 44.º; DL 26/2016) | ⚠️ | Aviso na ementa: informação sobre os 14 alergénios disponível por escrito na sala. O cliente tem de ter essa informação de facto (tabela por prato). Se publicar a ementa completa no site, indicar os alergénios por prato. |
| Preços (DL 138/90; DL 10/2015) | ⚠️ | O site não mostra preços (`— €`). Quando mostrar: com IVA incluído (texto já presente) e coincidir com a ementa afixada. Couvert: só cobrável se o cliente o puder recusar; não está no site. |
| Horário | ⚠️ | Seg–sáb 10:30–23:30 (Google); MAGG 2021 dizia 12:00–22:00. Confirmar, e horário da cozinha. |
| WhatsApp no 911 013 101 | ⚠️ | Se não houver, retirar o botão WhatsApp (fica SMS + chamada). |

## 4. Direitos de autor e acessibilidade

| Ponto | Estado | Notas |
|---|---|---|
| Tipos de letra | ✅ | Gloock, Newsreader: SIL OFL 1.1, alojados no site. Registado no README. |
| Mapa | ✅ | © OpenStreetMap contributors (ODbL), atribuição visível. |
| Imagens | ✅/⚠️ | Só ilustrações próprias. 6 molduras `[FOTO DO CLIENTE]`: o cliente fornece fotografias com direitos (e autorização de pessoas reconhecíveis). |
| Acessibilidade (WCAG 2.1 AA, objetivo) | ✅ | Lighthouse a11y 100 (README), labels, erros com `aria-live` e `aria-invalid`, foco visível, `prefers-reduced-motion`. Não é e-commerce, a Lei Europeia da Acessibilidade não se aplica diretamente. |

## 5. Segurança

| Ponto | Estado | Notas |
|---|---|---|
| Arquitetura | ✅ | 100 % estático, sem servidor, sem dependências npm em produção, sem segredos. |
| Cabeçalhos (`public/vercel.json`) | ✅ | CSP `default-src 'none'` sem `unsafe-inline` (único script inline autorizado por sha256; `build.py` falha se o hash não bater), `frame-ancestors 'none'`, `form-action 'self'`, `base-uri 'none'`, `object-src 'none'`, `upgrade-insecure-requests`; HSTS 2 anos; `nosniff`; `X-Frame-Options: DENY`; `Referrer-Policy: strict-origin-when-cross-origin`; `Permissions-Policy`; COOP. |
| XSS | ✅ | Sem `innerHTML`; o talão usa `textContent`; o texto vai para o URL com `encodeURIComponent`. Testado com `<img src=x onerror=…>` no nome: não executa. |
| Links externos | ✅ | Nenhum `target=_blank`; externos com `rel=noopener`. Sem redirects abertos. |
| Email/SPF/DKIM | n/a | Não há envio de email pelo site. |
| HSTS `includeSubDomains` | ⚠️ | Ao ligar o domínio final, confirmar que todos os subdomínios têm HTTPS (ou retirar `includeSubDomains`). |

## 6. Funcionamento

| Ponto | Estado | Notas |
|---|---|---|
| Formulário: estados | ✅ | Erro de nome vazio, domingo e data passada (texto visível + `aria-invalid`); mensagem "A abrir o WhatsApp… / as mensagens…" ao enviar, com telefone de recurso. |
| Fallback sem JS | ✅ | Horários estáticos no HTML; `<noscript>` com telefone, SMS e WhatsApp; botões de envio e talão escondidos sem JS. |
| tel / WhatsApp / SMS / direções | ✅ | `tel:+351911013101`, `wa.me/351911013101?text=…`, `sms:+351911013101?&body=…`, Google Maps e Apple Maps com coordenadas OSM. |
| 404 | ✅ | `public/404.html` bilingue (PT + EN), `noindex`. |
| sitemap / robots / hreflang | ✅ | 4 URLs com `hreflang` pt-PT/en/x-default; canonical por página. Domínio `cantinho-faro.vercel.app` provisório: trocar em `build.py`, `sitemap.xml`, `robots.txt`. |
| Cache | ✅ | Fontes 1 ano `immutable` (ficheiros não mudam), assets 1 semana, CSS/JS 1 h com revalidação (nomes sem hash). |
| Teste de fumo (Chromium) | ✅ | `/`, `/en/`, `/privacidade/`, `/en/privacy/` 200 sem erros de consola nem violações de CSP; 404 devolve a página personalizada; links internos todos 200; formulário gera URL WhatsApp e SMS corretos. |
