# Cold Outreach Blueprint — resumo e passos

Fonte: "The Cold Outreach Blueprint That Prints Leads" — Jayden Leilua (Velocityflow), YouTube, 1h20, publicado em 14/07/2026.
https://youtu.be/hpp8e7NZsDY

Resumo da transcrição completa (legendas automáticas, inglês). O autor tem uma agência que faz cold email e LinkedIn para empresas B2B nos EUA. Os números e as ferramentas são os dele. A secção final adapta o método ao nosso negócio de websites.

---

## Visão geral: o sistema em 6 blocos

1. **Infraestrutura de email.** Sem ela nada chega à caixa principal.
2. **Construção de listas.** Mercado, segmentos, ICP, scraping, verificação e enriquecimento.
3. **Oferta.** O que o cliente ganha, não o que tu fazes.
4. **Mensagem + vídeo Loom.** Um só vídeo gravado uma vez em vez de vídeos personalizados.
5. **LinkedIn automatizado.**
6. **Respostas e objeções.** O framework ACA e marcar a chamada.

A ideia central do autor: o cold outreach não é magia. É simples quando as peças encaixam e falha quando uma delas está partida.

---

## 1. Infraestrutura (entregabilidade)

O autor diz que o texto do email (assunto, palavras "spam") é cerca de 1% do problema. Os outros 99% são domínios, aquecimento, reputação e registos DNS.

### Passos
1. **Nunca enviar cold email do domínio principal.** As denúncias de spam colam-se ao domínio, e depois as faturas e os emails para clientes também vão parar ao spam.
2. **Criar muitos domínios secundários** parecidos com a marca (ex.: marca-marketing.co, marca-media.co). Ele pede ao ChatGPT nomes com ar profissional, sem cidades aleatórias.
   - Evitar `.info`: diz que foram para a lista negra ainda durante o aquecimento, por serem usados por spammers. Passou para `.co` (cerca de 6–9 $/domínio).
3. **Calcular quanta infraestrutura é precisa** com base no volume mensal pretendido, na taxa de resposta (média ~2%) e na conversão em reunião.
   - Google: 2 caixas por domínio, ~15 emails/dia por caixa (incluindo aquecimento).
   - Microsoft: até 99 caixas por domínio é arriscado. Recomenda ~49.
   - Divisão Google/Outlook de 50/50, ou 70/30 a favor do Google, que ultimamente tem funcionado melhor.
   - Exemplo dele (escala muito grande): 104 mil contactos/mês → 177 domínios, 645 caixas, cerca de 52 reuniões. **Para começar, usar muito menos.**
4. **Comprar os domínios** em massa (Porkbun, pesquisa em bulk de até 100 de cada vez).
5. **Comprar as caixas** num fornecedor (Premium Inboxes, Scaled Mail…) que configura DNS, cria as caixas e liga-as ao sequenciador (Plus Vibe, Smartlead, Instantly). O redirecionamento dos domínios aponta para o site principal. Remetente: o teu nome ou personas.
6. **Aquecimento:** ligar o warm-up e esperar **2 semanas** antes do primeiro envio.
   - Valores de referência no Google: começar em 5/dia e subir 3 por dia até 25. No Outlook, ~6/dia.
7. **Lote A / Lote B:** um lote envia durante 30 dias enquanto o outro aquece. Trocar a cada 30–60 dias.
8. **Verificar a cada ~2 semanas** se os emails chegam à caixa principal (ferramentas de teste de inbox). Abaixo de ~80% o domínio está "queimado" e é altura de trocar de lote.

### As 5 regras dele
1. Nunca enviar do domínio principal.
2. Criar muitos domínios secundários.
3. Caixas separadas por domínio, com o nome da empresa (Google 2–3, Microsoft 49–99).
4. Lote A e lote B.
5. Aquecer 2 semanas.

---

## 2. Construção de listas

### Conceitos
- **TAM** (mercado total endereçável) é toda a gente a quem podes enviar.
- **Segmentar:** nunca enviar o mesmo email a todo o mercado. Iscos diferentes apanham peixes diferentes. Enviar o mesmo email a todos dá pouca resposta e queima a infraestrutura.
- **ICP** (cliente ideal) é um segmento concreto, por exemplo 10–50 empregados, setor X, faturação Y.

### Passos (método manual)
1. **Apollo → separador Companies:** escolher o país.
2. Em vez de filtros de setor, usar **palavras-chave na descrição da empresa**, que deixam escapar menos empresas. Ele pede ao GPT ~50 palavras-chave separadas por vírgulas.
3. Filtrar o **tamanho da empresa** (ex.: 11–50).
4. **Controlo de qualidade:** saltar para a página 100, onde o Apollo começa a ficar menos rigoroso, e abrir alguns sites. Quando aparecem empresas erradas, pedir ao GPT palavras para excluir e colá-las em "exclude keywords". Repetir até a lista estar limpa.
5. **Separador People:** estado do email = verified, unverified, user managed e update required. Cargos de decisão sugeridos pelo GPT. Localização do contacto = localização da empresa.
6. Filtros extra opcionais: tecnologias, faturação, financiamento, **anúncios de emprego / sinais de intenção**.
7. Copiar o URL da pesquisa e fazer o scraping (Ample Leads, ~24h para 10 mil).
8. **Verificar os emails** no Million Verifier (~15 min). Dos ~9.500 só ~5.000 eram válidos. Muitos bounces destroem a infraestrutura.
9. **Enriquecer no Clay:**
   - Normalizar o nome da empresa (tirar "LLC", "Inc." para soar humano).
   - "Agente de confirmação de ICP": a IA vê o site e escreve "yes" se a empresa encaixa e nada se não encaixa, o que facilita filtrar.
   - Coluna de personalização: o case study principal do cliente ou, em alternativa, o serviço principal. Usa-se numa frase do tipo "se eu te arranjar 15+ prospects à procura de [serviço] nos próximos 30 dias, interessa?".
10. Exportar o CSV e carregá-lo no sequenciador.

### Versão automatizada com Claude Code (substitui o Clay)
- Motivo: os créditos do Clay chegam aos milhares de $/mês a escala. Com Claude Code (plano de 20 $) faz o mesmo mais barato e, segundo ele, com melhor qualidade.
- Criou uma skill de "pipeline de lead gen" que capta o ICP, faz scraping (AI Ark), filtra, verifica (Million Verifier), personaliza e exporta CSV.
- Pede-se em linguagem natural, por exemplo: "50 empresas de recrutamento nos EUA, 1–10 empregados, fundadores/CEOs/donos".
- Pede **3x mais leads** do que o objetivo (150 para ficar com 50) porque se perdem na verificação e no filtro de ICP.
- Usar o modo automático para não ter de aprovar cada passo. A skill corrige os próprios erros.
- Pedidos de seguimento: limpar nomes de empresa e criar a coluna "case study principal, ou serviço principal como alternativa". Demorou cerca de 2 minutos para 50 leads.

---

## 3. Oferta

### O que é uma oferta
- **Não é o serviço** ("temos uma agência de leads"). É **o que o cliente fica a ter** ("10–15 chamadas qualificadas na agenda por mês").
- Vende-se a praia, não o aeroporto.

### 4 perguntas que a oferta tem de responder
1. **Resultado:** que mudança de estado o comprador obtém? Tem de ser um estado, não uma entrega.
2. **Mecanismo:** porque é que a tua abordagem funciona e as outras não?
3. **Inversão de risco:** o que acontece se não funcionar? Tem de estar dentro da oferta, sobretudo com tráfego frio.
4. **Forma de pagamento:** pagamento único, setup, avença, por performance ou híbrido.

O comprador cético pensa em três coisas: a promessa, a garantia e a prova. **A prova (case study) vale sempre mais do que a garantia**, e as duas juntas são o ideal.

### Escada do "para que"
Partir da entrega e perguntar "para quê?" até chegar ao valor final. Exemplo: um processo de onboarding → clientes obtêm valor mais cedo → menos cancelamentos nos primeiros 90 dias → contratos mais longos. Vende-se o último degrau.

### Captar procura vs. gerar procura
| | Captar procura | Gerar procura |
|---|---|---|
| Quem | Já quer e anda à procura | Tem o problema mas não sabe que precisa de ti |
| O teu trabalho | Ser a opção mais credível | Mudar a crença antes de vender |
| Volume / conversão | Baixo / alta | Alto / baixa |
| Texto | Problema → solução, curto | Pergunta sobre a dor e educação, um pouco mais longo |

### Equação de valor (Hormozi)
Valor = (Resultado desejado × Probabilidade percebida) / (Tempo de espera × Esforço e sacrifício)
- O resultado desejado quase nunca é o problema. **A probabilidade percebida é o problema 9 em cada 10 vezes.** Sobe-se com case studies, prova social e garantias.

### Como escrever uma garantia condicional
1. Resultado mensurável (ex.: 10–15 chamadas qualificadas).
2. Prazo (por mês).
3. Consequência concreta (dinheiro de volta, ou trabalhamos de graça).
4. Condições mínimas exigidas ao cliente. Quanto menos lhe pedires, melhor: os donos de negócio têm dinheiro, não tempo.

### Oferta de entrada (front-end offer) para tráfego frio
Algo gratuito e pequeno que resolve uma parte do problema grande **e que te custa tempo ou recursos reais**:
| Não funciona | Funciona |
|---|---|
| Guia grátis | **Auditoria grátis da situação concreta** (ex.: velocidade do site e quanto mais rápido podia ser) |
| Webinar gravado | Sessão de estratégia ao vivo |
| PDF de checklist, cada vez mais feitos com IA | Amostra de trabalho sobre o ativo real do cliente |
| Consulta genérica | Diagnóstico com conclusões por escrito |

Uma oferta fraca é "ajudamos empresas a crescer". Uma forte é "garantimos 50 reuniões em 30 dias ou não paga".

### Estrutura da mensagem
1. **Linha 1, gancho relevante:** uma pergunta sobre a dor, que mostre que conheces o mundo dele.
2. **Linhas 2–3:** o resultado concreto.
3. **Linha 4:** a prova ou o mecanismo, numa linha (não explicar o processo).
4. **Linha 5:** inversão de risco e um pedido de baixa fricção, do tipo "valeria a pena conversar?". **Nunca** "tem 15 minutos esta semana?", que é como pedir em casamento no primeiro encontro.

Se a oferta não cabe numa frase, ainda não é uma oferta.

### Scorecard de 7 eixos (a nota mais baixa é o que te está a custar vendas)
1. Embalagem e diferenciação (pessoa, problema e mecanismo com nome)
2. Economia e margem
3. Escalabilidade (fica mais barato com volume?)
4. Poder de mercado (consegues subir o preço?)
5. Força do mecanismo (explica porque os outros falharam)
6. Volume de prova: **vender um produto a um só avatar** para acumular case studies do mesmo setor
7. Garantia (condicional e credível?)

---

## 4. O vídeo Loom único

- Os Loom personalizados funcionam, mas não escalam: são ~3 min por lead (gravar, cortar, carregar), o que dá ~16h para 1.000 leads, e o ganho é marginal.
- A confiança vem de **mostrares que sabes do que falas**, não de abrires o LinkedIn da pessoa. Deve funcionar como um VSL.
- **Um único vídeo**, gravado uma vez e enviado só a quem responde com interesse.

### Email que leva ao vídeo (curto, como uma mensagem a um amigo)
O formato é: [Nome], preparei um vídeo de 2 minutos a mostrar a estratégia que usámos para o cliente X chegar ao resultado Y. Posso enviar?
- A pessoa só tem de responder "sim". Ele diz que ~90% dos que respondem abrem o vídeo e chegam à chamada já "quentes".

### Guião do vídeo (1–2 min) em 2 partes
1. **Desarmar:** reconhecer o formato ("achei mais fácil explicar num vídeo do que por email"). Tom casual e humano.
2. **Prova:** porque te devem ouvir e o que já fizeste (o resultado de um cliente e como foi conseguido). Depois:
   - quem és, numa frase;
   - porque és diferente;
   - o convite: "auditoria **cortesia**" (diz que "grátis" aumenta a desconfiança): o que se analisa e o que é realista, sem pressão;
   - urgência: "só estamos a fazer isto para poucos negócios agora";
   - CTA: "responde a este email e marcamos".

A mudança de mentalidade é **escalar a autoridade, não a personalização**.

---

## 5. LinkedIn automatizado (ferramenta: Aimfox, ~50 $/mês por conta, 7 dias grátis)

1. Ligar a conta do LinkedIn (extensão do Chrome ou login).
2. Definir limites semanais (os dele, com a conta já aquecida: 200 pedidos de ligação, 150 mensagens, 150 InMails). Contas novas devem ligar o aquecimento.
3. Criar a campanha:
   - outbound (ligações de 2.º e 3.º grau) ou inbound (as tuas ligações atuais);
   - fontes: pesquisa do LinkedIn, Sales Navigator integrado, participantes de eventos, quem interagiu com posts, grupos, CSV;
   - excluir quem já foi contactado e **quem não tem foto de perfil**.
4. Filtros: cargo (fundador/co-fundador), dimensão da empresa (1–10), país, setor, idioma do perfil e **"publicou no LinkedIn recentemente"** (pessoas ativas).
5. Sequência:
   - pedido de ligação (as notas exigem LinkedIn Premium: a conta grátis só tem 5 notas/mês);
   - ver o perfil antes de ligar e reagir a um post ~2h depois;
   - mensagens de seguimento quando a ligação é aceite (há modelos e IA, por exemplo para dar os parabéns por uma conquista);
   - retirar o pedido se não for aceite em 7 dias;
   - testes A/B e tradução automática.
6. Horário: 9h–19h no fuso do prospect, sem domingos.
7. Integração com o Slack para responder rapidamente.

---

## 6. Respostas e objeções

### Framework ACA (para todas as respostas com interesse)
**Acknowledge, Context, Ask:** reconhecer, dar contexto e fazer uma pergunta.
- "Quanto cobram?" → "Boa pergunta. Depende do tamanho e da velocidade a que querem crescer. Estaria aberto a uma conversa rápida esta semana para ver se faz sentido?"
- "Já trabalharam com alguém do meu setor?" → "Boa pergunta. Sim, com um negócio parecido com o seu. Posso enviar?"

### Marcar a chamada (o mínimo de fricção possível)
- **Não enviar só o link do calendário.** Segundo ele, cerca de metade nunca chega a marcar ("as pessoas são preguiçosas").
- Propor **duas horas concretas** ("quarta às 14h ou quinta às 15h?") e acrescentar o link do calendário como alternativa.
- Quando escolhem uma hora, **és tu que envias o convite** ("já enviei o convite, pode aceitar?").

### Rapidez
- Responder a cada resposta com interesse em **15–30 minutos**.
- Ainda melhor: **ligar nos primeiros 5 minutos** (o número costuma estar na assinatura). Não é uma cold call, porque a pessoa acabou de responder.

### Objeções ("acho que não é para mim")
- É difícil tratá-las por email, por isso é melhor ao telefone.
- Usar o mesmo ACA: "É justo." → voltar à oferta de entrada e à inversão de risco ("só paga as reuniões que marcarmos") → "Estaria aberto a ver se funciona no seu caso?"

---

## Como aplicar ao nosso negócio (sites ≥1000€ para negócios locais sem site)

Atenção: o vídeo é sobre **B2B nos EUA em volume muito alto**. O nosso caso é diferente: negócios locais em Portugal, muitos sem email profissional, e um volume baixo. O que transfere bem:

1. **Oferta (a parte mais valiosa para nós):**
   - Resultado em vez de entrega. Não "fazemos websites", mas algo como "clientes novos que o encontram no Google e reservam online, sem depender só do Instagram".
   - **A oferta de entrada já é a nossa demo personalizada** (agente frontend-designer). É exatamente uma "amostra de trabalho sobre o ativo real do cliente", que o vídeo aponta como o que funciona com tráfego frio.
   - Definir uma **garantia condicional** (ex.: "se o site não estiver online em X dias, não paga a última prestação") e a forma de pagamento (sinal + resto, ou sinal + avença de manutenção).
   - **Um avatar de cada vez** (ex.: restaurantes em Faro) para acumular case studies do mesmo setor.
2. **Guiões (agente cold-call-writer):** aplicar o ACA a cada objeção, propor duas horas concretas para a reunião, ligar depressa a quem responde e usar um pedido de baixa fricção ("posso mostrar-lhe?").
3. **Vídeo único:** gravar um vídeo de 1–2 min (desarmar → prova → convite) para enviar a quem mostra interesse, em vez de explicar tudo por mensagem.
4. **Listas (agentes business-finder e owner-finder):** segmentar por setor, confirmar o ICP com IA a partir da presença online (sem site = ICP) e pedir ~3x mais leads do que o objetivo.
5. **Se fizermos cold email:** nunca do domínio principal, usar domínios secundários aquecidos 2 semanas, verificar emails antes de enviar e manter volumes pequenos.
6. **Legal:** ver com o agente backend-maker as regras de comunicações não solicitadas em Portugal e o RGPD antes de qualquer envio em massa por email ou LinkedIn. As regras dos EUA seguidas no vídeo não se aplicam cá.
