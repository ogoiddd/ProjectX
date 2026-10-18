# Zarpa: cold email para clínicas

Data: 2026-10-18 · Estado: **v2, decisões tomadas, por aprovar antes do 1.º envio**. Nada é enviado sem a tua aprovação.

O email junta-se à operação que já temos (`cabecilha` + agentes, demos personalizadas, guiões de chamada). O email **não fecha a venda**: gera um "sim, mostre-me", e a venda fecha-se numa conversa com o Diogo Martins.

---

## 0. Resumo

| | Decisão |
|---|---|
| **Marca** | **Zarpa** (`zarpa.pt`). Ver `marca.md` |
| **Remetente** | Diogo Martins |
| **Setor-piloto** | **Clínicas** (dentária, fisioterapia, estética, veterinária) |
| **Preços** | **a partir de 910**, IVA incluído: Completo 2490 · Profissional 1490 ⭐ · Essencial 910 |
| **Pagamento** | Nada adiantado. 100% na entrega, quando o cliente aprovar o site |
| **Leads** | AI Ark + "quick and rich"(?) + Get Leads → **MillionVerifier** → visita a cada site → **icebreaker** personalizado |
| **Envio** | Sequenciador: **Smartlead** (recomendado), Plus Vibe, Instantly ou EmailBison |
| **Métrica principal** | Receita por 100 emails entregues |

---

## 1. Enquadramento legal

> Ainda não é um parecer jurídico. Antes do 1.º envio é preciso confirmar o texto consolidado da Lei 41/2004 no Diário da República e qual é a entidade que gere a lista de oposição.

| Regra | O que implica |
|---|---|
| **Lei 41/2004, art. 13.º-A**: email de marketing a **pessoas singulares** exige consentimento prévio. | Fora do email: **médicos, fisioterapeutas e outros em nome individual** e endereços pessoais que não sejam o contacto publicado do negócio. Esses leads vão para o canal telefone. |
| Às **pessoas coletivas** pode enviar-se, mas há direito de oposição e uma **lista nacional de oposição** (art. 13.º-B). | Só **sociedades** (Lda, Unipessoal Lda, SA), confirmadas pela denominação social/NIF. Antes de cada campanha, cruzamos com a lista de oposição. |
| Endereços permitidos | O email **publicado pela clínica** como contacto (mesmo que seja um gmail) ou um email **no domínio da clínica**, incluindo o nominativo do sócio-gerente ou do diretor clínico. Nunca emails "adivinhados" que o MillionVerifier não valide. |
| **RGPD art. 14**: dizer de onde vêm os dados e como se opor. | Todos os emails levam o rodapé de `marca.md`, com a origem do contacto, a identificação da Zarpa e "responda SAIR". |
| **Supressão** | Quem responder SAIR ou "não me contacte" vai para `supressao.csv` e nunca mais é contactado, em nenhum canal. |
| Publicidade em saúde | Não afeta os emails, mas sim o **conteúdo dos sites** das clínicas (sem promessas de resultados nem antes/depois enganosos). Fica a cargo do `backend-maker`. |

---

## 2. Oferta e método high-ticket

```
Email curto + icebreaker  →  "Sim"  →  Maquete + vídeo 90s + 2 horários  →  Chamada 20 min  →  Proposta 3 pacotes  →  100% na entrega
   pedir licença               resposta      prova no ativo real                 diagnóstico        ancoragem             risco zero
```

Regras de preço e de objeções: **`vendas/conhecimento/psicologia-venda.md`** (obrigatório). Em resumo:
- preços **sem "€" nem ponto**, precisos e com IVA incluído;
- pacotes apresentados **do mais caro para o mais barato**;
- o preço **nunca aparece** antes de verem a maquete;
- CTA orientado para o "não" ("Seria descabido…?") com a frase de liberdade ("se não fizer sentido, é só dizer").

### Pacotes (conteúdo a confirmar)
| Pacote | Preço (IVA incl.) | Para quem | Inclui |
|---|---|---|---|
| **Completo** | 2490 | Clínicas com várias especialidades ou médicos | Tudo do Profissional + **marcação online em tempo real** (integração com a agenda que usam, ou sistema próprio) + PT/EN + 3 meses de manutenção |
| **Profissional** ⭐ | 1490 | A maioria | Até 6 páginas (especialidades, equipa, acordos/seguros, contactos), **pedido de marcação online**, SEO local, ficha Google otimizada, avaliações à vista |
| **Essencial** | 910 | Pequenos consultórios | 1 página: serviços, horário, mapa, ligar/WhatsApp num toque, ficha Google ligada ao site |

Todos incluem a parte legal (RGPD, cookies, Livro de Reclamações, RAL), alojamento no 1.º ano e entrega em cerca de 14 dias. A manutenção é opcional: 39 · 59 · 79 por mês.

**Pagamento:** nada adiantado, 100% na entrega aprovada. Proteções: acordo de 1 página aceite por email antes de começar; o site fica na nossa pré-visualização até ao pagamento; pagamento até 8 dias após a entrega; 2 rondas de alterações incluídas.

### ICP: que clínicas
| Situação | Ângulo | Exemplo de icebreaker |
|---|---|---|
| **Sem site** (só ficha Google, Facebook ou Instagram) | "Quem pesquisa não vos encontra" | "Vi que a Clínica X tem 4,8 em 212 avaliações no Google, mas o botão 'website' leva ao Facebook." |
| **Site fraco** (não funciona no telemóvel, lento, sem HTTPS, sem marcação, desatualizado) | "Tem site, mas não converte" | "Abri o site da Clínica X no telemóvel e o botão de marcação fica fora do ecrã." |
| Site bom | **Excluir** | — |

Sub-nichos por ordem: **dentária** (ticket alto, tratamentos caros) → **fisioterapia** → **estética** → **veterinária**.

---

## 3. Pipeline de leads (automático)

```
 1. SCRAPE            2. ENRIQUECER          3. VERIFICAR           4. FILTRO LEGAL        5. VISITAR SITE        6. EXPORTAR
 AI Ark               todos os contactos     MillionVerifier        sociedade? oposição?   + icebreaker           sequenciador
 quick and rich(?)    email, telefone,       (emails)               supressão?             (agente)               (API/CSV)
 Get Leads            decisor, site, NIF     libphonenumber (tel)                                                 ↓ aprovação humana
```

### Passo a passo
1. **Scrape** (sem Apollo). Pedimos **3× o objetivo** (ex.: 450 para ficarem ~150), porque muitos caem na verificação e no filtro legal.
   - **AI Ark:** empresas em Portugal com palavras-chave na descrição (clínica dentária, medicina dentária, fisioterapia, clínica de estética, clínica veterinária…), 1–50 pessoas. Cargos: sócio-gerente, diretor clínico, proprietário, fundador.
   - **Get Leads** e **"quick and rich"**: a mesma pesquisa, para cobrir os buracos. ⚠️ Não sei qual é a ferramenta "quick and rich". Diz-me o nome exato ou o site.
   - ⚠️ **Limite destas bases:** as bases B2B encontram empresas a partir do domínio, por isso **as clínicas sem site aparecem pouco**. Para esse segmento proponho juntar um scraper do Google Maps (Outscraper ou Apify), que apanha a ficha Google, as avaliações e o "website" (vazio ou Facebook).
2. **Enriquecer (toda a informação de contacto):** email geral, email do decisor, telefone fixo e móvel publicados, nome e cargo do decisor, site, ficha Google (nota e nº de avaliações), Instagram/Facebook, denominação social e NIF (→ `tipo_entidade`).
3. **Verificar:**
   - **MillionVerifier** (API) em todos os emails. Só passa `ok`. Os `catch_all` vão para um lote separado e pequeno. `invalid`, `disposable` e `unknown` saem.
   - **Telefones:** o MillionVerifier só verifica emails. Os números são validados com `libphonenumber` (formato e tipo: móvel ou fixo) e servem para a chamada depois de uma resposta.
4. **Filtro legal:** sociedade ✔ · não está na lista de oposição ✔ · não está em `supressao.csv` ✔. Os outros leads vão para o canal telefone ou são descartados.
5. **Visitar o site e escrever o icebreaker** (agente `icebreaker-writer`):
   - abre o site, ou a ficha Google/Instagram se não houver site;
   - regista **evidências**: HTTPS, versão móvel, velocidade no telemóvel (PageSpeed), marcação online sim/não, ano do copyright, nº de avaliações e nota, concorrente próximo com marcação online;
   - escreve **1 frase de ≤ 25 palavras** com um facto observado e verificável. Nunca elogio vazio ("adorei o vosso site") nem nada inventado;
   - grava a frase, a evidência e a URL da fonte. Se não houver um facto bom, o lead fica com `icebreaker = null` e não é enviado.
6. **Exportar** `campanhas/<id>/envio.csv` com os campos de `marca.md` (`saudacao`, `clinica`, `cidade`, `especialidade`, `icebreaker`, `fonte_contacto`, `variante`…). **Tu aprovas** e depois sobe para o sequenciador por API.
7. **Respostas:** o webhook do sequenciador → classificação automática (positiva / neutra / negativa / SAIR) → o Diogo responde a um "sim" em **< 15 min** e liga se houver número. Cada "sim" dispara a maquete do `frontend-designer` em ≤ 48h.
8. **Resultados** → `resultados.csv` → `analista-conversao` (§5).

### Agentes e scripts a criar (próximo passo)
| Peça | Faz |
|---|---|
| `.claude/agents/lead-scraper.md` | Corre os passos 1–4 por API e grava `vendas/email/campanhas/<id>/leads-verificados.json` |
| `.claude/agents/icebreaker-writer.md` | Passo 5: visita cada site e escreve o icebreaker com a evidência |
| `.claude/agents/analista-conversao.md` | Lê os resultados, calcula o funil e propõe o próximo teste |
| `vendas/email/pipeline/*.py` | Chamadas às APIs (AI Ark, Get Leads, MillionVerifier, PageSpeed, sequenciador) |
| Chaves | Em variáveis de ambiente (`AIARK_API_KEY`, `MILLIONVERIFIER_API_KEY`, `SMARTLEAD_API_KEY`…). **Nunca no repositório** |

---

## 4. Infraestrutura de envio

| Peça | Escolha |
|---|---|
| Domínio principal | `zarpa.pt`: site e portefólio. **Nunca envia cold email** |
| Domínios de envio | `usezarpa.pt`, `zarpastudio.pt`, `zarpahq.com`. Parecem livres numa verificação por DNS de 2026-10-18; confirmar na compra. Redirecionam para `zarpa.pt` |
| Caixas | 2 por domínio = **6 caixas** Google Workspace, todas "Diogo Martins" (diogo@, d.martins@) |
| DNS | SPF, DKIM, DMARC (`p=none` → `quarantine`), domínio de tracking próprio |
| Aquecimento | **2–3 semanas** antes do 1.º envio, sempre ligado. Subida até ~20/dia por caixa |
| **Sequenciador** | **Smartlead** (recomendado: API completa para ligar ao pipeline, caixas ilimitadas, aquecimento incluído). Alternativas: Instantly (o mais simples), Plus Vibe (o mais barato), EmailBison (pensado para agências com muito volume, demais para começar). Confirmar que o plano escolhido inclui API |
| Tracking | Aberturas **desligadas**. Mede-se pela resposta |
| Inbox | Teste a cada 2 semanas. Abaixo de 80% em inbox, o domínio descansa |

**Volume:** 20–40 contactos novos por dia. **Custo:** ~130–200€/mês (Workspace, sequenciador, AI Ark, MillionVerifier e domínios).

---

## 5. Métricas

Um evento por linha em `resultados.csv`: `lead_id, campanha, variante, subnicho, data, evento, valor`.

| Etapa | Meta inicial* | Alerta |
|---|---|---|
| Bounce | < 2% | > 3%: pausar |
| Taxa de resposta | ≥ 6% | < 3% |
| **Resposta positiva** | ≥ 3% | < 1,5% |
| Opt-out / queixa | < 2% / < 0,1% | rever segmento |
| Positiva → reunião | ≥ 50% | < 35% |
| Comparência | ≥ 75% | < 60% |
| Reunião → venda | ≥ 25% | < 15% |
| Ticket médio | ≥ 1400 | < 1000 |
| **⭐ Receita por 100 entregues** | ≥ 300 | < 100 |

\* Hipóteses de partida, a recalibrar com os nossos números ao fim de ~500 envios.

**Diagnóstico:**

| Sintoma | Causa provável |
|---|---|
| Poucas respostas | entregabilidade ou segmento |
| Respostas negativas | oferta ou icebreaker fraco |
| Positivas que não marcam | fricção na marcação |
| Faltas | falta de lembretes |
| Reuniões sem venda | preço, demo ou pacotes |

---

## 6. Ciclo de otimização

- Análise **semanal** e decisão **quinzenal**.
- **Uma variável de cada vez**, com A/B aleatório dentro do mesmo sub-nicho.
- Decide-se pela resposta positiva, com **≥ 150 entregues por variante** e uma diferença **≥ 1,5×** durante 2 semanas.
- O analista ataca primeiro a **etapa com o maior desvio** face à meta.
- Tudo fica registado em `experiencias.md`.

| # | Variável | A | B |
|---|---|---|---|
| 1 | Oferta de entrada | Maquete já feita (seq. A) | Maquete a pedido (seq. B) |
| 2 | Sub-nicho | Dentária | Fisioterapia |
| 3 | Tipo de icebreaker | Avaliações Google | Falha no site |
| 4 | CTA | "Posso enviar?" | "Seria descabido enviar?" |
| 5 | Saudação | "Bom dia," | "Bom dia, Dra. {{nome}}," |
| 6 | Assunto | `{{clinica}}` | `site da {{clinica}}` |
| 7 | Frase de liberdade | sem | com |
| 8 | Nº de follow-ups | 3 | 4 |
| 9 | Âncora | 2490 | 2990 |

Mais testes em §4 de `psicologia-venda.md`.

---

## 7. Os 15 emails

Estão em `vendas/email/emails/`. Usam os campos e o rodapé de `marca.md`.

| # | Ficheiro | Sequência | Dia | Objetivo |
|---|---|---|---|---|
| 1 | `01-a1-abertura-maquete-feita.md` | A | 0 | Pedir licença para enviar a maquete já feita |
| 2 | `02-a2-perda.md` | A | 3 | Mostrar o que perdem (pacientes que marcam noutro lado) |
| 3 | `03-a3-como-funciona.md` | A | 7 | 3 passos + pagamento só no fim |
| 4 | `04-a4-despedida.md` | A | 14 | Fechar com a porta aberta |
| 5 | `05-b1-abertura-maquete-a-pedido.md` | B | 0 | Oferecer a maquete em 48h |
| 6 | `06-b2-concorrencia.md` | B | 3 | Quem aparece no Google em vez deles |
| 7 | `07-b3-risco-zero.md` | B | 7 | Antecipar objeções + risco zero |
| 8 | `08-b4-despedida.md` | B | 14 | Fechar com a porta aberta |
| 9 | `09-abertura-dentaria.md` | A ou B | 0 | Abertura para clínicas dentárias |
| 10 | `10-abertura-fisioterapia.md` | A ou B | 0 | Abertura para fisioterapia |
| 11 | `11-abertura-estetica.md` | A ou B | 0 | Abertura para estética |
| 12 | `12-abertura-veterinaria.md` | A ou B | 0 | Abertura para veterinária |
| 13 | `13-entrega-maquete.md` | resposta | — | Link + vídeo + 2 horários |
| 14 | `14-proposta.md` | pós-reunião | — | 3 pacotes + próximo passo |
| 15 | `15-reativacao.md` | 60–90 dias | — | Reabrir quem disse "agora não" |

---

## 8. O que falta de ti

1. **"quick and rich":** qual é a ferramenta (nome exato ou site)?
2. **Sequenciador:** Smartlead (recomendado) ou outro?
3. **Google Maps scraper** para as clínicas sem site: junto ao pipeline?
4. **Contas e chaves de API** (AI Ark, Get Leads, MillionVerifier, sequenciador): quando as tiveres, vão para variáveis de ambiente e eu ligo o pipeline.
5. **Dados legais da Zarpa** para o rodapé: denominação, NIF e morada. Sem isto não se pode enviar.
6. **Pacotes:** confirmar o conteúdo de cada um (§2).

## 9. Calendário

| Semana | O quê |
|---|---|
| 0 | Respostas de §8 · compra de domínios e caixas · DNS · verificação legal · INPI/RNPC "Zarpa" |
| 1–2 | Aquecimento · agentes e scripts do pipeline · 1.º scrape (450 → ~150 dentárias) · vídeo de 90 s |
| 3 | **Piloto:** dentárias, Sequência A vs. B, 20–40/dia |
| 4 | 1.ª análise · primeiras reuniões |
| 5 | Decisão 1 → piloto 2 (fisioterapia ou teste #3) |
| 6+ | Ciclos de 2 semanas |
