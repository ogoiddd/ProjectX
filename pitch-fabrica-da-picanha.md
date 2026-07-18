# Pitch — Fábrica da Picanha (@fabricadapicanha)

> Auditoria real feita a 18/07/2026 aos sites fabricadapicanha.pt, fabricadapicanha.com e massama.fabricadapicanha.pt.

---

## 1. Os erros do website (a tua munição)

### Erros graves — usa estes primeiro

1. **O site inteiro é UMA página.** Não existe página de menu, não existem páginas por restaurante (Odivelas, Alverca, Campo de Ourique), nada. Um cliente que pesquisa "menu fábrica da picanha" não encontra nada no site.
2. **Zero preços no site.** O rodízio custa ~20,95€ — um preço competitivo que é o maior argumento de venda deles — e não aparece em lado nenhum. Estão a esconder a própria arma.
3. **Zero horários.** Quem quer jantar às 22h30 não sabe se ainda serve. Vai ligar? Não — vai ao concorrente que tem o horário no Google.
4. **Zero moradas e zero mapa.** Só dizem os nomes das zonas. Sem Google Maps integrado, sem morada completa, sem estacionamento.
5. **Zero fotos de comida.** A homepage carrega literalmente só logótipos (verificado no HTML: as únicas imagens são o logo em 4 tamanhos e favicons). Um restaurante de picanha sem uma única foto de picanha no site.
6. **Quando partilham o site no WhatsApp/Instagram, aparece um logo cinzento** (a og:image é `fabrica-gray.png`, um logo cinza de 1920px) em vez de uma foto suculenta de carne. Cada partilha é uma oportunidade desperdiçada.
7. **fabricadapicanha.com/home/ dá erro 404** — e é este o link que aparece nos resultados do Google. Clientes a cair numa página de erro.
8. **O site de Massamá (nova unidade) é uma landing page vazia** feita noutro sistema (LeadConnectorHQ) — sem morada, sem data de abertura, sem menu, sem reservas. Identidade visual desligada do site principal. Dois "sites" que parecem duas empresas diferentes.
9. **Servidor lento: mais de 1 segundo só para o servidor responder** (TTFB medido: 1,04s). No mobile, com imagens de 265KB só para o logo, a experiência é pesada. Google penaliza isto no ranking.

### Erros técnicos/SEO — para mostrar profundidade

10. **Sem Schema.org de restaurante** (JSON-LD) — o Google não consegue mostrar preços, horários, avaliações nos resultados. Os concorrentes com schema aparecem com estrelas; eles não.
11. **Sem página individual por localização = a perder o SEO local.** "rodízio Odivelas", "rodízio Alverca", "picanha Campo de Ourique" — cada uma destas pesquisas devia ter uma página dedicada. Não têm nenhuma.
12. **Sem avaliações no site** — nenhuma integração com Google Reviews ou TripAdvisor, quando restaurantes vivem de prova social.
13. **Contacto único: WhatsApp.** Sem telefone por unidade, sem email. Cliente de 55 anos que não usa WhatsApp? Perdido.
14. **Copy repetitiva e genérica** — "Por isso", "Além disso", "Ou seja" em série; call-to-action vago ("A tua próxima refeição memorável").
15. **WordPress carregado de plugins** (Elementor + HT Mega + FluentForm + PixelYourSite + widget de acessibilidade) para entregar... uma página com 2 links. Peso máximo, resultado mínimo.
16. **Sem FAQ** — alergias, grupos grandes, aniversários, estacionamento, take-away: tudo perguntas que acabam no telefone deles todos os dias e que o site devia responder.
17. **32 mil seguidores no Instagram a apontar para um site que não converte.** O tráfego existe — a máquina de converter é que não.

### A frase-resumo da auditoria (decora isto)

> "Vocês têm 32 mil seguidores, 3 restaurantes cheios e o melhor preço de rodízio da Grande Lisboa — e o vosso site não tem menu, não tem preços, não tem horários, não tem moradas e não tem uma única foto de picanha. O vosso site é o único empregado da casa que não vende."

---

## 2. A frase para passar o gatekeeper (quem atende o telefone)

**Versão principal:**

> "Boa tarde! Fala [nome]. Preciso de falar com o gerente por causa de um problema que encontrei no site da Fábrica — o link que aparece no Google está a dar erro e estão a perder reservas com isso. É rápido, mas tem de ser com ele. Ele está?"

**Porquê funciona:** não estás a "vender", estás a reportar um problema real (o 404 do fabricadapicanha.com/home/ é verificável em 10 segundos). O gatekeeper não quer ser a pessoa que ignorou um problema que custa dinheiro ao patrão.

**Versão alternativa (mais soft):**

> "Boa tarde! Quem é o responsável pela parte do site e das reservas online? Encontrei uma falha que vos está a custar clientes e queria mostrar-lha antes que mais gente repare. Consegue passar-me a ele, por favor?"

**Se perguntarem "é sobre o quê? diga-me a mim":**

> "Com todo o gosto, mas é técnico e ele vai querer ver com os olhos dele — leva 2 minutos. Diga-lhe só: 'é sobre o erro no site que aparece no Google'. Ele vai querer atender."

---

## 3. O speech para o gerente (estilo Grant Cardone)

### Abertura (10 segundos — capta atenção com o problema, não contigo)

> "Sr. [nome], vou direto ao assunto porque sei que está a gerir três casas cheias. Faça uma coisa por mim agora: pesquise 'Fábrica da Picanha' no Google e clique no segundo resultado. Dá erro 404. Página de erro. É isso que centenas de clientes seus veem por semana."

*(Pausa. Deixa-o processar.)*

### O problema (30 segundos — factos, não opiniões)

> "E fui ver o site principal. Vocês têm o melhor produto da Grande Lisboa — rodízio de picanha a menos de 21 euros, três casas, 32 mil seguidores no Instagram. E o site? Não tem menu. Não tem preços. Não tem horários. Não tem moradas. Não tem UMA foto de picanha — verifiquei o código, as únicas imagens que carregam são o vosso logótipo. Quando alguém partilha o vosso site no WhatsApp, aparece um logo cinzento. Cinzento! Vocês vendem picanha suculenta e a internet mostra cinzento."

### A dor (o custo de não fazer nada)

> "Sr. [nome], quantas mesas vale um cliente que pesquisa 'rodízio Odivelas' às 20h de sábado? Esse cliente hoje não vos encontra — encontra o concorrente que tem horário, preço e fotos no Google. Não é o site que custa dinheiro. É o site que vocês TÊM que custa dinheiro. Todos os dias. Vocês já pagam por um site — só que ele não trabalha."

### A solução (o que vendes)

> "O que eu faço é simples: transformo o vosso site no melhor empregado da casa. Um empregado que trabalha 24 horas, nunca se atrasa, e diz a cada cliente o preço, o horário, a morada e mostra a picanha a sair da grelha. Página por restaurante para dominarem as pesquisas em Odivelas, Alverca e Campo de Ourique. Menu com preços. Reservas a um clique. Avaliações do Google à vista. E quando abrirem Massamá — porque eu vi que vem aí — já está tudo pronto para encher a casa desde o dia um."

### O fecho (assume a venda)

> "Eu não vim vender-lhe um site. Vim recuperar as reservas que está a perder todas as semanas. Uma mesa de 4 pessoas são ~84 euros. Se o site novo trouxer UMA mesa extra por dia, são mais de 2.500 euros por mês, por casa. Três casas. Faça as contas. Quinze minutos, eu mostro-lhe no meu portátil o antes e o depois — quando é melhor para si, terça ou quinta?"

### Respostas a objeções

| Objeção | Resposta |
|---|---|
| "Já temos site." | "Têm um site — não têm uma máquina de reservas. Um site sem menu, preços e horários é um cartão de visita caro. E o vosso ainda por cima dá 404 no Google." |
| "As casas já estão cheias." | "Hoje. E Massamá? Vão abrir uma casa nova com uma landing page vazia? A altura de construir a máquina é ANTES de precisar dela. E casa cheia com reserva online é casa cheia sem telefone a tocar a atrapalhar o serviço." |
| "Não tenho tempo." | "Exato — é por isso que o site tem de responder às perguntas que a sua equipa atende ao telefone o dia todo. Horários, preços, moradas, grupos. Eu tiro-lhe trabalho de cima, não acrescento." |
| "Quanto custa?" | "Menos do que as mesas que perde num fim de semana. Deixe-me mostrar-lhe primeiro o que está partido — se depois de ver não achar que é óbvio, não lhe cobro nem a conversa." |
| "Manda por email." | "Mando, mas email não mostra o 404 ao vivo nem a diferença lado a lado. 15 minutos presenciais valem mais do que 50 emails. Eu vou aí a Odivelas — terça ao final da tarde?" |

---

## 4. Regras de ouro (Cardone mode)

1. **Massive action:** liga, aparece, segue no Instagram, comenta, volta a ligar. Um "não" é só um "ainda não".
2. **Vende o problema antes da solução.** O 404 é o teu cavalo de Troia — é verificável em 10 segundos no telemóvel dele.
3. **Fala em mesas e euros, nunca em "SEO" e "schema".** O gerente conta mesas, não meta tags.
4. **Assume sempre o fecho:** nunca "quer marcar?"— sempre "terça ou quinta?".
5. **Leva o antes/depois no portátil.** Mockup da homepage deles com foto de picanha, preço e botão de reserva. Quem vê, compra.
