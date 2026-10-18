# Cold email para vender websites (≥1000€): plano para análise

Data: 2026-10-18 · Estado: **rascunho para aprovação**. Nada é enviado antes de o aprovares.

O plano junta o canal de email à operação que já temos (`cabecilha` + 5 agentes, demos personalizadas, guiões de chamada, pagamento só na entrega). O email **não substitui** a chamada. Serve para gerar respostas "sim, mostre-me", e a venda fecha-se numa conversa.

---

## 0. Resumo em 6 linhas

1. **Quem:** só **sociedades** (Lda, Unipessoal Lda, SA) sem site ou com site fraco, num **setor de cada vez**. Os empresários em nome individual ficam fora do email por razões legais (§1) e são trabalhados por telefone.
2. **Método:** *demo-first*. Primeiro um email curto e sem links: "fiz uma maquete do vosso site, posso enviar?". Depois a demo com um vídeo de 90 s, uma chamada de 20 min e uma proposta com 3 pacotes. O cliente não paga nada adiantado: paga 100% no fim, quando aprovar o site. Os preços incluem IVA.
3. **Envio automático:** domínios secundários aquecidos, 6 caixas e um sequenciador. Os agentes preparam a lista e a personalização, e tu aprovas cada campanha.
4. **Medição:** a métrica principal é **receita por 100 emails entregues**, com o funil completo registado por campanha e por variante.
5. **Otimização:** ciclos de 2 semanas, **uma variável de cada vez** e um registo de experiências. Um agente `analista-conversao` lê os resultados e propõe o próximo teste.
6. **Primeiro passo:** decidir o nome, os preços, o setor-piloto e a ferramenta (§9). Daí até ao primeiro envio são cerca de 3 semanas, por causa do aquecimento dos domínios.

---

## 1. Enquadramento legal (isto define a quem se pode escrever)

> Ainda não é um parecer jurídico. Antes do primeiro envio, o agente `backend-maker` (ou um advogado) deve confirmar o texto consolidado da Lei 41/2004 no Diário da República e qual é a entidade que gere a lista de oposição.

| Regra | O que implica para nós |
|---|---|
| **Lei 41/2004, art. 13.º-A** (alterada pela Lei 46/2012): marketing direto por email a **pessoas singulares** exige **consentimento prévio e expresso**. | Não há cold email para **empresários em nome individual** nem para o email pessoal do dono, que são o canal **telefone/presencial** (guiões existentes). |
| Para **pessoas coletivas** o envio é permitido, mas têm direito de oposição e existe uma **lista nacional de oposição** (art. 13.º-B) que tem de ser consultada. | Antes de cada campanha, cruzamos a lista com a lista de oposição. O business-finder regista `tipo_entidade` (confirmado pela denominação social/NIF) e `elegivel_email`. |
| **RGPD art. 14**: quando os dados não foram recolhidos junto do titular, é preciso dizer **de onde vêm** e como se opor. | Todos os emails levam um rodapé com a identificação da empresa (nome, NIF, morada), a origem do contacto ("email público na vossa ficha Google") e uma linha de saída ("Para não receber mais emails, responda SAIR."). Não se usa "responda 'não'", porque os pedidos são feitos para que o "não" signifique avançar (ver `vendas/conhecimento/psicologia-venda.md`). |
| Só email **genérico da empresa** (geral@, info@, reservas@), nunca nominativo inferido. | O agente não "adivinha" emails do tipo nome.apelido@. |
| Quem disser não, sai para sempre. | Uma lista de supressão global (`vendas/email/supressao.csv`) é verificada pelo agente antes de qualquer exportação. |

**Consequência prática:** o universo de email é mais pequeno do que o de telefone (muitos negócios sem site também não têm email). O plano assume entre **100 e 400 leads elegíveis por mês**, por isso a qualidade tem de pesar mais do que o volume.

---

## 2. O método high-ticket (porque o vamos usar)

Vender 1.000–3.000€ a um dono de negócio por email frio não acontece num só email. O que funciona neste ticket é **reduzir o risco percebido em cada passo** e **mostrar antes de pedir**:

```
Email curto (sem links)  →  "Sim"  →  Demo + vídeo 90s + 2 horários  →  Chamada 20 min  →  Proposta 3 pacotes  →  100% na entrega
   pedir licença             resposta     prova no ativo real                 diagnóstico       ancoragem               inversão de risco
```

Peças do método (vêm do `vendas/conhecimento/cold-outreach-blueprint.md`, adaptadas). As regras de preço e de objeções estão em **`vendas/conhecimento/psicologia-venda.md`**, de uso obrigatório em tudo o que o cliente lê ou ouve:

1. **Vender o resultado, não o site.** Falar de "pedidos de orçamento sem pagar comissão à Zaask", "reservas diretas sem depender da Booking", "pacientes que o encontram no Google", e não de "fazemos websites".
2. **Oferta de entrada = maquete com o nome, fotos e serviços deles** (já a fazemos). É uma amostra de trabalho sobre o ativo real, o que mais converte com tráfego frio.
3. **Primeiro email sem links nem imagens**, para proteger a entregabilidade. O primeiro "sim" é o micro-compromisso que importa.
4. **Contas de retorno na chamada.** Por exemplo: "uma obra de remodelação dá ~3.000€ de margem, o site paga-se com um cliente".
5. **Proposta com 3 pacotes (ancoragem).** Apresentada do mais caro para o mais barato, e o do meio é o que queremos vender. Os preços são precisos e aparecem sem "€" nem ponto ("1890", não "1.890€"). Os preços **incluem IVA** ("1890, já com IVA"). A moeda aparece uma única vez, numa linha de condições no fim. Ver §9.
6. **Inversão de risco total:** nada adiantado, **100% na entrega**, quando o cliente aprovar o site. No email aparece como "não paga nada até o site estar pronto e aprovado por si". É o argumento mais forte contra o "não" de risco e de preço.
   - **Proteções (recomendadas):** acordo de 1 página aceite por escrito (email serve) antes de começar; o site fica numa pré-visualização nossa e só passa para o domínio do cliente depois do pagamento; pagamento no dia da entrega, ou até 8 dias depois; no máximo 2 rondas de alterações incluídas.
7. **Contornar o "não":** perguntas feitas para que o "não" signifique avançar ("Seria descabido enviar-lhe a maquete?"), "mas é livre de recusar" e uma resposta preparada para cada um dos 5 tipos de "não" (valor, preço, risco, tempo, pessoa). Nunca com urgência falsa nem factos inventados.
8. **Rapidez:** responder a um "sim" em **menos de 15 min** em horário de trabalho, e ligar se houver número.
9. **Um setor de cada vez**, para acumular casos de estudo do mesmo nicho. Cada venda torna-se prova social no email seguinte do mesmo setor.

### Setores por ordem de prioridade (ticket × dor × facilidade em ter email)

| # | Setor | Ângulo do resultado | Ticket provável |
|---|---|---|---|
| 1 | Construção / remodelações / piscinas (já temos leads no Algarve) | Deixar de pagar comissão por pedido nas plataformas e ter um portefólio de obras | 1.500–2.500€ |
| 2 | Clínicas (dentária, fisio, estética, veterinária) | Marcações online e confiança antes da 1.ª consulta | 1.500–3.000€ |
| 3 | Alojamento local / turismo rural | Reservas diretas sem 15–18% de comissão | 1.500–3.000€ |
| 4 | Oficinas / stands | Pedidos de orçamento e marca própria | 1.000–1.500€ |
| 5 | Restauração | Reservas, menu multilíngue, turistas | 1.000–1.500€ (fecha pior) |

---

## 3. Infraestrutura de envio

| Peça | Escolha proposta | Notas |
|---|---|---|
| Domínio principal | `<marca>.pt` | Fica com o site e o portefólio. **Nunca envia cold email.** |
| Domínios de envio | 3 domínios parecidos (ex.: `<marca>studio.pt`, `use<marca>.pt`, `<marca>-web.pt`) | Redirecionam para o principal. Evitar `.info`. |
| Caixas | 2 por domínio = **6 caixas** (Google Workspace) | Remetente com nome real (ex.: "Diogo da <Marca>"). |
| DNS | SPF, DKIM, DMARC (`p=none` → `quarantine`), domínio de tracking próprio | |
| Aquecimento | **2–3 semanas** antes do 1.º envio, sempre ligado | Começar em 5/dia e subir até ~20/dia por caixa. |
| Sequenciador | **lemlist** (empresa da UE, bom para RGPD) ou **Instantly** (mais barato) | Ver decisão em §9. Mais tarde pode ser substituído por um envio próprio (Gmail API) ligado ao repositório. |
| Verificação | MillionVerifier ou ZeroBounce antes de cada envio | Bounce **< 2%** ou a campanha é pausada. |
| Tracking | **Aberturas desligadas** e só rastreio de respostas | O pixel prejudica a entregabilidade e a Apple falseia as aberturas. A métrica é a resposta. |
| Teste de inbox | A cada 2 semanas (glockapps ou similar) | Abaixo de ~80% em inbox, o domínio descansa e entra outro. |

**Capacidade:** 6 caixas × 20/dia ≈ 120 emails/dia, muito mais do que o universo elegível. Começamos com **20–40 novos contactos/dia** e o resto da capacidade vai para follow-ups.

**Custo aproximado:** domínios ~40€/ano, Workspace ~45€/mês, sequenciador ~40–100€/mês, verificação ~10€/mês. Total de **~100–150€/mês**, que se paga com 10% de uma venda.

---

## 4. Pipeline automatizado com os nossos agentes

```
business-finder ─► owner-finder ─► [NOVO] email-writer ─► revisão humana ─► sequenciador ─► respostas
     (leads)        (decisor)      (1.ª linha + variante)    (aprovar CSV)      (envia)          │
                                                                                                 ▼
 frontend-designer ◄──────────── "sim" ◄─────────────────────────────────────────────── classificar resposta
  (demo em 24–48h)                                                                               │
        │                                                                                        ▼
 cold-call-writer ─► chamada 20 min ─► proposta ─► venda          [NOVO] analista-conversao ◄─ resultados.csv
```

### Alterações aos agentes existentes
- **business-finder:** campos novos `email_empresa` (só genérico e público, com fonte), `tipo_entidade` (`sociedade` | `eni` | `desconhecido`), `elegivel_email` (bool) e `setor_normalizado`.
- **frontend-designer:** dois modos. **"demo prévia"** para os leads de topo (a maquete está feita antes do email) e **"demo a pedido"** para quem respondeu "sim" (entrega em ≤48h). Os dois modos são uma experiência em si (§6).

### Agentes novos (a criar depois de aprovado)
- **`email-writer`**: para cada lead elegível, escolhe a sequência e a variante, escreve **uma linha de personalização verificável** (ex.: "vi que têm 86 avaliações de 4,8 na Zaask mas nenhum sítio onde mostrar as obras") e exporta `campanhas/<id>/envio.csv`. Não inventa factos e cita a fonte de cada linha.
- **`analista-conversao`**: lê `resultados.csv`, calcula o funil por campanha, variante e setor, compara com as metas, escreve `campanhas/<id>/analise.md` e propõe **uma** próxima experiência.

### Estrutura de pastas
```
vendas/email/
  plano.md                 ← este ficheiro
  marca.md                 ← nome, tom, assinatura, rodapé legal
  emails/01..15-*.md       ← os 15 emails (depois da aprovação)
  supressao.csv            ← quem disse não / lista de oposição
  experiencias.md          ← registo de todas as experiências e decisões
  campanhas/<AAAA-MM>-<setor>-<id>/
    envio.csv              ← leads + variante + personalização
    resultados.csv         ← um evento por linha (ver §5)
    analise.md
```

### Regra humana mantida
Os agentes preparam e **tu aprovas** cada `envio.csv` antes de carregar no sequenciador, tal como já acontece com as chamadas. As respostas também são lidas e respondidas por uma pessoa: os agentes só classificam e sugerem a resposta.

---

## 5. Métricas: o que vamos medir

### Funil (um evento por linha em `resultados.csv`)
`lead_id, campanha, variante, setor, data, evento, valor`
com `evento` ∈ `enviado | bounce | resposta_positiva | resposta_neutra | resposta_negativa | opt_out | reuniao_marcada | reuniao_feita | proposta | venda | perdido`.

| Etapa | Fórmula | Meta inicial* | Alerta |
|---|---|---|---|
| Entregabilidade | 1 − bounces/enviados | ≥ 98% | < 97%: pausar |
| Taxa de resposta | respostas / entregues | ≥ 6% | < 3% |
| **Resposta positiva** | positivas / entregues | ≥ 3% | < 1,5% |
| Opt-out / queixa | opt-out / entregues | < 2% / < 0,1% | acima disso: rever segmento |
| Positiva → reunião marcada | | ≥ 50% | < 35% |
| Comparência | feitas / marcadas | ≥ 75% | < 60% |
| Reunião → venda | vendas / reuniões feitas | ≥ 25% | < 15% |
| Ticket médio | receita / vendas | ≥ 1.500€ | < 1.100€ |
| Ciclo de venda | dias do 1.º email até à venda | ≤ 21 dias | > 45 |
| **⭐ Receita por 100 entregues** | receita / entregues × 100 | ≥ 300€ | < 100€ |

\* *As metas são hipóteses de partida para um nicho local e personalizado, não dados do mercado. O analista recalibra-as com os nossos números ao fim de ~500 envios.*

**Conta de exemplo (hipótese):** 500 entregues → 15 positivas (3%) → 8 reuniões → 6 feitas → 1–2 vendas × 1.500€ ≈ **1.500–3.000€/mês** com ~150€ de custo de ferramentas.

### Árvore de diagnóstico (onde mexer quando a métrica cai)
| Sintoma | Causa provável | Primeira coisa a testar |
|---|---|---|
| Poucas respostas de qualquer tipo | Entregabilidade ou segmento | Teste de inbox → trocar setor/subsegmento |
| Respostas, mas sobretudo negativas | Oferta pouco relevante | Ângulo do resultado, prova do setor |
| Positivas que não marcam | Fricção na marcação | 2 horários + ligação imediata, vídeo antes |
| Marcam e faltam | Pouco compromisso | Lembrete no dia anterior + WhatsApp 1h antes |
| Reuniões sem venda | Preço, valor ou demo | Contas de retorno, pacotes, qualidade da demo |
| Ticket baixo | Âncora fraca | Ordem e preço dos pacotes |

---

## 6. Ciclo de otimização da conversão

**Ritmo:** análise **semanal** (5 min de leitura do `analise.md`) e decisão **quinzenal**.

**Regras para não nos enganarmos com amostras pequenas:**
1. **Uma variável de cada vez**, com 2 variantes por campanha (A/B) e leads distribuídos aleatoriamente dentro do mesmo setor.
2. A decisão faz-se sobre a **resposta positiva**, que é o sinal rápido. As vendas são poucas demais para decidir testes. Ficam como validação ao fim de cada trimestre.
3. Mínimo de **~150 entregues por variante** antes de decidir. Só se declara vencedor quando a diferença é **≥ 1,5×** e se mantém em 2 semanas seguidas. Se não houver diferença clara, fica a variante mais simples ou mais barata.
4. O vencedor passa a **controlo** e o próximo teste desafia-o.
5. Tudo fica escrito em `experiencias.md`: hipótese → variantes → n → resultado → decisão → aprendizagem.

**Lista de experiências (por impacto esperado):**

| # | Variável | A | B |
|---|---|---|---|
| 1 | **Setor/segmento** | Remodelações | Clínicas |
| 2 | **Oferta de entrada** | Demo já feita ("já fiz") | Demo a pedido ("posso fazer?") |
| 3 | CTA | "Posso enviar?" | "Seria descabido enviar-lhe?" (orientado para o "não") |
| 4 | Ângulo | Perder dinheiro (comissões) | Ganhar clientes (Google) |
| 5 | Prova | Sem caso | Caso do mesmo setor (após a 1.ª venda) |
| 6 | Tratamento | Formal (o senhor / a empresa) | Próximo (primeiro nome) |
| 7 | Assunto | Nome do negócio | Pergunta curta |
| 8 | Nº de follow-ups | 3 | 5 |
| 9 | Dia/hora | Ter–Qui 9h | Ter–Qui 14h30 |
| 10 | Pacotes | Âncora 2890 | Âncora 3890 |
| 11 | Formato do preço | 1.890€ | 1890 |
| 12 | Frase de liberdade | sem | "mas é livre de recusar" |

Mais testes de preço e de objeções: §4 de `vendas/conhecimento/psicologia-venda.md`.

**Como o analista adapta a estratégia:** em cada análise identifica **a etapa do funil com o maior desvio negativo** face à meta (pela árvore em §5) e propõe o teste dessa etapa, mesmo que não seja o próximo da lista. Mexe-se primeiro no estrangulamento.

---

## 7. Nome da empresa (proposta, escolhe tu)

Critérios: português de Portugal, curto, que um dono de restaurante ou de uma empresa de obras entenda à primeira, ligado ao resultado (ser visto e escolhido) e não à tecnologia.

| Nome | Ideia | Prós | Contras |
|---|---|---|---|
| **Montra** ⭐ | "A montra do seu negócio, aberta 24 horas." | Muito PT-PT, imagem imediata, 6 letras | É uma palavra comum, por isso o `.pt` exato deve estar ocupado (usar `montra.studio`, `somosmontra.pt`). É preciso verificar o INPI |
| Fachada | A primeira impressão de quem passa | Forte para construção e comércio | Em sentido figurado pode soar a "só aparência" |
| Balcão | Onde o cliente é atendido e compra | Sugere vendas e marcações | Soa um pouco a banca ou repartição |
| Alpendre | Lugar de boas-vindas, casa portuguesa | Distinto e quente | Pouco claro sobre o que fazemos |
| Rossio | Praça central onde toda a gente passa | Português e memorável | Conotação forte com Lisboa |

**Recomendação: Montra.** Assinatura: *"Montra — sites que trazem clientes a negócios portugueses."* Antes de fechar o nome é preciso verificar a disponibilidade do domínio, o INPI (marca) e o RNPC (firma/denominação).

---

## 8. Mapa dos 15 emails (escritos depois de aprovares este plano)

Todos são texto simples, com **< 90 palavras**, sem links nem imagens no primeiro contacto, levam uma linha personalizada com fonte e o rodapé legal de §1. Seguem `psicologia-venda.md`: os preços aparecem sem "€" nem ponto, os CTA são orientados para o "não" e levam a frase de liberdade.

**Sequência A, "Demo já feita"** (leads de topo, a maquete existe antes do envio)
1. **A1 Abertura:** "Fiz uma versão do site da [Negócio], posso enviar-lhe?" (dia 0)
2. **A2 Ângulo do custo:** o que estão a pagar hoje (comissões, clientes perdidos) (dia 3)
3. **A3 Mini-caso / contas:** "um cliente paga o site" (dia 7)
4. **A4 Despedida:** "fecho o assunto, a maquete fica guardada 30 dias" (dia 14)

**Sequência B, "Demo a pedido"** (restantes leads elegíveis)
5. **B1 Abertura:** pergunta sobre a dor e "posso preparar-lhe uma maquete sem compromisso?" (dia 0)
6. **B2 Concorrência:** "os 3 primeiros no Google em [cidade] para [serviço] têm site" (dia 3)
7. **B3 Inversão de risco:** não paga nada até o site estar pronto e aprovado por si (dia 7)
8. **B4 Despedida** (dia 14)

**Aberturas por setor** (substituem A1/B1 no setor certo)
9. **Construção/remodelações:** comissões das plataformas vs. um portefólio próprio
10. **Clínicas:** marcações online e confiança antes da 1.ª consulta
11. **Alojamento/turismo:** reservas diretas sem 15–18% de comissão
12. **Restauração:** reservas, menu multilíngue e informação certa no Google

**Depois da resposta** (enviados por uma pessoa e pré-escritos)
13. **Entrega da demo:** link + vídeo de 90 s + **2 horários concretos** + link de calendário como alternativa
14. **Depois da reunião:** proposta com 3 pacotes, resumo do que ouvimos e próximo passo com data
15. **Reativação (60–90 dias)** de quem disse "agora não", com uma novidade (caso novo do setor)

Cada email traz no topo: **objetivo**, **variável que testa**, **assunto A/B** e **campos de personalização**.

---

## 9. Decisões que preciso de ti

1. **Nome:** Montra ou outro da lista (ou uma sugestão tua)?
2. **Pacotes e preços** (proposta, apresentada ao cliente do mais caro para o mais barato: *Completo* 2890 · *Profissional* 1890 ⭐ · *Essencial* 1190, mais manutenção de 39 · 59 · 79 por mês). A base atual da operação é 1000. **IVA incluído** (decidido).
3. **Setor-piloto:** remodelações no Algarve (já temos leads) ou clínicas?
4. **Ferramenta:** lemlist (UE) ou Instantly (mais barato)?
5. **Remetente:** "Diogo" (como nos guiões) ou outro nome?
6. **Orçamento mensal** de ferramentas: ~100–150€ está bem?

## 10. Calendário

| Semana | O quê |
|---|---|
| 0 | Decisões de §9, verificação legal, compra dos domínios e das caixas, DNS |
| 1–2 | Aquecimento · business-finder com os campos novos (300 leads → ~150 elegíveis) · escrita dos 15 emails · criação do `email-writer` e do `analista-conversao` · vídeo de 90 s |
| 3 | **Campanha piloto 1**: setor-piloto, Sequência A vs. B, ~150 leads por variante, 20–40/dia |
| 4 | 1.ª análise semanal e primeiras reuniões |
| 5 | **Decisão 1** (vencedor A/B) → campanha 2 (2.º setor ou experiência #3) |
| 6+ | Ciclos de 2 semanas e revisão trimestral com vendas reais |
