# 🤖 Polymarket Copytrading Bot

Bot que **deteta** trades de carteiras que escolheres na Polymarket e **copia-os**
automaticamente na tua conta, dimensionando cada ordem segundo a tua estratégia e
os teus limites de risco.

Arquitetura (a mesma que o guia da QuickNode descreve):

```
   ┌────────────────┐   sonda cada Ns    ┌──────────────────┐
   │  Data API      │◀───────────────────│   WATCHER        │
   │ (deteção de    │  trades dos alvos  │ (bot.py)         │
   │  trades)       │───────────────────▶│                  │
   └────────────────┘                    └────────┬─────────┘
                                                   │ trade novo
                                          ┌────────▼─────────┐
                                          │  SIZING + RISCO  │
                                          │ (sizing.py)      │
                                          └────────┬─────────┘
                                                   │ decisão
   ┌────────────────┐   ordem FOK        ┌────────▼─────────┐
   │  CLOB API      │◀───────────────────│   EXECUTOR       │
   │ (execução)     │                    │ (clob.py)        │
   └────────────────┘                    └──────────────────┘
```

- **Deteção** — sonda a [Data API](https://docs.polymarket.com/api-reference/core/get-trades-for-a-user-or-markets)
  (`/trades`), que é pública e sem autenticação.
- **Execução** — usa o cliente oficial [`py-clob-client`](https://github.com/Polymarket/py-clob-client)
  para assinar e submeter ordens de mercado na CLOB.
- **Estado** — guarda em `state.json` que trades já viu (para não duplicar) e
  quanto já gastou hoje (limite diário).

---

## ⚠️ Antes de começares — lê isto

- **Isto mexe com dinheiro real.** Um bug, um alvo azarado ou um mercado ilíquido
  podem fazer-te perder USDC. Começa com valores pequenos.
- **Copytrading não é lucro garantido.** Copias as boas *e* as más decisões do
  alvo, e entras sempre um pouco depois dele (pior preço).
- **Nunca partilhes a tua chave privada.** O `.env` está no `.gitignore` — mantém
  assim. Quem tiver a chave controla os teus fundos.
- **Confirma a legalidade** da Polymarket na tua jurisdição antes de a usares.

---

## 📋 Pré-requisitos

1. **Uma conta Polymarket** em [polymarket.com](https://polymarket.com) (login por
   email/Magic ou carteira). Faz um pequeno depósito de **USDC na rede Polygon**.
2. **A tua chave privada** e o **endereço que detém os fundos** (ver secção
   "Configuração" abaixo — é o passo que mais confunde).
3. **Python 3.10+** (ou Docker).
4. **Um sítio para alojar o bot** que esteja sempre ligado: um VPS barato
   (Hetzner, DigitalOcean, Contabo…), um Raspberry Pi, ou qualquer máquina que não
   desligues. O bot precisa de correr 24/7 para não perder trades.

---

## 🚀 Instalação

```bash
git clone <este-repositório>
cd ProjectX

# (recomendado) ambiente virtual
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

## ⚙️ Configuração

Copia o exemplo e edita:

```bash
cp .env.example .env
nano .env        # ou o editor que preferires
```

### Os campos mais importantes

| Variável | O que é | Onde obter |
|---|---|---|
| `POLYGON_PRIVATE_KEY` | A chave que **assina** as ordens (0x…) | Exporta-a da tua carteira Polymarket / MetaMask |
| `POLYMARKET_FUNDER_ADDRESS` | O endereço que **detém o USDC** | Ver abaixo ⬇️ |
| `POLYMARKET_SIGNATURE_TYPE` | Como assinas | `1` para login email/Magic (o mais comum), `0` para MetaMask/EOA |
| `TARGET_WALLETS` | Quem copiar | Endereços do [leaderboard](https://polymarket.com/leaderboard) |

#### Como descobrir o `FUNDER_ADDRESS` e o `SIGNATURE_TYPE` (importante!)

A Polymarket usa muitas vezes uma **proxy wallet**: a chave que assina é diferente
do endereço que guarda o dinheiro. Escolhe o teu caso:

- **Login por email / Magic (a maioria dos utilizadores web):**
  `SIGNATURE_TYPE=1`. O `FUNDER_ADDRESS` é o teu *Polymarket deposit address* —
  vê-lo em **polymarket.com → Deposit**, ou no teu perfil. A chave privada é a da
  wallet Magic associada.

- **Carteira própria (MetaMask/EOA) com os fundos nessa conta:**
  `SIGNATURE_TYPE=0` e o `FUNDER_ADDRESS` é o **mesmo endereço** da tua chave.

> 💡 Se as ordens falharem com erros de saldo/allowance, quase sempre é porque o
> `FUNDER_ADDRESS` ou o `SIGNATURE_TYPE` estão trocados.

#### Como escolher quem copiar

Vai ao [leaderboard da Polymarket](https://polymarket.com/leaderboard), abre o
perfil de um trader com bom histórico, e copia o endereço da carteira (0x…) do
URL/perfil. Cola em `TARGET_WALLETS` (podes pôr vários separados por vírgula).

> Dica: prefere traders com **volume consistente** e mercados líquidos. Um trader
> que faz apostas gigantes e raras é difícil de copiar bem.

### Estratégia de tamanho (sizing)

| `SIZING_STRATEGY` | Comportamento |
|---|---|
| `fixed` | Gastas sempre `FIXED_SIZE_USDC` por cada compra copiada (ex.: 5 USDC) |
| `proportional` | Gastas `valor-do-alvo × COPY_RATIO` (ex.: `0.05` = 5% do que ele apostou) |

Em ambos os casos, cada ordem é limitada por `MAX_POSITION_USDC` (teto por trade) e
pelo `MAX_DAILY_USDC` (teto por dia).

### Quando o alvo vende (`SELL_MODE`)

| Valor | Comportamento |
|---|---|
| `exit_full` | Quando o alvo vende esse token, vendes **toda** a tua posição nele (sais quando ele sai) |
| `proportional` | Vendes uma fração proporcional ao que ele vendeu |
| `ignore` | Só copias compras; geres as saídas à mão |

---

## ✅ Testar antes de arriscar dinheiro

**1) Verifica a config e a ligação (não envia ordens):**

```bash
python run.py --check
```

Isto valida o `.env`, lê os trades recentes dos teus alvos e (se estiveres em live)
testa a autenticação na CLOB.

**2) Corre em modo DRY-RUN** (o valor por defeito no `.env.example`):

```bash
python run.py
```

Com `DRY_RUN=true`, o bot faz **tudo** — deteta trades, calcula tamanhos, aplica
limites — mas em vez de enviar ordens escreve no log `[DRY-RUN] COMPRARIA…`. Deixa-o
correr um bocado e confirma que as decisões fazem sentido.

**3) Passa a LIVE** só quando confiares: muda no `.env`

```env
DRY_RUN=false
```

e volta a correr `python run.py`. Começa com `FIXED_SIZE_USDC` pequeno e um
`MAX_DAILY_USDC` baixo.

> No primeiro arranque o bot faz **bootstrap**: marca todos os trades já existentes
> dos alvos como "vistos" e **não** os copia. Só copia trades que aconteçam *depois*
> de o ligares. Isto evita copiar retroativamente o histórico inteiro.

---

## 🖥️ Alojar o bot 24/7

O bot só copia trades enquanto está a correr. Opções:

### Opção A — `systemd` num VPS (recomendado)

Cria `/etc/systemd/system/copybot.service`:

```ini
[Unit]
Description=Polymarket Copytrading Bot
After=network-online.target

[Service]
WorkingDirectory=/home/USER/ProjectX
ExecStart=/home/USER/ProjectX/.venv/bin/python run.py
Restart=always
RestartSec=10
User=USER

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now copybot
journalctl -u copybot -f          # ver logs em tempo real
```

### Opção B — Docker

```bash
docker build -t copybot .
docker run -d --name copybot --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  copybot

docker logs -f copybot
```

O volume `-v` mantém o `state.json` entre reinícios (dedup + gasto diário).

### Opção C — deixar num terminal (só para testes)

```bash
python run.py            # Ctrl+C para parar
# ou em background:
nohup python run.py > bot.log 2>&1 &
```

---

## 📊 Monitorização e paragem

- **Logs**: tudo é registado no stdout (nível controlado por `LOG_LEVEL`).
  Cada trade detetado, cada decisão (copiado / ignorado e porquê) e cada ordem.
- **Parar**: `Ctrl+C` (ou `systemctl stop copybot` / `docker stop copybot`). O bot
  termina o ciclo atual, guarda o estado e sai de forma limpa.
- **Estado**: `state.json` guarda os trades já processados e o gasto do dia. Apagá-lo
  faz o bot voltar a fazer bootstrap (recomeça "do zero", sem copiar o passado).

---

## 🗂️ Estrutura do projeto

```
run.py                 Ponto de entrada (python run.py [--check])
copybot/
  config.py            Carrega e valida o .env
  data_api.py          Cliente da Data API (deteção de trades + posições)
  sizing.py            Cálculo do tamanho e regras de risco
  clob.py              Execução de ordens via py-clob-client
  state.py             Dedup de trades + limite de gasto diário
  bot.py               Loop principal (watcher + executor)
  logger.py            Logging
requirements.txt
.env.example           Modelo de configuração (copia para .env)
Dockerfile
```

---

## 🩺 Resolução de problemas

| Sintoma | Causa provável / solução |
|---|---|
| `Configuração inválida: … em falta` | Falta uma variável no `.env`. Compara com `.env.example`. |
| `--check` diz "sem trades lidos" | Endereço do alvo errado, ou a carteira não tem trades recentes. |
| Ordens falham com erro de saldo/allowance | `FUNDER_ADDRESS` ou `SIGNATURE_TYPE` errados; ou USDC insuficiente na Polygon. |
| Ordem `FOK` rejeitada | Mercado sem liquidez suficiente para preencher já; é normal em mercados finos. |
| Não copia nada | Confirma que não estás só a apanhar o bootstrap; faz um trade de teste no alvo; baixa o `MIN_TRADE_USDC`. |
| Copiou tarde / pior preço | Baixa o `POLL_INTERVAL_SECONDS` para reagir mais depressa. |

---

## 📈 Como ajustar a estratégia

- **Começa conservador:** `SIZING_STRATEGY=fixed`, `FIXED_SIZE_USDC=2`,
  `MAX_DAILY_USDC=20`, um único alvo de confiança.
- **Poll mais rápido = entradas mais próximas do alvo**, mas mais chamadas à API.
  15s é um bom equilíbrio; 5s é agressivo.
- **Vários alvos:** o bot funde os trades de todos por ordem cronológica. Cuidado
  com o gasto diário combinado.
- **Filtra mercados** com `ALLOWED_CONDITION_IDS` / `BLOCKED_CONDITION_IDS` se só
  quiseres certos temas.

---

## ⚖️ Aviso legal

Este software é fornecido "tal como está", apenas para fins educativos. Não é
aconselhamento financeiro. Trading envolve risco de perda total do capital. O autor
não é responsável por perdas. Verifica a legalidade da Polymarket na tua região.
