# Taberna Zé-Zé: legalidade, segurança e funcionamento

Revisão de 2026-10-09 sobre `public/`. Esta lista não é aconselhamento jurídico: os pontos marcados com "validar" são para o cliente confirmar com o contabilista ou o advogado dele antes de publicar.

Legenda: OK = cumprido no site · CLIENTE = precisa de dados ou decisão do cliente · BLOQUEIA = impede a publicação (a demo não é afetada)

## 1. Legal

| Tema | Estado | Detalhe |
|---|---|---|
| RGPD: aviso de tratamento no pedido de mesa | OK | O texto `.fine` da comanda (PT/EN) diz quem trata os dados, para quê, que o site não guarda nada, que as alergias só são usadas para a refeição, que no WhatsApp se aplicam também as regras da Meta, e tem link para a política. Não há checkboxes. Só o nome e a nota são campos livres, e a nota é opcional. |
| RGPD: política de privacidade PT + EN | OK / CLIENTE | `privacidade.html` e `privacy.html`: responsável, finalidades, bases legais (6.º/1/b para a reserva; 9.º/2/a para alergias, que são dados de saúde; 6.º/1/f para os registos do alojamento), subcontratantes (WhatsApp/Meta, operadoras, alojamento), transferência para os EUA, direitos, CNPD, ausência de decisões automatizadas. Falta: **denominação social, NIPC, email e prazo de conservação das mensagens** (sugestão: 30 dias). Confirmar o alojamento (Vercel) e validar o texto. |
| Cookies / ePrivacy (Lei 41/2004) | OK | Zero cookies, zero analytics e zero pedidos a terceiros ao carregar a página: as fontes são auto-alojadas e o mapa é SVG inline. O único armazenamento é `localStorage.lang` (`pt`/`en`), gravado só quando o visitante muda o idioma. É estritamente necessário, por isso não precisa de banner (art. 5.º/3). Está explicado na política. Google Maps, WhatsApp, Facebook e Tripadvisor só abrem com clique, como links. Se no futuro se puser analytics, usar uma ferramenta sem cookies (Plausible/Umami) e atualizar a política. |
| Livro de Reclamações Eletrónico (DL 156/2005, red. DL 74/2017) | OK / CLIENTE | Link destacado (a negrito) no rodapé e na política, para `livroreclamacoes.pt/Inicio/`. O cliente tem de confirmar que tem o livro físico e a adesão à plataforma digital. |
| RAL (Lei 144/2015, art. 18.º) | OK / validar | O rodapé e a política indicam o CIMAAL, Centro de Informação, Mediação e Arbitragem de Conflitos de Consumo do Algarve (consumoalgarve.pt, 289 823 135), competente para o distrito de Faro, e remetem para consumidor.gov.pt. O cliente deve confirmar se aderiu a algum centro. A plataforma europeia ODR foi encerrada em julho de 2025, por isso não leva link. |
| Informação obrigatória (DL 7/2004, art. 10.º) | CLIENTE | O nome comercial, a morada e o telefone já lá estão. A **denominação social, o NIPC e o email** estão como `[CONFIRMAR COM CLIENTE]` no rodapé e na política. A restauração não precisa de registo profissional. |
| Alergénios (Reg. UE 1169/2011; DL 26/2016) | OK / CLIENTE | O cabeçalho da ementa (PT/EN) avisa que os pratos levam crustáceos e moluscos, que a lista de ingredientes não substitui a informação sobre os 14 alergénios e que essa informação está disponível na casa. A nota do pedido aceita alergias. O cliente tem de garantir que a casa tem essa informação por escrito, disponível para quem a pedir. Se um dia o site vender take-away online, a informação sobre alergénios tem de estar no site antes da compra. |
| Preços (DL 138/90) | OK / CLIENTE | Não há preços inventados. Cada `€ —` tem texto para leitores de ecrã ("preço por confirmar" / "price to be confirmed"), o JSON-LD não tem `priceRange` nem `offers`, e há a nota "Preços na casa, com IVA incluído". Quando houver preços: valores finais com IVA, iguais aos da ementa afixada à porta. |
| Opiniões e marcas de terceiros | CLIENTE | São citações curtas de opiniões Google, com o autor identificado. O número de opiniões (963) tem de ser atualizado antes de publicar (ver README). |
| Direitos de autor | OK | Fontes OFL auto-alojadas. Azulejo, logótipo, cataplana e ícones desenhados de raiz. Mapa © OpenStreetMap (ODbL), creditado. Não há fotos de terceiros: as fotos do cliente estão em `[FOTO DO CLIENTE]`. |
| Acessibilidade (objetivo WCAG 2.1 AA) | OK | Lighthouse a11y 100 (README). Nesta revisão: "€ —" com texto acessível; nos controlos que não funcionam sem JS, o aviso é dado em texto. |

## 2. Segurança

| Tema | Estado | Detalhe |
|---|---|---|
| Arquitetura | OK | Estático, sem backend, sem segredos e sem dependências em runtime. |
| Cabeçalhos (`public/vercel.json`) | OK | CSP estrita sem `unsafe-inline`: `default-src 'none'`; scripts `'self'` mais o hash sha256 do único script inline (o do `<head>` que evita o salto de idioma); `style-src 'self'`; `frame-ancestors 'none'`; `base-uri 'none'`; `object-src 'none'`; `form-action 'self'`; `upgrade-insecure-requests`. Também HSTS (2 anos), `nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`, COOP e CORP. Testado com um servidor local que aplica estes cabeçalhos: 0 violações de CSP e 0 erros de consola. **Se o script inline mudar, recalcular o hash.** Nota: o `vercel.json` está dentro de `public/`, por isso o projeto Vercel tem de ter `public` como Root Directory. |
| XSS (nome e nota na pré-visualização) | OK | A pré-visualização usa `textContent` e os links usam `encodeURIComponent`. Testado com `<img src=x onerror=alert(1)>` e `</output><script>…`: aparece como texto, não é criado nenhum nó e não abre nenhum diálogo. Os `innerHTML` restantes só recebem strings fixas do dicionário i18n ou valores gerados (datas e horas). O valor de `?lang=` e do `localStorage` passa por uma lista de valores permitidos (`pt`/`en`). |
| `target=_blank` | OK | Todos os links levam `rel="noopener"` (verificado automaticamente, incluindo os links injetados pelo i18n). |
| Open redirects / CSRF / injeção | OK | Não há parâmetros de redirecionamento nem servidor. O `submit` do formulário está bloqueado em JS (o formulário não envia nada). |
| Email / SPF / DKIM / DMARC | n/a | Não há envio de email. Se o cliente usar um domínio próprio com email, configurar estes registos. |

## 3. Funcionamento

| Tema | Estado | Detalhe |
|---|---|---|
| Pedido de mesa (estados) | OK | Dias fechados e horas passadas aparecem desativados, com uma dica para "hoje em cima da hora". A pré-visualização é atualizada ao vivo, a ligação ao WhatsApp é `wa.me/351938735167?text=…` e o SMS é `sms:+351938735167?&body=…`. O texto avisa que a mesa só fica reservada quando a casa responder. |
| Sem JS | OK | Um `<noscript>` (PT+EN) pede para ligar ou enviar uma mensagem. Ficam escondidos os campos que não funcionariam (dia, hora, nome, nota, pré-visualização, "Juntar ao pedido", botão EN). Os botões WhatsApp, SMS e Ligar e as direções continuam a funcionar. |
| tel / WhatsApp / SMS / direções | OK / CLIENTE | `tel:+351938735167` em todos os sítios. As direções são `google.com/maps/dir/?api=1&destination=37.020463,-7.933839`. **Falta confirmar se o 938 735 167 tem WhatsApp** e qual é o número das reservas (a DISH indica 910 344 728 e 289 825 056). |
| 404 | OK | `404.html` (PT+EN, `noindex`). Testado com resposta 404. |
| Sitemap / robots / hreflang | OK | `sitemap.xml` tem `/`, `/?lang=en`, `/privacidade` e `/privacy`, com `xhtml:link` hreflang. A home tem hreflang pt-PT, en (`?lang=en`) e x-default. `?lang=en` abre já em inglês, o botão EN atualiza o URL e o canonical, e o link da política muda para `/privacy`. `robots.txt` permite tudo. **Para um deploy de demonstração público, considerar `noindex`** para não competir com a ficha Google da casa. |
| Cache / performance | OK | Fontes `immutable` 1 ano, porque são ficheiros estáveis (se mudarem, mudar o nome). Assets 7 dias com `stale-while-revalidate`. CSS/JS 1 h com `must-revalidate`, porque não têm hash. Fontes com preload e `font-display: swap`. A compressão é feita pelo Vercel. |

## Bloqueia a publicação (não a demo)

- Denominação social, NIPC e email (DL 7/2004 e responsável RGPD).
- Confirmar que o número usado tem WhatsApp, senão o botão principal falha.
- Horário: há fontes em conflito e o site mostra "Aberto agora" com base nele.
- Prazo de conservação das mensagens e validação jurídica da política.
- Domínio final: trocar `taberna-ze-ze-faro.vercel.app` no canonical, hreflang, OG, JSON-LD, sitemap e robots.
