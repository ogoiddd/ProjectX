# odds_value — análise de valor em odds de futebol

Ferramenta em Python para encontrar **valor esperado positivo (EV+)** em
mercados de futebol, comparando a odd de cada casa contra uma linha de
**consenso** construída a partir de dezenas de casas, com a margem removida.

Só usa **fontes públicas e legítimas** (APIs oficiais). **Não faz scraping**
de sites de casas de apostas.

---

## Como funciona

```
fetch.py   ──►  devig.py   ──►  value.py   ──►  cli.py
(recolha)      (sem margem)    (EV/valor)     (tabela + CSV)
```

1. **Recolha** — odds de várias casas por mercado (1X2, totals, BTTS) via
   The Odds API; opcionalmente forma/golos via API-Football.
2. **Preço justo** — remove-se a margem (overround) de cada casa por dois
   métodos (proporcional e Shin) e calcula-se uma linha de consenso
   ponderada (casas afiadas como a Pinnacle pesam mais).
3. **Valor** — para cada seleção compara-se a melhor odd contra a
   probabilidade de consenso: `EV% = (odd × prob_consenso) − 1`. Sinaliza-se
   tudo acima de +2%, ordenado por magnitude, com aviso de dispersão/outlier.
4. **Contexto** — flags para 2ª mão de eliminatória, altitude (>2000 m) e
   mercados combinados (margem alta) para reduzir falsos positivos.
5. **Output** — tabela em consola, CSV e resumo final.

### Filtros de fiabilidade

Para reduzir falsos positivos onde os cálculos são frágeis:

- **Mín. 5 casas por mercado** — mercados com menos casas são **descartados**
  (consenso pouco fiável). Ajustável com `--min-books`.
- **Prob. de consenso ≥ 10%** — seleções na cauda (azarões extremos) são
  **ignoradas**: o devig é pouco fiável aí e o EV fica hipersensível a erros.
  Ajustável com `--min-prob`.
- **Concordância Shin × proporcional** — cada sinal é avaliado sob os **dois**
  métodos de devig; a coluna `Confirma` diz se ambos concordam. Sinais de um
  só método são marcados como **menos robustos**.
- **Mediana e desvio** — além da melhor odd, mostra-se a **odd mediana** e o
  **desvio-padrão** entre casas, para contextualizar quão fora da linha está a
  melhor odd.
- **Estatística por casa** — conta quantas vezes cada bookmaker aparece como
  "melhor odd"; uma casa que domina (≥40%) é assinalada como possível
  **outlier sistemático** (linhas moles/desatualizadas, não valor real).

### Whitelist: acionável vs referência

Podes indicar as **casas onde consegues apostar** (`--books`, ou o campo na
web). Nesse caso o output separa-se em duas secções:

- **Acionável** — valor na melhor odd **entre as tuas casas**. É o que podes
  mesmo jogar.
- **Referência** — valor a viver **noutras casas** (a que não tens acesso).
  Não é acionável, mas é informativo: se as casas afiadas (Pinnacle) estão
  bem acima do consenso, confirma que a linha tem valor.

Ponto importante: **todas** as casas continuam a entrar no cálculo do
consenso (mais dados = melhor estimativa). A whitelist só decide o que conta
como *oportunidade*, não o que entra na média. A correspondência de nomes é
tolerante (`betfair` casa com `betfair_ex_eu`).

---

## Instalação

```bash
pip install -r requirements.txt   # requests
```

Chaves de API lidas de variáveis de ambiente:

```bash
export ODDS_API_KEY=xxxxxxxxxxxxxxxx      # https://the-odds-api.com  (tier gratuito)
export API_FOOTBALL_KEY=yyyyyyyyyyyy      # https://www.api-football.com (opcional)
```

## Utilização

```bash
# Ao vivo (The Odds API):
python -m odds_value.cli --sport soccer_epl --markets h2h,totals --method shin --csv valor.csv

# Sem rede, a partir de uma resposta guardada (útil para demo/teste):
python -m odds_value.cli --from-json examples/the_odds_api_sample.json --compare-devig
```

Opções principais:

| Opção | Descrição |
|-------|-----------|
| `--sport` | chave do desporto no The Odds API (ex.: `soccer_epl`, `soccer_uefa_champs_league`) |
| `--markets` | `h2h` (1X2), `totals` (O/U), `btts` |
| `--regions` | `eu,uk,us,au` |
| `--method` | `proportional` ou `shin` (devig usado no consenso) |
| `--ev-threshold` | EV mínimo para sinalizar (fracionário; `0.02` = +2%) |
| `--min-books` | nº mínimo de casas por mercado (padrão 5) |
| `--min-prob` | prob. de consenso mínima por seleção (padrão `0.10`) |
| `--books` | whitelist de casas onde podes apostar (separadas por vírgula) |
| `--compare-devig` | mostra proporcional vs Shin para o 1.º mercado |
| `--csv` | caminho do CSV de saída |
| `--from-json` | lê JSON local em vez de chamar a API |

### Colunas da tabela / CSV

`jogo · mercado · seleção · melhor odd · casa · mediana · desvio · prob. consenso ·
odd justa · EV% · EV Shin/Prop · confirma (concordância dos métodos)`.
O CSV inclui ainda `ev_shin_pct`, `ev_prop_pct`, `metodos_confirmam`, `n_casas`,
`dispersao_odds`, `outlier`, `avisos`. No fim, um resumo lista quantas casas
deram a melhor odd (estatística de outliers) e quantos mercados foram
descartados por terem menos de 5 casas.

---

## Web app — usar no telemóvel (iPhone/Android) em qualquer lugar

Há uma interface web incluída (`odds_value/web.py`), construída **só com a
biblioteca-padrão do Python** — não precisa de Flask/FastAPI, só de `requests`.

Correr localmente:

```bash
export ODDS_API_KEY=xxxxxxxx
python -m odds_value.web        # abre http://localhost:8000
```

Abres o endereço no browser (Safari/Chrome), escolhes competição, mercados e
método, e obténs a tabela de valor com um botão para descarregar o CSV. Podes
"Adicionar ao ecrã inicial" no iPhone para ficar com aparência de app. Há uma
opção **"usar dados de exemplo"** para testar sem chave de API.

### Alojar de graça (para aceder de qualquer lado)

O objetivo "usar em qualquer lugar" resolve-se alojando a web app; o iPhone só
abre o link. O repositório já traz os ficheiros de deploy.

**Render (recomendado, plano gratuito):**
1. Faz push deste repositório para o GitHub.
2. Em render.com: **New + → Blueprint** e aponta para o repo (usa `render.yaml`).
3. No dashboard, define a variável de ambiente **`ODDS_API_KEY`** (secreta).
4. Fica disponível num URL `https://…onrender.com` — abre-o no iPhone.

**Railway / Fly.io / Heroku:** usam o `Procfile` (`web: python -m odds_value.web`);
define lá a variável `ODDS_API_KEY`. A app lê a porta de `PORT` automaticamente.

**No próprio iPhone (a-Shell, sem servidor):** instala o a-Shell, faz
`pip install requests`, copia a pasta `odds_value/`, e corre
`python -m odds_value.web`; depois abre `http://localhost:8000` no Safari.
Serve para uso local no aparelho (não fica acessível fora dele).

> ⚠️ **Segurança:** aloja atrás de HTTPS (Render/Railway dão-no de borla) e não
> exponhas a tua `ODDS_API_KEY` no cliente — ela fica só no servidor.

---

## Os dois métodos de remoção de margem

- **Normalização proporcional** — escala as probabilidades implícitas para
  somarem 1. Simples e robusta, mas enviesa contra os favoritos
  (*favourite-longshot bias*), porque as casas costumam carregar mais margem
  nos azarões.
- **Método de Shin (1993)** — modela a margem como fração `z` de dinheiro
  informado ("insider trading") e resolve `z` numericamente. Corrige parte do
  enviesamento e costuma aproximar-se melhor das probabilidades verdadeiras
  em mercados de 2-3 seleções. `--compare-devig` mostra os dois lado a lado.

---

## Fontes de dados e limitações

### The Odds API (`the-odds-api.com`)
- **O quê:** agrega odds de dezenas de casas por mercado; formato decimal; ISO
  para datas. Endpoint usado: `GET /v4/sports/{sport}/odds`.
- **Limitações:**
  - Tier gratuito tem **quota mensal de pedidos** — cada chamada consome
    crédito proporcional ao nº de regiões/mercados. Verifica os headers
    `x-requests-remaining` / `x-requests-used`.
  - **Latência:** as odds podem estar alguns segundos/minutos atrasadas face à
    casa; uma odd "de valor" pode já não existir quando fores apostar.
  - **Cobertura desigual:** nem todas as casas cotam todos os mercados; só se
    usam no consenso as casas que cotaram **todas** as seleções do mercado.
  - Não expõe metadados de contexto (eliminatórias, estádio) — ver abaixo.

### API-Football (`api-football.com`)
- **O quê:** forma recente, golos marcados/sofridos, fixtures e resultados de
  eliminatórias (útil para o filtro de 2.ª mão).
- **Limitações:** tier gratuito com **limite diário** de chamadas; requer
  mapear IDs de equipas/ligas; a cobertura histórica varia por competição.

### Limitações do próprio modelo
- O **consenso não é a verdade** — é a melhor estimativa disponível do
  mercado. Uma odd muito acima do consenso pode ser **valor genuíno** ou
  **erro/informação em falta** na casa (lesões, onze, notícias). Esses casos
  são marcados como **outlier** — confirma sempre antes de apostar.
- **Mercados combinados** (resultado+golos, etc.) têm margem tipicamente
  **20-30%**, muito acima dos mercados simples; o consenso é bem menos fiável
  e a ferramenta avisa-o.
- **Contexto distorce mercados de resultado:** numa **2.ª mão de
  eliminatória** o favorito pode não precisar de vencer; a **altitude**
  (>2000 m, ex.: La Paz, Quito, Bogotá) afeta desempenho e golos. Estas flags
  são heurísticas — a de 2.ª mão tem de ser passada explicitamente porque a API
  não a fornece.
- **Isto não é aconselhamento de apostas.** EV+ com base num consenso é uma
  estimativa estatística com incerteza; usa gestão de risco e joga de forma
  responsável.

---

## Testes

```bash
pytest -q
```

Cobrem sobretudo as funções de remoção de margem (`tests/test_devig.py`:
proporcional, Shin, `z` de Shin, consenso ponderado) e a deteção de valor
(`tests/test_value.py`: EV, outliers, avisos de contexto).

## Estrutura

```
odds_value/
  fetch.py     # clientes The Odds API / API-Football + heurísticas de contexto
  devig.py     # remoção de margem (proporcional + Shin) e consenso
  value.py     # EV%, dispersão, outliers, filtros de contexto
  pipeline.py  # recolha → análise + serialização CSV (partilhado CLI/web)
  cli.py       # tabela em consola, CSV, resumo
  web.py       # web app (stdlib) para usar no browser/telemóvel
tests/
  test_devig.py
  test_value.py
examples/
  the_odds_api_sample.json   # resposta de exemplo para correr offline
Procfile, render.yaml, runtime.txt   # deploy (Render/Railway/Fly.io)
```
