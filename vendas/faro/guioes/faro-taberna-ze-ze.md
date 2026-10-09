# Guião de chamada: Taberna Zé-Zé (Faro)

- **Lead:** `faro-taberna-ze-ze`
- **Telefone:** 938 735 167 (o da ficha Google). É um telemóvel e pode ser o número pessoal do dono, por isso convém ser ainda mais curto e respeitoso.
- **Outros números** (vêm da página DISH/Makro e não estão confirmados): 910 344 728 ("reservas") e 289 825 056 (fixo). Não ligar para eles à primeira. Só servem para a pergunta sobre o horário e os contactos (ver Gancho).
- **Morada:** Travessa do Alportel 15, 8000-448 Faro, junto ao Largo do Carmo.
- **Decisor:** não identificado. Pedir pelo **responsável / dono**. Uma única review fala num "Eldu" e o Wanderlog fala numa "Palmira". São fontes fracas: **não usar estes nomes na chamada** nem dizer "o senhor Eldu está?". O nome descobre-se perguntando (ver secção 1).
- **Quando ligar:** de terça a quinta, entre as 16:00 e as 17:30. O horário real é incerto (ver abaixo), por isso:
  - **Hipótese A, só jantares (Google: seg–sáb 18–23):** às 16:00 a casa está fechada ou a preparar o jantar. Se atender alguém, é provavelmente o dono, que pode estar fora da taberna. Perguntar logo "Apanho-o numa boa altura?".
  - **Hipótese B, almoço e jantar (DISH: 12–15 e 18–01):** às 16:00 acabou o almoço e há uma pausa até ao jantar. É a melhor janela. Não ligar antes das 15:30.
  - Em qualquer caso: **nunca depois das 17:30** (preparação do jantar), nunca à hora de almoço, nunca à noite, nem ao fim de semana. Evitar a segunda-feira (uma fonte diz que fecham à segunda).
- **Objetivo:** mandar o link da demo por WhatsApp **durante a chamada** e marcar 15 minutos na taberna (antes do jantar, a uma hora que ele escolha) ou por telefone, com dia e hora. O melhor resultado é um "sim" com sinal de 50%.
- **Demo:** `sites/faro-taberna-ze-ze/public/` (ainda não está publicada). Antes de ligar, pôr um link de pré-visualização no ar: **[LINK DA DEMO]**. Ter também à mão os screenshots `qa/mob-hero.png`, `qa/mob-comanda-filled.png`, `qa/mob-en-hero.png` e `qa/mob-map.png`.

## Factos que podes dizer (verificados)

| Facto | Como dizer |
|---|---|
| Google: **4,7** com cerca de **963 opiniões** (Algarve Atlas, 09-10-2026; o Wanderlog já mostrava 976) | "Têm 4,7 no Google com quase mil opiniões." Dizer "quase mil", não um número exato. |
| Junto ao Largo do Carmo, a uns 70 m da Igreja do Carmo / Capela dos Ossos | "Mesmo ao lado do Carmo, onde passam os turistas da Capela dos Ossos." |
| Conhecidos pelas cataplanas e arrozes para dois | "As cataplanas são o que as pessoas mais falam nas opiniões." |
| Há uma página automática DISH/Makro: `tabernaze-ze.makro.rest` | "Vi que têm uma página na plataforma da Makro." |
| A página DISH diz seg–sáb 12–15 e 18–01. O Google diz seg–sáb 18–23, domingo fechado | **Só como pergunta:** "Qual é o horário certo?" |
| A página DISH tem 910 344 728 e 289 825 056. O Google tem 938 735 167 | **Só como pergunta:** "Para reservas, qual é o número que querem que as pessoas usem?" |
| A página DISH não mostra preços | Só se vier a propósito. Não criticar a página. |
| Convém reservar, a sala é pequena (Wanderlog, Airial) | "Pelo que se lê, a sala é pequena e convém reservar." |

**NÃO dizer como facto:**
- **Nomes de pessoas** ("Eldu", "Palmira"). Não estão confirmados.
- **Que o Google está errado** ou que a Makro está errada. Não sabemos qual dos dois está certo. É sempre uma pergunta.
- **Concorrentes.** Há tabernas em Faro com site próprio, mas não nomear nenhuma. Dizer só "há casas aqui em Faro que já recebem pedidos de mesa pelo site".
- **Se o 938 tem WhatsApp.** Não sabemos. Perguntar.
- **Email** taberna-barzeze@hotmail.com: está na página DISH mas não está confirmado. Pedir o email em vez de o ler.
- **Pagamento, ar condicionado, take-away, eventos privados.** É texto de modelo da DISH. Não usar.
- Nada de testemunhos, nada de "outros clientes nossos", nada de números de faturação, de clientes perdidos ou de turistas inventados.

---

## 1. Passar o porteiro (e descobrir o nome de forma honesta)

Numa casa de família, quem atende é muitas vezes o próprio dono ou alguém da família. Pode estar a fazer compras ou a preparar a cozinha.

> "Boa tarde, é o Diogo. Queria falar com o responsável da Taberna Zé-Zé. É sobre as reservas e a informação da casa na internet. Apanho-o numa boa altura?"

**Se perguntarem "da parte de quem?" ou "é sobre o quê?":**
> "Diogo, faço sites para negócios aqui do Algarve. Reparei que a taberna aparece com horários e telefones diferentes no Google e na página da Makro. Já fiz uma versão de exemplo de um site para a Zé-Zé e queria mostrá-la ao responsável. São dois minutos."

**Para saber o nome** (sem rodeios e sem fingir que já o conhecias):
> "Já agora, com quem estou a falar?" ou "Qual é o nome do responsável, para eu não estar sempre a dizer 'o dono'?"

- Se derem o nome, apontar logo em `decisores.json` (nome, fonte: "chamada de [data]") e passar a usá-lo.
- Se não quiserem dizer: "Sem problema." Não insistir.
- Nunca dizer que é "pessoal", que "ele está à espera da chamada", que é "da Makro" ou "do Google". Não somos nem da Makro nem do Google, e se perguntarem diz-se isso claramente.

**Se o responsável não estiver:**
> "Qual é a melhor hora para o apanhar, antes do serviço? ... Posso deixar-lhe um link por WhatsApp para ele ver quando tiver um minuto. Para que número envio?"

Apontar a hora sugerida e voltar a ligar a essa hora, nem antes nem depois (e nunca dentro do serviço).

**Se o porteiro disser "não estamos interessados":** conta como o primeiro não, mas é o primeiro não do porteiro e não do dono.
> "Percebo. Só lhe peço uma coisa: posso deixar o link do exemplo para o responsável ver? Se ele não quiser, não volto a ligar."

Se voltarem a dizer que não: agradecer e terminar. Registar `recusa_porteiro` com a data e **não** voltar a ligar antes de 2–3 meses. Se pedirem para não voltar a ligar, marcar `nao_contactar`.

---

## 2. Abertura (até 15 s)

> "Boa tarde [Sr./Sra. Nome / é o responsável?]. É o Diogo, faço sites para negócios aqui do Algarve. Liguei por causa da informação da Taberna Zé-Zé na internet. Tem 30 segundos para eu dizer porque liguei? Se não fizer sentido, desligamos."

Esperar pela resposta. Se disser "diga lá", seguir. Se estiver a chegar o peixe ou a preparar a sala, passar logo para a objeção "Não tenho tempo".

---

## 3. Gancho (pergunta sobre o horário + demo)

> "Têm 4,7 no Google com quase mil opiniões, ali ao pé do Carmo. Quem passa pela Capela dos Ossos e pesquisa onde jantar encontra-vos. Mas eu fui ver e fiquei com uma dúvida: o Google diz que abrem de segunda a sábado das 18 às 23. A página da Makro diz que também abrem ao almoço, das 12 às 15, e que fecham à uma da manhã. E tem outros telefones. Qual é o horário certo?"

**Deixar responder.** Depois, conforme a resposta:

- **Se o certo for o do Google (só jantares):**
  > "Então quem vê a página da Makro pode aparecer ao meio-dia e encontrar a porta fechada, ou ligar para um número que já não usam. E não sabemos quantos desistem antes de ligar."
- **Se o certo for o da Makro (almoço e jantar):**
  > "Então o Google está a dizer a toda a gente que ao almoço estão fechados. Quem procura onde almoçar ao pé do Carmo nem sequer vos vê como opção."
- **Se for outro horário, ou se ele não souber o que diz cada um:**
  > "Então neste momento há duas versões na internet e nenhuma está certa. Isso resolve-se."

Depois, nos três casos:
> "E há outra coisa: numa sala pequena que enche, não há forma de pedir mesa sem ser a ligar. Por isso fiz uma versão de exemplo do site da Zé-Zé. Já está feita, não lhe custa nada ver. Posso mandar-lhe agora o link por WhatsApp? Para que número?"

**Enviar logo** (texto curto: "Taberna Zé-Zé – exemplo do site: [LINK DA DEMO]"). Se ele abrir durante a chamada, mostrar estas 3 coisas por esta ordem:

1. **"Pedir mesa" em 3 toques:** "Carregue em 'Pedir mesa', em baixo. O cliente escolhe o dia, as pessoas e a hora. O domingo aparece riscado e as horas que já passaram ficam bloqueadas, por isso ninguém pede mesa para quando estão fechados. No fim sai uma mensagem já escrita, que segue por WhatsApp ou SMS. Vocês confirmam quando tiverem um minuto, sem atender o telefone a meio do serviço. E se for um turista a usar o site em inglês, a mensagem chega com a tradução em português."
2. **A ementa com "Juntar ao pedido de mesa":** "As cataplanas e os arrozes estão lá com os ingredientes tal como estão na vossa página da Makro. O cliente pode carregar em 'Juntar ao pedido de mesa' e a mensagem diz logo 'queremos uma cataplana de marisco para dois'. Assim a cozinha fica a saber antes de a pessoa chegar."
3. **"Aberto agora", o mapa e as opiniões:** "Logo em cima diz se estão abertos agora, à hora certa. Há um mapa desenhado com a Igreja do Carmo e a Capela dos Ossos, para o turista dar com a Travessa do Alportel. E há cinco opiniões verdadeiras do Google, copiadas tal como os clientes as escreveram."

Se ele não puder abrir agora: "Fica no WhatsApp. Quando tiver um minuto, abra no telemóvel."

**Nota:** o exemplo usa o horário do Google. Se ele disser que o horário é outro, responder: "É só uma linha. Corrijo e fica certo em todo o lado: no site, no Google e na página da Makro."

---

## 4. Perguntas (é ele que diz qual é o problema)

Fazer 2 ou 3 perguntas, uma de cada vez, e deixá-lo falar.

1. "Hoje as reservas chegam-vos como? Por telefone, por mensagem, ou as pessoas aparecem à porta?"
2. "Quantas vezes por noite é que o telefone toca a meio do serviço, para pedir mesa ou perguntar se estão abertos?"
3. "Têm muitos estrangeiros? Como é que fazem quando ligam em inglês?"
4. "E o número das reservas: é o 938 ou o 910? Algum deles tem WhatsApp?" (útil para o projeto)
5. (Só se for o caso) "A página da Makro foram vocês que a pediram, ou veio com o cartão Makro? Ainda lá mexem?"

Repetir o que ele disse com as palavras dele antes de passar à proposta: "Então, se percebi bem, ..."

---

## 5. Proposta e preço (dizer com naturalidade)

> "O que proponho é isto: um site à medida da Zé-Zé, como o que viu, com as vossas fotos e a ementa certa, em português e em inglês. Fica com o pedido de mesa por WhatsApp. Eu corrijo a ficha do Google e ponho o horário e o telefone certos em todo o lado, também na página da Makro se me der acesso. Inclui pôr a taberna bem no Google em Faro (o SEO local), a parte legal (RGPD, Livro de Reclamações) e o alojamento do primeiro ano. Fica pronto em cerca de duas semanas."
>
> "Custa 1000 euros. Metade para arrancar e metade na entrega. Se depois quiser que eu trate das atualizações, como mudar a ementa ou os preços, a manutenção fica entre 30 e 50 euros por mês, mas é opcional."

**Âncora no valor** (sem prometer resultados):
> "Para pôr isto em perspetiva: uma mesa de quatro que pede duas cataplanas, e que vem mais umas vezes por ano, ou que traz amigos, já paga uma boa parte do site. Não lhe garanto quantas mesas vai trazer, ninguém honesto garante. Mas hoje há duas versões do vosso horário na internet, e isso só pode fazer perder clientes, nunca ganhar."

Depois de dizer o preço, **calar** e esperar pela resposta.

---

## 6. Fecho (próximo passo concreto, com data)

Escolher conforme a temperatura da conversa:

- **Quente:** "Se gostou, posso começar já. Mando-lhe hoje a proposta com os dados para o sinal. Começo quando receber, e daqui a duas semanas tem o site no ar, a tempo de pôr o horário de inverno certo. Pode ser?"
- **Morno:** "Que tal 15 minutos [terça / quinta] às [16:30]? Passo pela taberna antes do jantar, ou falamos por telefone, e vemos o exemplo juntos. Que dia lhe dá mais jeito?"
- **Frio mas aberto:** "Veja o link com calma. Ligo-lhe [dia concreto, ter–qui] às [16:00–17:00] só para saber o que achou. Combinado?"

Antes de desligar, confirmar sempre: o nome dele, o número de WhatsApp, o email (pedir, não ler o que temos), o horário certo da casa e o dia e hora do próximo contacto.

---

## 7. Objeções

Para cada objeção: **reconhecer → reenquadrar → perguntar.** Contar os "nãos" (ver secção 8).

### Chave: "Já temos a página da Makro."
> "Tem razão, e não é má ideia ter essa página. Mas é um modelo automático da plataforma: não tem preços, e o horário e os telefones não batem com o Google. O cliente vê as duas e não sabe em qual acreditar. O site é vosso, o Google aponta para lá e tem o pedido de mesa. A página da Makro pode ficar, e eu ponho-a igual. Quer ver a diferença no telemóvel?"

### Chave: "A casa enche." / "Não preciso de mais clientes."
> "Acredito, com 4,7 e quase mil opiniões. Mas o site não é para encher a casa. É para três coisas: o telefone não tocar a meio do serviço, o pedido chegar escrito com o dia, as pessoas e até a cataplana, e ninguém aparecer à hora errada por causa de um horário trocado. E no inverno também enche todas as noites?"

Se ele disser que sim, que enche o ano todo:
> "Ótimo sinal. Então o que interessa é organizar os pedidos e acertar a informação. Faz sentido para vocês receber as mesas por mensagem em vez de ao telefone?"

### "Não preciso, tenho Facebook/Instagram."
> "Faz sentido, e as redes ajudam. Mas quem está no Carmo e pesquisa 'onde jantar em Faro' cai no Google e não no Facebook. Hoje o Google não tem para onde apontar, e a página da Makro diz outra coisa. O site é vosso e não depende de um algoritmo. Ligo o Facebook ao site, claro. Qual é a página que usam?"

### "Já tenho clientes que cheguem / trabalho por recomendação."
> "Acredito. Quase mil opiniões não se fazem sem isso. Mas hoje, quando alguém recomenda a Zé-Zé, a primeira coisa que a pessoa faz é pesquisar. E encontra dois horários diferentes. O site não é para trazer gente nova, é para não perder quem já vos vinha procurar. Quer ver como fica essa primeira impressão?"

### "É caro." / "Não tenho dinheiro agora."
> "Percebo. 1000 euros é dinheiro. Paga-se uma vez, com o alojamento do primeiro ano incluído, e não há mensalidade obrigatória nem comissão por reserva. Quantas mesas a mais por mês é que precisava para compensar?"

Se for mesmo uma questão de tesouraria (por exemplo, no fim da época):
> "Os 50% de sinal servem para arrancar e o resto só se paga na entrega. Se preferir, marcamos para [mês] e eu volto a ligar nessa altura, antes da próxima época. Que mês lhe dá mais jeito?"

Não baixar o preço logo à primeira. Não inventar descontos que acabam.

### "Envie por email."
> "Envio, claro. Antes disso já lhe mandei o link por WhatsApp: é mais rápido abrir no telemóvel. Qual é o email certo? ... E para não ficar perdido na caixa de correio, posso ligar-lhe [dia] às [hora, antes do jantar] para saber o que achou?"

Se for uma forma educada de despachar a chamada, fazer o mesmo e ficar com a data marcada. Se ele recusar a data, isso conta como um não.

### "O meu sobrinho / filho faz isso."
> "Ainda bem que tem alguém de confiança. A pergunta é só uma: já o fez? Porque o Google e a Makro continuam a dizer horários diferentes. Se ele tiver tempo, ótimo. Se não, eu entrego em duas semanas, com o Google, o inglês e a parte legal incluídos, e ele pode até ficar com a manutenção. Quer mostrar-lhe o exemplo e decidirem juntos?"

### "Já tive um site e não serviu para nada."
> "Isso acontece muito: o site fica feito, ninguém o liga ao Google e ninguém o encontra. O que é que esse site tinha? ... Neste caso, o Google aponta para o site, o site diz se estão abertos e o cliente pede mesa por WhatsApp. Se não servir para isso, não serve para nada, tem razão. Quer ver o exemplo e dizer-me se lhe parece diferente?"

### "Não quero reservas online, depois não aparecem."
> "É uma preocupação justa. Por isso o exemplo não reserva sozinho: manda um pedido e são vocês que confirmam. Ficam com o nome e o número da pessoa, por escrito. Como é que fazem hoje quando alguém marca e não aparece?"

### "Não tenho tempo agora." / "Ligue mais tarde."
> "Claro, está a preparar o serviço. Mando-lhe o link por WhatsApp e ligo [terça/quarta/quinta] às [16:00 / 17:00]. Qual destas horas é melhor?"

Apontar a hora e cumprir. "Mais tarde" sem hora marcada não conta como próximo passo.

### "Não estou interessado." (seco)
> "Entendido. Só uma pergunta, para eu não o voltar a incomodar sem razão: é porque não vê valor num site para a taberna, ou só porque agora não é altura?"

- Se for "agora não é altura": passar para "Não tenho tempo" e combinar uma data mais à frente.
- Se for "não vejo valor": um reenquadramento curto ("Mando-lhe só o link. Se em 30 segundos não lhe disser nada, apague."). Se disser não outra vez, ir para a saída elegante.
- Em qualquer caso, se a conversa o permitir: "Só para ficar a saber, o horário certo é o do Google?" Se ele responder, apontar. Não usar como desculpa para continuar a vender.

---

## 8. Saída elegante

Se ele disser **não duas vezes** depois de uma tentativa de reenquadrar, ou pedir **para não ser contactado** (seja o dono ou quem atende em nome da casa):

> "Com certeza. Obrigado pelo seu tempo. Não volto a ligar. Bom serviço logo à noite."

- Terminar a chamada. Não fazer "só mais uma coisa".
- Não enviar o follow-up se ele pediu para não ser contactado.
- Não ligar depois para os outros números (910 / 289) para tentar outra pessoa. A oposição vale para a casa.
- Registar no CRM ou em `decisores.json`: `nao_contactar: true`, a data, quem disse e as palavras exatas. Esta oposição tem de ser respeitada por toda a equipa.
- Se foi "não" sem pedir para não ser contactado: registar `recusou` com a data. Não voltar a ligar antes de 6 meses, no mínimo.

---

## 9. Mensagens de follow-up

**WhatsApp (durante ou logo a seguir à chamada):**
> Boa tarde [Sr./Sra. Nome], é o Diogo, falámos agora por telefone.
> Aqui está o exemplo do site da Taberna Zé-Zé: [LINK DA DEMO]
> Abra no telemóvel e carregue em "Pedir mesa", em baixo. Em 3 toques sai uma mensagem já escrita para vocês. Experimente também em inglês.
> O horário no exemplo é o do Google. Se o certo for outro, corrijo.
> Ligo [dia] às [hora], como combinámos. Obrigado.

**Email (se ele o pediu):**
> **Assunto:** Taberna Zé-Zé – exemplo do site (pedir mesa em 3 toques)
>
> Boa tarde [Sr./Sra. Nome],
>
> Como falámos por telefone, segue o exemplo que preparei para a Taberna Zé-Zé: [LINK DA DEMO]
>
> O que tem de diferente:
> - "Pedir mesa" em 3 toques: o domingo e as horas passadas ficam bloqueados e sai uma mensagem pronta por WhatsApp ou SMS. Se o cliente usar o site em inglês, a mensagem chega com tradução em português;
> - ementa de cataplanas e arrozes com o botão "Juntar ao pedido de mesa";
> - "aberto agora", um mapa com a Igreja do Carmo e a Capela dos Ossos, e cinco opiniões reais do Google.
>
> Hoje o Google e a página da Makro mostram horários e telefones diferentes. No projeto, fica tudo igual em todo o lado.
>
> Proposta: site à medida em português e inglês por 1000 € (50% de sinal e 50% na entrega), pronto em cerca de 2 semanas. Inclui SEO local, correção da ficha Google e da informação contraditória, conformidade legal (RGPD, Livro de Reclamações) e alojamento no 1.º ano. Manutenção opcional entre 30 e 50 €/mês.
>
> Os preços, as fotos e o horário no exemplo são provisórios e acertam-se consigo.
>
> Ligo-lhe [dia] às [hora]. Se preferir que não volte a contactar, basta responder a dizer isso.
>
> Cumprimentos,
> Diogo
> [telefone]

**Se não houver resposta:** fazer um único contacto extra 3 a 5 dias úteis depois, na hora boa (ter–qui, 16:00–17:30). Se mesmo assim não houver resposta, deixar de insistir e registar `sem_resposta`.

---

## Notas pós-chamada (preencher)

- Nome do dono / responsável (e se "Eldu" ou "Palmira" fazem sentido, só se ele o disser):
- Horário certo (almoço? que dia fecham? hora de fecho?):
- Número para reservas (938 / 910 / 289) e se tem WhatsApp:
- Email confirmado:
- Página DISH/Makro: quem a gere, têm acesso?
- Horas em que aceitam reservas:
- Preços da ementa e pratos que faltam:
- Fotos disponíveis (cataplana na mesa, porta da Travessa, sala):
- Nome legal e NIPC (para o rodapé e o Livro de Reclamações):
- Próximo passo e data:
- Estado: `reuniao` / `proposta_enviada` / `sinal` / `recusou` / `nao_contactar` / `sem_resposta`
