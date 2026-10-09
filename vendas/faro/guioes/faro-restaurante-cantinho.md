# Guião de chamada: Cantinho (Faro, Vila Adentro)

- **Lead:** `faro-restaurante-cantinho`
- **Telefone:** 911 013 101 (telemóvel da casa, segundo a ficha Google). Não usar o 965 391 296, que aparece em fontes de 2021 e parece antigo.
- **Morada:** R. do Repouso 6, 8000-169 Faro, junto ao Arco do Repouso (entrada da Vila Adentro).
- **Decisor:** não confirmado. **Pista:** um artigo da MAGG de 20-09-2021 apresenta o **Diogo Ferreira** como "um dos responsáveis" do Cantinho. O artigo tem cinco anos, por isso o nome é uma pista a confirmar e não um facto atual. Perguntar por ele assim: "ainda é ele o responsável?". Nunca dizer que o conheces.
- **Quando ligar:** terça a quinta, das **15:30 às 17:30**, entre o almoço e o jantar. Pela ficha Google o horário é seg–sáb das 10:30 às 23:30, mas não ligar durante o serviço (12:00–15:00 e a partir das 19:00), nem à sexta, nem ao sábado, nem ao domingo (está fechado). Se atenderem com barulho de sala: "Liguei em má hora. A que horas é mais calmo?" e desligar.
- **Objetivo:** enviar o link da demo por WhatsApp **durante a chamada** e marcar 15 min (ao telefone ou no restaurante, às 16:00) com data e hora. O melhor resultado é um "sim" com sinal de 50%.
- **Demo:** `sites/faro-restaurante-cantinho/public/` (PT em `/`, EN em `/en/`). Ainda não está publicada. Antes de ligar, pôr um link de pré-visualização no ar: **[LINK DA DEMO]**. Ter à mão os screenshots `qa/mob-hero.png`, `qa/desk-night-hero.png`, `qa/mob-sec-reservar.png`, `qa/mob-sec-ementa.png` e `qa/mob-en-hero.png`.
- **Nota:** o vendedor também se chama Diogo. Se o decisor for mesmo o Diogo Ferreira, a coincidência ajuda a quebrar o gelo ("Somos dois Diogos"), mas não forçar a piada.

## Factos que podes dizer (verificados)

| Facto | Como dizer |
|---|---|
| Google: **4,5** com **1327 avaliações** (Algarve Atlas, consultado a 2026-10-09) | "Têm 4,5 no Google com mais de 1300 avaliações. Isso é muita gente a falar bem da casa." |
| O botão "website" da ficha Google leva só ao **Facebook** (facebook.com/cantinhodefaro) | "Quem carrega em 'website' na ficha vai parar ao Facebook." |
| A página de Facebook pede login para se ver tudo (aconteceu-nos ao preparar a chamada) | "Eu próprio tentei ver a página sem conta e o Facebook pediu-me para entrar." |
| Morada junto ao Arco do Repouso, Vila Adentro | "Mesmo à porta do Arco do Repouso." |
| Horário Google: seg–sáb 10:30–23:30, domingo fechado | Usar só para confirmar: "No Google está das 10:30 às 23:30, segunda a sábado. Está certo?" |
| Concorrentes com site, verificados a 2026-10-09: **O Coreto** (ocoreto.pt, com ementa online) e **Taberna Portuguesa Decanter** (tabernaportuguesadecanter.pt, com ementa e "Reservar Mesa" pelo TheFork) | "O Coreto e o Decanter, aqui ao lado, já têm site com a ementa. O Decanter até tem reserva online." |
| Pratos e frases dos clientes na demo: vêm da MAGG 2021 e das avaliações Google | "Os pratos que pus são os da MAGG e os que os clientes elogiam nas avaliações. Corrige-se o que estiver desatualizado." |

**NÃO dizer como facto:**
- **Diogo Ferreira como responsável atual.** É uma pista de 2021. Só se pergunta.
- **À do Pinto.** Consta da lista de concorrentes, mas o adopinto.pt devolveu erro (503) quando foi verificado. Não o nomear. Basta o Coreto e o Decanter.
- **"O Coreto tem reservas online".** Não tem: o botão "Reserve" leva à página de contactos. Só o Decanter tem reserva online (TheFork).
- **Preços** de pratos (os da MAGG são de 2021 e não foram usados), prémios, ano de fundação, número de lugares.
- **Obras de artistas algarvios nas paredes** e o email geral.cantinho@gmail.com: não confirmados. Perguntar em vez de afirmar.
- **Se o 911 013 101 tem WhatsApp.** Não sabemos. Perguntar.
- Nada de testemunhos, nada de "outros restaurantes nossos clientes", nada de números de faturação ou de "vai ganhar X reservas".

---

## 1. Passar o porteiro (e confirmar o nome de forma honesta)

Numa casa pequena, quem atende pode ser o próprio dono ou alguém da sala a preparar o jantar. Tem pouco tempo.

> "Boa tarde, é o Diogo. Queria falar com o Diogo Ferreira. Ainda é ele o responsável do Cantinho? É sobre a presença do restaurante no Google."

**Se disserem "sim, é ele" ou "sou eu":** seguir para a Abertura.

**Se disserem "já não está" ou "não conheço":**
> "Obrigado, tinha esse nome de um artigo antigo. Então com quem devo falar? Quem é hoje o responsável?"

Apontar logo o nome certo em `decisores.json` (nome, fonte: "chamada de [data]") e retirar a pista antiga.

**Se perguntarem "da parte de quem?" ou "é sobre o quê?":**
> "Diogo, faço sites para negócios aqui do Algarve. Reparei que o Cantinho tem mais de 1300 avaliações no Google, mas o botão do site leva ao Facebook. Já fiz uma versão de exemplo do site do Cantinho e queria mostrá-la ao responsável. São dois minutos."

- Nunca dizer que é "pessoal", que "ele está à espera da chamada", que é "da MAGG", "do Google" ou "da câmara".
- Se não quiserem dizer o nome: "Sem problema." Não insistir.

**Se o responsável não estiver:**
> "Qual é a melhor hora para o apanhar, entre o almoço e o jantar? ... Posso deixar um link por WhatsApp para ele ver quando tiver um minuto. Este número tem WhatsApp?"

Apontar a hora e voltar a ligar a essa hora, nem antes nem depois.

**Se o porteiro disser "não estamos interessados":** é o primeiro não, mas é do porteiro e não do responsável.
> "Percebo. Só lhe peço uma coisa: posso deixar o link do exemplo para o responsável ver? Se ele não quiser, não volto a ligar."

Se voltarem a dizer que não: agradecer e terminar. Registar `recusa_porteiro` com a data e **não** voltar a ligar antes de 2–3 meses. Se pedirem para não voltar a ligar, marcar `nao_contactar`.

---

## 2. Abertura (até 15 s)

> "Boa tarde, [Sr. Diogo / o senhor é o responsável?]. É o Diogo, faço sites para negócios aqui do Algarve. Liguei por causa da ficha do Cantinho no Google. Tem 30 segundos para eu dizer porque liguei? Se não fizer sentido, desligamos."

Esperar pela resposta. Se disser "diga lá", seguir. Se estiver a receber peixe ou a montar a sala, passar para a objeção "Não tenho tempo".

---

## 3. Gancho (facto + demo)

> "O Cantinho tem 4,5 no Google com mais de 1300 avaliações. Pouca gente em Faro tem isso. Mas quem vê a ficha e carrega em 'website' vai parar ao Facebook, que pede login para ver tudo. Não vê a ementa, não vê se estão abertos, não reserva. O Coreto e o Decanter, aqui ao lado, já têm site com a ementa."
>
> "Por isso fiz uma versão de exemplo do site do Cantinho, em português e inglês. Já está feita, não lhe custa nada ver. Posso mandar-lhe agora o link? Este número tem WhatsApp?"

**Enviar logo** (texto curto: "Cantinho – exemplo do site: [LINK DA DEMO]"). Se ele abrir durante a chamada, mostrar estas 3 coisas por esta ordem:

1. **O arco e o "aberto agora"**: "Logo em cima está o Arco do Repouso. O céu dentro do arco é o céu de Faro agora: de dia é dia, ao pôr do sol fica dourado, à noite fica noite. E por baixo diz se o Cantinho está aberto agora, à hora certa de Portugal, mesmo para um turista com o telemóvel noutro fuso." (Às 16:00 vai estar de dia. Se quiser mostrar a noite, mandar o link com `?ceu=night` ou o screenshot `qa/desk-night-hero.png`.)
2. **As reservas**: "Mais abaixo o cliente escolhe o dia, a hora e quantas pessoas. Vai vendo um talão com o pedido e, quando carrega, sai uma mensagem de WhatsApp já escrita para o vosso número. Não há sistema nem mensalidade. Aos domingos não deixa reservar, porque estão fechados. No telemóvel há uma barra em baixo com Ligar, Ir e Reservar."
3. **A ementa e o mapa**: "A ementa tem os pratos da casa, e ao lado estão as frases dos clientes tal como as escreveram no Google, como 'o famoso banoffee'. Mais em baixo há um mapa desenhado da Vila Adentro para quem vem a pé. E tudo isto existe em inglês: carrega em EN e muda."

Se ele não puder abrir agora: "Fica no WhatsApp. Quando tiver um minuto entre serviços, abra no telemóvel."

---

## 4. Perguntas (é ele que diz qual é o problema)

Fazer 2 ou 3 perguntas, uma de cada vez, e deixá-lo falar.

1. "Hoje as reservas chegam-vos como? Telefone, Facebook, mensagem, ou as pessoas aparecem à porta?"
2. "Quantas vezes por dia toca o telefone a meio do serviço só para perguntar se estão abertos ou se há mesa?"
3. "Os clientes estrangeiros, que são muitos aí na Vila Adentro, como é que vos encontram e como reservam? Em inglês pelo Facebook?"
4. "E no inverno, de novembro a março, a casa enche da mesma forma ou há noites mais calmas?"
5. (Útil para o projeto) "A ementa ainda é parecida com a da MAGG de 2021, com a cataplana e o arroz de marisco? E o horário: o Google diz 10:30 às 23:30. A cozinha fecha a que horas?"

Repetir o que ele disse com as palavras dele antes de passar à proposta: "Então, se percebi bem, ..."

---

## 5. Proposta e preço (dizer com naturalidade)

> "O que proponho é isto: o site do Cantinho como o que viu, com as vossas fotografias, a ementa certa e os preços que quiserem pôr. Em português e inglês. Inclui pôr o Cantinho bem no Google em Faro (o SEO local), pôr o botão 'website' da ficha a apontar para o site em vez do Facebook, a parte legal (RGPD, Livro de Reclamações) e o alojamento do primeiro ano. Fica pronto em cerca de duas semanas."
>
> "Custa 1000 euros. Metade para arrancar e metade na entrega. Se depois quiser que eu mude a ementa ou os preços sempre que precisar, a manutenção fica entre 30 e 50 euros por mês, mas é opcional."

**Âncora no valor** (sem prometer resultados; deixar que seja ele a fazer a conta):
> "Para pôr isto em perspetiva: quanto deixa uma mesa de quatro ao jantar, com vinho? ... Então são umas quantas mesas a mais, ao longo de um ano, e o site está pago. Não lhe garanto quantas reservas vai trazer, ninguém honesto garante. Mas hoje, quem vos encontra no Google e quer ver a ementa ou reservar acaba no Facebook."

Depois de dizer o preço, **calar** e esperar pela resposta.

---

## 6. Fecho (próximo passo concreto, com data)

Escolher conforme a temperatura da conversa:

- **Quente:** "Se gostou, posso começar já. Mando-lhe hoje a proposta com os dados para o sinal. Começo quando receber, e daqui a duas semanas tem o site no ar, a tempo do inverno. Pode ser?"
- **Morno:** "Que tal 15 minutos [terça / quarta] às 16:00? Passo pelo Cantinho, entre o almoço e o jantar, e vemos o exemplo juntos no telemóvel. Que dia lhe dá mais jeito?"
- **Frio mas aberto:** "Veja o link com calma. Ligo-lhe [dia concreto, ter–qui] às [16:00] só para saber o que achou. Combinado?"

Antes de desligar, confirmar sempre: o nome dele (e se é mesmo o responsável), se o número tem WhatsApp, o email (pedir, não ler o que temos) e o dia e hora do próximo contacto.

---

## 7. Objeções

Para cada objeção: **reconhecer → reenquadrar → perguntar.** Contar os "nãos" (ver secção 8).

### Objeção-chave: "Já temos Facebook e a casa está sempre cheia."
> "Acredito. Mais de 1300 avaliações não aparecem numa casa vazia. E não lhe venho dizer que precisa de mais gente no verão."
>
> "Mas há duas coisas. A primeira: com a casa cheia, quem é que atende o telefone a meio do jantar? Com o site, o pedido chega por WhatsApp, por escrito, com o dia, a hora e quantas pessoas. Responde quando tiver as mãos livres. A segunda: o Facebook é bom para quem já vos segue, mas quem vos procura no Google e carrega em 'website' vai parar a uma página que pede login, sem ementa em inglês."
>
> "Pergunto-lhe só: em novembro, numa terça à noite, a sala também está cheia?"

- Se disser "sim, sempre": "Então o que lhe interessa são as reservas arrumadas e menos chamadas durante o serviço. Quer ver como chega a mensagem?"
- Se disser "no inverno é mais calmo": "É aí que conta quem vos encontra no Google. Quer ver o exemplo com calma e falamos [dia] às 16:00?"

### "Não preciso, tenho Facebook/Instagram."
> "Faz sentido, e as redes ajudam a mostrar o dia a dia. Mas o Facebook não é vosso: muda as regras quando quer, pede login a quem não tem conta e não aparece bem no Google quando alguém pesquisa 'restaurante Faro'. O site é o que a ficha do Google aponta, com ementa, horário e reservas, em português e inglês. E o Facebook e o Instagram ficam ligados no site. Qual dos dois é que usam mais?"

### "Já tenho clientes que cheguem / trabalho por recomendação."
> "Acredito. Mas hoje, quando um hotel ou um amigo recomenda o Cantinho, a primeira coisa que a pessoa faz é pesquisar no telemóvel. Encontra 4,5 estrelas e depois cai no Facebook. O site não é para encher a casa, é para não perder quem já vos vinha procurar. Quer ver como fica essa primeira impressão?"

### "É caro." / "Não tenho dinheiro agora."
> "Percebo. 1000 euros é dinheiro, sobretudo num restaurante. Paga-se uma vez, com o alojamento do primeiro ano incluído, e não há mensalidade obrigatória nem comissão por reserva, como nas plataformas. Quantas mesas de quatro é que precisava para compensar?"

Se for mesmo uma questão de tesouraria:
> "Os 50% servem para arrancar e o resto só se paga na entrega. Se for melhor depois do verão ou antes da Páscoa, marco e ligo nessa altura. Que mês lhe dá mais jeito?"

Não baixar o preço logo à primeira. Não inventar descontos que acabam.

### "Envie por email."
> "Envio, claro. Já lhe mandei o link por WhatsApp: é mais rápido abrir no telemóvel. Qual é o email certo? ... E para não ficar perdido, posso ligar-lhe [dia] às 16:00 para saber o que achou?"

Se for uma forma educada de despachar a chamada, fazer o mesmo e ficar com a data marcada. Se ele recusar a data, isso conta como um não.

### "O meu sobrinho faz isso."
> "Ainda bem que tem alguém de confiança. A pergunta é só uma: já o fez? Porque o botão do site ainda leva ao Facebook. Se ele tiver tempo, ótimo. Se não, eu entrego em duas semanas, com o inglês, a parte legal e o Google incluídos, e ele pode até ficar com as atualizações. Quer mostrar-lhe o exemplo e decidirem juntos?"

### "Já tive um site e não serviu para nada."
> "Isso acontece muito: o site fica feito, ninguém o liga ao Google e ninguém o encontra. O que é que esse site tinha? ... Neste caso, a ficha do Google com 1300 avaliações aponta para o site, o site diz se estão abertos e a reserva chega-vos por WhatsApp. Se não servir para isso, tem razão, não serve para nada. Quer ver o exemplo e dizer-me se lhe parece diferente?"

### "Não tenho tempo agora." / "Ligue mais tarde."
> "Claro, um restaurante não para. Mando-lhe o link por WhatsApp e ligo [terça/quarta/quinta] às [15:30 / 16:30]. Qual destas horas é melhor?"

Apontar a hora e cumprir. "Mais tarde" sem hora marcada não conta como próximo passo.

### "Não estou interessado." (seco)
> "Entendido. Só uma pergunta, para não o voltar a incomodar sem razão: é porque não vê valor num site para o Cantinho, ou só porque agora não é altura?"

- Se for "agora não é altura": passar para "Não tenho tempo" e combinar uma data mais à frente.
- Se for "não vejo valor": um reenquadramento curto ("Mando-lhe só o link. Se em 30 segundos não lhe disser nada, apague."). Se disser não outra vez, ir para a saída elegante.

### Extra: "Já estamos no TheFork / TripAdvisor."
> "Essas plataformas trazem gente, e não é para as largar. Mas cobram por reserva e mostram os concorrentes ao lado do Cantinho. No vosso site, a reserva chega direta, sem comissão, e o cliente só vê o Cantinho. Quanto é que pagam hoje por reserva?"

(Só usar se ele mencionar a plataforma. Não sabemos se o Cantinho está em alguma.)

---

## 8. Saída elegante

Se ele disser **não duas vezes** depois de uma tentativa de reenquadrar, ou pedir **para não ser contactado** (seja o responsável ou quem atende em nome da casa):

> "Com certeza. Obrigado pelo seu tempo, Sr. [Nome]. Não volto a ligar. Bom serviço logo à noite."

- Terminar a chamada. Não fazer "só mais uma coisa".
- Não enviar o follow-up se ele pediu para não ser contactado.
- Registar no CRM ou em `decisores.json`: `nao_contactar: true`, a data, quem disse e as palavras exatas. Esta oposição tem de ser respeitada por toda a equipa.
- Se foi "não" sem pedir para não ser contactado: registar `recusou` com a data. Não voltar a ligar antes de 6 meses, no mínimo.

---

## 9. Mensagens de follow-up

**WhatsApp (durante ou logo a seguir à chamada):**
> Boa tarde Sr. [Nome], é o Diogo, falámos agora por telefone.
> Aqui está o exemplo do site do Cantinho: [LINK DA DEMO]
> Abra no telemóvel. O céu dentro do arco é o de Faro à hora a que abrir. Mais abaixo está a reserva que vos chega por WhatsApp, e em cima o botão EN para a versão em inglês.
> Ligo [dia] às [hora], como combinámos. Obrigado.

**Email (se ele o pediu):**
> **Assunto:** Cantinho – exemplo do site (Arco do Repouso, PT/EN)
>
> Boa tarde Sr. [Nome],
>
> Como falámos por telefone, segue o exemplo que preparei para o Cantinho: [LINK DA DEMO]
>
> O que tem de diferente:
> - o Arco do Repouso com o céu de Faro em tempo real, e a indicação de "aberto agora" à hora de Portugal;
> - reservas que chegam por WhatsApp como mensagem já escrita (dia, hora, pessoas), sem sistema nem comissões; recusa domingos; no telemóvel, botões para Ligar, Ir e Reservar;
> - a ementa da casa com as frases dos clientes tal como as escreveram, um mapa desenhado da Vila Adentro e tudo em português e inglês.
>
> Proposta: site à medida por 1000 € (50% de sinal e 50% na entrega), pronto em cerca de 2 semanas. Inclui SEO local, ficha Google com o botão "website" a apontar para o site, versão em inglês, conformidade legal (RGPD, Livro de Reclamações) e alojamento no 1.º ano. Manutenção opcional entre 30 e 50 €/mês.
>
> A ementa, o horário, as fotografias e os textos do exemplo são provisórios e acertam-se consigo.
>
> Ligo-lhe [dia] às [hora]. Se preferir que não volte a contactar, basta responder a dizer isso.
>
> Cumprimentos,
> Diogo
> [telefone]

**Se não houver resposta:** fazer um único contacto extra 3 a 5 dias úteis depois, ter–qui entre as 15:30 e as 17:30. Se mesmo assim não houver resposta, deixar de insistir e registar `sem_resposta`.

---

## Notas pós-chamada (preencher)

- Nome do responsável (o Diogo Ferreira ainda está? sócios?):
- O 911 013 101 tem WhatsApp? Email confirmado:
- Horário real e hora de fecho da cozinha (Google: 10:30–23:30; MAGG 2021: 12:00–22:00):
- Ementa e preços atuais, prato do dia:
- Plataformas usadas (TheFork, TripAdvisor, outras):
- Ainda há obras de artistas algarvios nas paredes? Lugares na sala/esplanada:
- Fotografias disponíveis (porta e arco, sala com lareira, arroz de marisco, polvo, esplanada, banoffee):
- Entidade legal e NIF (para o rodapé e a fatura):
- Próximo passo e data:
- Estado: `reuniao` / `proposta_enviada` / `sinal` / `recusou` / `nao_contactar` / `sem_resposta`
