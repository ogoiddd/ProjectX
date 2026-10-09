# Guião de chamada: Arealauto - Oficina de Reparações, Lda. (Faro)

- **Lead:** `faro-arealauto-oficina`
- **Telefone:** 289 882 080 (fixo da oficina)
- **Morada:** Sítio do Brejo, Areal Gordo, 8005-409 Faro
- **Decisor:** não identificado pelo nome. Pedir pelo **gerente / responsável**. A empresa é uma Lda., por isso pode haver mais de um sócio-gerente.
- **Quando ligar:** de terça a quinta, entre as 10:00 e as 11:30 ou entre as 14:30 e as 16:30. Evitar a abertura (08:30), a hora de almoço (12:30–14:00), o fim do dia e a sexta à tarde. A oficina fecha ao fim de semana: não ligar.
- **Objetivo:** enviar o link da demo por WhatsApp **durante a chamada** e marcar 15 min (por telefone ou na oficina) com data e hora. O melhor resultado é um "sim" com sinal de 50%.
- **Demo:** `sites/faro-arealauto-oficina/public/` (ainda não está publicada). Antes de ligar, pôr um link de pré-visualização no ar: **[LINK DA DEMO]**. Ter também à mão os screenshots `qa/mobile-first.png` e `qa/mobile-folha.png`.

## Factos que podes dizer (verificados)

| Facto | Como dizer |
|---|---|
| Constituída a 14-06-1996, faz 30 anos em 2026 | "Trinta anos de casa este ano." |
| 11 a 15 empregados (Iberinform) | Não dizer o número. Basta "uma casa com equipa". |
| Google: nota **4,4**, **sem fotos e sem website** | "A ficha no Google tem 4,4, mas não tem fotos nem site." |
| Rede de Oficinas Recomendadas da Ocidental (Ageas) | "Vi que estão na rede recomendada da Ocidental." |
| Multimarca | "Oficina multimarca." |
| Horário: seg–sex 08:30–12:30 e 14:00–18:00 (Waze/Google) | Usar só para confirmar: "Continua das 8:30 às 18:00 com pausa para almoço?" |

**NÃO dizer como facto:**
- **TOPCAR.** O Google e o Waze já mostraram "TOPCAR - Arealauto", mas a oficina já não aparece na lista atual da TOPCAR. Isto só se pergunta, e com cuidado (ver Perguntas). Pode ter havido uma saída que custou dinheiro ou foi conflituosa. Não insistir no tema.
- **Número de avaliações.** Não está confirmado.
- **Concorrentes.** Os sites carsandcars.pt e oacc.pt vieram de resultados de pesquisa e não foram abertos. Não os nomear. Dizer só "há oficinas em Faro que já aparecem com site".
- **Email** arealauto@iol.pt: não está confirmado. Pedir o email em vez de o ler.
- Nada de testemunhos, nada de "outros clientes nossos", nada de números de faturação inventados.

---

## 1. Passar o porteiro (e descobrir o nome de forma honesta)

Vai atender a receção, o administrativo ou um mecânico. Estas pessoas filtram as chamadas e têm pouco tempo.

> "Bom dia, é o Diogo. Podia falar com o gerente da Arealauto? É sobre a presença da oficina no Google."

**Se perguntarem "da parte de quem?" ou "é sobre o quê?":**
> "Diogo, faço sites para negócios aqui do Algarve. Reparei que a ficha da oficina no Google não tem site nem fotos. Já fiz uma versão de exemplo do site da Arealauto e queria mostrá-la ao responsável. São dois minutos."

**Para saber o nome** (sem rodeios e sem fingir que já o conhecias):
> "Já agora, com quem devo falar? Qual é o nome do gerente, para eu não estar sempre a dizer 'o responsável'?"

- Se derem o nome, apontar logo em `decisores.json` (nome, fonte: "receção, chamada de [data]") e passar a usá-lo.
- Se não quiserem dizer: "Sem problema." Não insistir. O nome pode ser confirmado mais tarde na certidão permanente do registo comercial (NIPC 503688894), que é pública e paga.
- Nunca dizer que é "pessoal", que "ele está à espera da chamada" ou que "é da seguradora". Também não usar o nome da Ocidental para passar.

**Se o gerente não estiver ou estiver na oficina:**
> "Qual é a melhor hora para o apanhar? ... Posso deixar-lhe um link por WhatsApp para ele ver quando tiver um minuto. Para que número envio?"

Apontar a hora sugerida e voltar a ligar a essa hora, nem antes nem depois.

**Se o porteiro disser "não estamos interessados":** isto conta como o primeiro não, mas é o primeiro não do porteiro e não do gerente.
> "Percebo. Só lhe peço uma coisa: posso deixar o link do exemplo para o gerente ver? Se ele não quiser, não volto a ligar."

Se voltarem a dizer que não: agradecer e terminar. Registar `recusa_porteiro` com a data e **não** voltar a ligar antes de 2–3 meses. Se pedirem para não voltar a ligar, marcar `nao_contactar`.

---

## 2. Abertura (até 15 s)

> "Bom dia [Sr. Nome / o senhor é o gerente?]. É o Diogo, faço sites para negócios aqui do Algarve. Liguei por causa da ficha da Arealauto no Google. Tem 30 segundos para eu dizer porque liguei? Se não fizer sentido, desligamos."

Esperar pela resposta. Se disser "diga lá", seguir. Se estiver com um carro no elevador, passar para a objeção "Não tenho tempo".

---

## 3. Gancho (facto + demo)

> "A oficina tem 30 anos este ano, está na rede recomendada da Ocidental e tem 4,4 no Google. É uma boa reputação. Mas quem pesquisa 'oficina Faro' no telemóvel encontra a ficha sem fotos e sem site. Não fica a saber o que fazem, se estão abertos nem como marcar. Liga a quem aparecer mais completo."
>
> "Por isso fiz uma versão de exemplo do site da Arealauto. Já está feita, não lhe custa nada ver. Posso mandar-lhe agora o link por WhatsApp? Para que número?"

**Enviar logo** (texto curto: "Arealauto – exemplo do site: [LINK DA DEMO]"). Se ele abrir durante a chamada, mostrar estas 3 coisas por esta ordem:

1. **O talão "Hoje na oficina"**: "Logo em cima diz se estão abertos agora ou à hora de almoço, à hora certa de Portugal. No telemóvel há uma barra em baixo com Ligar, Marcar e Ir. O cliente carrega e liga ou abre o GPS."
2. **A folha de obra**: "O cliente preenche no telemóvel o nome, a matrícula (que fica formatada, tipo AA-00-AA), o problema e o dia que prefere. Sai uma mensagem de WhatsApp já escrita para a oficina. Chega-vos o pedido arrumado, sem papelada."
3. **O conta-quilómetros 1996 → 2026 e o selo da Rede Recomendada Ocidental**: "Os 30 anos e a Ocidental aparecem logo. É isso que dá confiança a quem não vos conhece."

Se ele não puder abrir agora: "Fica no WhatsApp. Quando tiver um minuto, abra no telemóvel."

---

## 4. Perguntas (é ele que diz qual é o problema)

Fazer 2 ou 3 perguntas, uma de cada vez, e deixá-lo falar.

1. "Hoje os clientes novos chegam-vos como? Recomendação, seguradora, ou alguém que vos encontrou no Google?"
2. "Quando alguém vos pesquisa ao fim de semana ou à noite, com a oficina fechada, como é que deixa o pedido?"
3. "Quantas chamadas por dia é que a receção atende só para perguntar o horário ou se fazem determinado serviço?"
4. (**Opcional e com tato**, só se a conversa estiver a correr bem) "Vi que o Google e o Waze já vos mostraram como 'TOPCAR - Arealauto'. Isso ainda se mantém ou agora estão por conta própria?"
   - Se estiverem por conta própria: "Então faz ainda mais sentido terem uma montra vossa, que não dependa de uma rede. E convém corrigir o nome na ficha do Google, que eu também trato."
   - Se ele não gostar do assunto: "Era só para saber que nome pôr no site." Mudar logo de tema.
5. (Útil para o projeto) "No Google aparecem como 'serviços de usinagem automotiva'. Fazem retificação ou trabalhos de torno?"

Repetir o que ele disse com as palavras dele antes de passar à proposta: "Então, se percebi bem, ..."

---

## 5. Proposta e preço (dizer com naturalidade)

> "O que proponho é isto: um site à medida da Arealauto, como o que viu, com as vossas fotos e os serviços certos. Inclui pôr a oficina bem no Google em Faro (o SEO local), arranjar a ficha do Google com fotos e o link para o site, a parte legal (RGPD, Livro de Reclamações) e o alojamento do primeiro ano. Fica pronto em cerca de duas semanas."
>
> "Custa 1000 euros. Metade para arrancar e metade na entrega. Se depois quiser que eu trate das atualizações, a manutenção fica entre 30 e 50 euros por mês, mas é opcional."

**Âncora no valor** (sem prometer resultados):
> "Para pôr isto em perspetiva: numa oficina, um cliente novo que faça uma embraiagem ou uma revisão com travões, e que depois volte durante anos, paga uma boa parte do site. Não lhe garanto quantos clientes vai trazer, ninguém honesto garante. Mas hoje quem vos procura no Google não encontra nada para além da morada."

Depois de dizer o preço, **calar** e esperar pela resposta.

---

## 6. Fecho (próximo passo concreto, com data)

Escolher conforme a temperatura da conversa:

- **Quente:** "Se gostou, posso começar já. Mando-lhe hoje a proposta com os dados para o sinal. Começo quando receber, e daqui a duas semanas tem o site no ar. Pode ser?"
- **Morno:** "Que tal 15 minutos [terça às 10:30 / quinta às 15:00]? Passo pela oficina no Areal Gordo, ou falamos por telefone, e vemos o exemplo juntos. Que dia lhe dá mais jeito?"
- **Frio mas aberto:** "Veja o link com calma. Ligo-lhe [dia concreto, ter–qui] às [hora] só para saber o que achou. Combinado?"

Antes de desligar, confirmar sempre: o nome dele, o número de WhatsApp, o email (pedir, não ler o que temos) e o dia e hora do próximo contacto.

---

## 7. Objeções

Para cada objeção: **reconhecer → reenquadrar → perguntar.** Contar os "nãos" (ver secção 8).

### "Não preciso, tenho Facebook/Instagram."
> "Faz sentido, e as redes ajudam. Mas, pelo que vi, a Arealauto não tem página que apareça a quem pesquisa, e quem procura oficina no Google cai na ficha. O site é o que essa ficha aponta, com o horário e a folha de obra. É vosso, não depende de um algoritmo nem de uma rede. Se tiver página, qual é? Posso ligá-la ao site."

### "Já tenho clientes que cheguem / trabalho por recomendação."
> "Acredito. Trinta anos não se fazem sem isso. Mas hoje, quando alguém recomenda a Arealauto, a primeira coisa que a pessoa faz é pesquisar no Google. E encontra uma ficha sem fotos. O site não é para encher a oficina, é para não perder quem já vos vinha procurar. Quer ver como fica essa primeira impressão?"

Variação "não tenho mãos a medir":
> "Ótimo sinal. Nesse caso, o que interessa é a folha de obra: os pedidos chegam por escrito, com a matrícula e o problema, e a receção não fica ao telefone. Faz sentido para vocês?"

### "É caro." / "Não tenho dinheiro agora."
> "Percebo. 1000 euros é dinheiro. Fica pago uma vez, com o alojamento do primeiro ano incluído, e não há mensalidade obrigatória. Comparando com um trabalho médio na oficina, quantos clientes novos é que precisava para compensar?"

Se for mesmo uma questão de tesouraria:
> "Os 50% de sinal servem para arrancar e o resto só se paga na entrega. Se preferir, marcamos para [mês] e eu volto a ligar nessa altura. Que mês lhe dá mais jeito?"

Não baixar o preço logo à primeira. Não inventar descontos que acabam.

### "Envie por email."
> "Envio, claro. Antes disso já lhe mandei o link por WhatsApp: é mais rápido abrir no telemóvel. Qual é o email certo? ... E para não ficar perdido na caixa de correio, posso ligar-lhe [dia] às [hora] para saber o que achou?"

Se for uma forma educada de despachar a chamada, fazer o mesmo e ficar com a data marcada. Se ele recusar a data, isso conta como um não.

### "O meu sobrinho faz isso."
> "Ainda bem que tem alguém de confiança. A pergunta é só uma: já o fez? Porque a ficha continua sem site. Se ele tiver tempo, ótimo. Se não, eu entrego em duas semanas, com a parte legal e o Google incluídos, e ele pode até ficar com a manutenção. Quer mostrar-lhe o exemplo e decidirem juntos?"

### "Já tive um site e não serviu para nada."
> "Isso acontece muito: o site fica feito, ninguém o liga ao Google e ninguém o encontra. O que é que esse site tinha? ... Neste caso, a ficha do Google aponta para o site, o site diz se estão abertos e o cliente manda o pedido por WhatsApp. Se não servir para isso, não serve para nada, tem razão. Quer ver o exemplo e dizer-me se lhe parece diferente?"

### "Não tenho tempo agora." / "Ligue mais tarde."
> "Claro, uma oficina não para. Mando-lhe o link por WhatsApp e ligo [terça/quarta/quinta] às [10:30 / 15:00]. Qual destas horas é melhor?"

Apontar a hora e cumprir. "Mais tarde" sem hora marcada não conta como próximo passo.

### "Não estou interessado." (seco)
> "Entendido. Só uma pergunta, para eu não o voltar a incomodar sem razão: é porque não vê valor num site para a oficina, ou só porque agora não é altura?"

- Se for "agora não é altura": passar para "Não tenho tempo" e combinar uma data mais à frente.
- Se for "não vejo valor": um reenquadramento curto ("Mando-lhe só o link. Se em 30 segundos não lhe disser nada, apague."). Se disser não outra vez, ir para a saída elegante.

### Extra: "Já tenho a seguradora / a rede que me manda trabalho."
> "A Ocidental é uma boa porta, e por isso pus o selo da rede recomendada no site. Mas esses são os clientes que a seguradora vos manda. Os particulares que pesquisam sozinhos não sabem disso, a não ser que o vejam. Quanto do vosso trabalho vem por seguradora e quanto vem de particulares?"

---

## 8. Saída elegante

Se ele disser **não duas vezes** depois de uma tentativa de reenquadrar, ou pedir **para não ser contactado** (seja o gerente ou o porteiro em nome da empresa):

> "Com certeza. Obrigado pelo seu tempo, Sr. [Nome]. Não volto a ligar. Bom trabalho."

- Terminar a chamada. Não fazer "só mais uma coisa".
- Não enviar o follow-up se ele pediu para não ser contactado.
- Registar no CRM ou em `decisores.json`: `nao_contactar: true`, a data, quem disse e as palavras exatas. Esta oposição tem de ser respeitada por toda a equipa.
- Se foi "não" sem pedir para não ser contactado: registar `recusou` com a data. Não voltar a ligar antes de 6 meses, no mínimo.

---

## 9. Mensagens de follow-up

**WhatsApp (durante ou logo a seguir à chamada):**
> Bom dia Sr. [Nome], é o Diogo, falámos agora por telefone.
> Aqui está o exemplo do site da Arealauto: [LINK DA DEMO]
> Abra no telemóvel. Em cima vê se a oficina está aberta e, mais abaixo, a "folha de obra" que o cliente preenche e vos chega por WhatsApp.
> Ligo [dia] às [hora], como combinámos. Obrigado.

**Email (se ele o pediu):**
> **Assunto:** Arealauto – exemplo do site (30 anos, Areal Gordo)
>
> Bom dia Sr. [Nome],
>
> Como falámos por telefone, segue o exemplo que preparei para a Arealauto: [LINK DA DEMO]
>
> O que tem de diferente:
> - diz ao cliente se a oficina está aberta agora, com botões para ligar, marcar e ir;
> - folha de obra no telemóvel, que chega à oficina como mensagem de WhatsApp, com a matrícula formatada;
> - os 30 anos de casa e a Rede de Oficinas Recomendadas da Ocidental à vista.
>
> Proposta: site à medida por 1000 € (50% de sinal e 50% na entrega), pronto em cerca de 2 semanas. Inclui SEO local, ficha Google com fotos e link para o site, conformidade legal (RGPD, Livro de Reclamações) e alojamento no 1.º ano. Manutenção opcional entre 30 e 50 €/mês.
>
> Os serviços, as fotos e os nomes da equipa no exemplo são provisórios e acertam-se consigo.
>
> Ligo-lhe [dia] às [hora]. Se preferir que não volte a contactar, basta responder a dizer isso.
>
> Cumprimentos,
> Diogo
> [telefone]

**Se não houver resposta:** fazer um único contacto extra 3 a 5 dias úteis depois, na hora boa (ter–qui). Se mesmo assim não houver resposta, deixar de insistir e registar `sem_resposta`.

---

## Notas pós-chamada (preencher)

- Nome do gerente / sócios:
- WhatsApp / email confirmados:
- TOPCAR (ainda pertencem à rede? O que dizem):
- Serviços confirmados (revisões, travões, diagnóstico, motor/embraiagem, pré-inspeção, retificação/torno?):
- Outras seguradoras ou acordos:
- Fotos disponíveis (equipa, portão com letreiro, oficina):
- Próximo passo e data:
- Estado: `reuniao` / `proposta_enviada` / `sinal` / `recusou` / `nao_contactar` / `sem_resposta`
