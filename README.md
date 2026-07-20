# solana-token-monitor-x

Monitora uma lista configurável de contas do X (Twitter) via **API oficial v2
(tier pago)**, detecta anúncios de lançamento de tokens Solana nos posts
(contract address direto, link do pump.fun/Dexscreener ou site externo),
valida o CA on-chain e dispara alerta instantâneo no Telegram (e Discord,
opcional). Inclui um módulo de execução **opcional e desligado por padrão**
(swap SOL → token via Jupiter), com **paper trading como modo padrão**.

Inspirado no cenário do lançamento do $TRUMP (jan/2025), em que o anúncio foi
um post com link para o site + CA.

> ⚠️ **Aviso**: memecoins recém-lançadas são de altíssimo risco (rug pulls,
> honeypots, tokens falsos postados por contas hackeadas). Este projeto é
> educacional; o modo live movimenta dinheiro real por sua conta e risco.
> Nada aqui é recomendação de investimento.

## Por que Node.js

- O ecossistema Solana/Jupiter é JavaScript-first; exemplos e APIs assumem JS.
- `fetch` nativo, streams e `AbortSignal` cobrem polling, filtered stream e
  timeouts sem bibliotecas extras.
- **Zero dependências de runtime**: todas as integrações (X, Telegram,
  Discord, Jupiter, RPC Solana) usam `fetch` nativo; a assinatura ed25519 do
  modo live usa `node:crypto`; testes usam `node:test`. Num projeto que pode
  tocar em chave de carteira, cadeia de suprimentos vazia = superfície de
  ataque mínima (sem risco de pacote npm comprometido exfiltrar a chave).

## Arquitetura

```
                 ┌──────────────────────────────────────────┐
                 │              src/index.js                │
                 │  carrega .env + config.json, faz o wiring │
                 └──────────────┬───────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        │                 MONITOR                        │
        │  poller.js  → /2/tweets/search/recent          │
        │               (1 query cobre todas as contas,  │
        │                since_id incremental)           │
        │  stream.js  → /2/tweets/search/stream          │
        │               (Pro tier; push em ~1-5s,        │
        │                keep-alive + reconexão)         │
        │  latência = agora − timestamp do snowflake ID  │
        └───────────────────────┬───────────────────────┘
                                │ tweet + latência
        ┌───────────────────────┴───────────────────────┐
        │              PIPELINE (pipeline.js)            │
        │                                                │
        │  1. parser/extract.js (puro, testável)         │
        │     • regex base58 32-44 chars, com validação  │
        │       real (decode → 32 bytes)                 │
        │     • links: pump.fun / dexscreener / birdeye /│
        │       solscan / raydium → CA extraído da URL   │
        │     • site externo sem CA → fila de scan       │
        │  2. parser/siteScan.js                         │
        │     • fetch com timeout + cap de bytes         │
        │     • ranking por proximidade de keywords      │
        │       ("contract", "CA", "mint"…)              │
        │  3. validator/caValidator.js                   │
        │     • RPC getAccountInfo: conta existe e é um  │
        │       mint SPL (Token ou Token-2022)?          │
        │     • link de par (dexscreener) → resolve para │
        │       o mint via API de pairs                  │
        │     • enriquecimento Dexscreener (nome, liq.)  │
        │  4. alerts/notifier.js                         │
        │     • Telegram + Discord em paralelo           │
        │     • loga latência detecção + alerta          │
        │  5. executor/ (OPCIONAL, off por padrão)       │
        │     • kill switch → limites → quote Jupiter    │
        │     • paper: simula e loga em data/trades.jsonl│
        │     • live: assina (node:crypto ed25519) e     │
        │       envia via RPC                            │
        └────────────────────────────────────────────────┘
```

### Estrutura de pastas

```
src/
  index.js               entrypoint / wiring / shutdown
  config.js              .env + config.json + validação
  pipeline.js            orquestração por post (testável)
  util/
    base58.js            base58 + validação de endereço Solana
    logger.js            logs estruturados JSON-lines
  monitor/
    xApi.js              cliente X API v2 (rate limit, retries, snowflake→ms)
    poller.js            polling via search/recent
    stream.js            filtered stream com reconexão
  parser/
    extract.js           extração de CAs e links (funções puras)
    siteScan.js          fetch + scan de sites externos
  validator/
    caValidator.js       validação on-chain + Dexscreener
  alerts/
    notifier.js          Telegram + Discord
  executor/
    executor.js          paper/live trading com limites e kill switch
    signer.js            keypair burner + assinatura de versioned tx
test/                    testes unitários (node --test)
config.example.json      tunables (sem segredos)
.env.example             segredos (nunca commitados)
```

## Setup

Requisitos: Node.js >= 20 (testado no 22). Sem `npm install` necessário para
rodar — não há dependências de runtime.

```bash
cp config.example.json config.json   # edite as contas monitoradas etc.
cp .env.example .env                 # preencha os tokens
npm test                             # testes unitários
npm start                            # inicia o monitor
```

Logs são JSON-lines no stdout — redirecione para arquivo ou jq:
`npm start | tee monitor.log` / `npm start | jq .`

### Kill switch (execução)

Duas formas, ambas checadas **a cada trade**, sem reiniciar o processo:

- `touch KILL_SWITCH` na raiz do projeto (remova o arquivo para reativar);
- variável de ambiente `KILL_SWITCH=1`.

### Habilitando execução (leia antes)

1. `executor.enabled: true` no `config.json` → ainda é **paper trading**:
   pega quote real na Jupiter, loga e grava em `data/trades.jsonl`, não toca
   em carteira.
2. Só depois de validar o comportamento: `paperTrading: false` **e**
   `BURNER_WALLET_PRIVATE_KEY` no `.env` (carteira descartável com fundos
   mínimos — nunca a principal). Limites obrigatórios: `buyAmountSol` ≤
   `maxSolPerTrade`, `maxSlippageBps` ≤ 10000, `priorityFeeLamports`
   configurável.

## Custos da API do X (confirme em developer.x.com — mudam com frequência)

| Tier  | Preço (ordem de grandeza, 2025/2026) | O que dá para este projeto |
|-------|--------------------------------------|-----------------------------|
| Free  | $0    | Inútil: ~100 leituras/mês, sem search útil |
| Basic | ~US$ 200/mês | `search/recent` com rate limit baixo (~60 req/15min por app) → polling de ~15s cobrindo todas as contas numa query; ~10-15k posts lidos/mês; **sem** filtered stream |
| Pro   | ~US$ 5.000/mês | Filtered stream (push em segundos), 1M posts/mês, rate limits altos |

Na prática: **Basic + polling** dá latência de detecção na casa de
10-30 segundos (intervalo de polling + atraso do índice de busca).
**Pro + stream** dá ~1-5 segundos. Ambos ficam atrás dos snipers
profissionais (ver limitações).

## Limitações conhecidas (importante)

- **Latência da API oficial**: mesmo o filtered stream (Pro) entrega o post
  segundos depois da publicação, e o índice do `search/recent` pode atrasar
  mais. No lançamento do $TRUMP, bots competitivos compraram em <1s usando
  firehoses comerciais e infraestrutura colocated — a API oficial não compete
  nesse patamar. Trate este sistema como alerta rápido, não como sniper de
  primeiro bloco.
- **Truth Social não tem API pública.** O anúncio do $TRUMP saiu no Truth
  Social e no X quase simultaneamente; este projeto só cobre o X. Não há
  forma oficial de monitorar Truth Social.
- **Scraping viola os ToS do X.** A alternativa "grátis" (scraping da web ou
  de endpoints internos) viola os Termos de Serviço do X e pode derrubar sua
  conta/IP; este projeto usa somente a API oficial paga, por isso os custos
  acima são incontornáveis.
- **Rate limits**: o cliente respeita `x-rate-limit-reset` em 429 e usa
  backoff exponencial em 5xx/queda de stream, mas o tier Basic limita a
  frequência efetiva de polling.
- **Validação ≠ segurança**: o validador confirma que o CA existe e é um mint
  SPL, e enriquece com Dexscreener — isso **não** detecta honeypot, rug ou
  token falso postado por conta hackeada.
- **Dexscreener logo após o lançamento**: pares podem demorar minutos para
  indexar; "sem pares ainda" não invalida o token (o alerta indica isso).
- **Sites externos**: páginas 100% renderizadas em JavaScript (SPA sem SSR)
  não expõem o CA no HTML inicial; o scanner só vê o HTML bruto.

## Testes

```bash
npm test
```

Cobrem: parser (CA puro, link pump.fun, link dexscreener/par, site externo,
post sem nada, falsos positivos de base58, dedupe), scanner de HTML (ranking
por keyword/frequência), base58 round-trip, conversão snowflake→timestamp,
chunking de queries, validador (mint válido, conta inexistente, não-mint,
resolução de par) e executor (desligado por padrão, kill switch por env e por
arquivo, limite por trade, paper mode sem tocar em `/swap`, live sem chave
falha com segurança).
