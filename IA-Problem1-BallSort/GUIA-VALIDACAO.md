# Guia de validação: Problem 1 (Ball Sort Puzzle)

Este guia explica o código do zero: primeiro o problema, depois o Java que precisas de saber, depois cada ficheiro linha a linha, e no fim as perguntas que o professor pode fazer, com as alterações ao código já escritas.

---

## Parte 1: a ideia geral em 5 frases

1. Um **estado** é uma fotografia do jogo: que bolas estão em que tubos.
2. A partir de um estado, cada **movimento legal** dá um novo estado (um "filho").
3. Isto forma um **grafo de estados**: o estado inicial liga-se aos filhos, que se ligam aos filhos deles, e assim por diante.
4. Queremos o **caminho mais curto** (menos movimentos) do estado inicial até um estado objetivo (todos os tubos vazios ou cheios de uma só cor).
5. O algoritmo do Tutorial 1 (**procura de custo uniforme**, uma forma de *best-first*) explora sempre primeiro o estado com menor custo acumulado `g`. Como todos os movimentos custam 1, o primeiro objetivo que encontra é o de menor número de movimentos.

### O padrão Strategy (o que o professor mais quer ver)

O código está dividido em duas partes que não se conhecem uma à outra:

| Parte | Ficheiro | O que sabe |
|---|---|---|
| **O algoritmo** (contexto) | `BestFirst.java` | Sabe procurar. **Não sabe nada de bolas nem tubos.** |
| **O problema** (estratégia) | `BallSortLayout.java` | Sabe as regras do jogo. **Não sabe nada de procura.** |
| **O contrato entre os dois** | `Ilayout.java` | Uma interface com 3 métodos: `children()`, `isGoal()`, `getK()`. |

O `BestFirst` é **exatamente o mesmo** que no 8-puzzle do Tutorial 1. Para resolver o Ball Sort só foi preciso escrever uma nova classe que implementa `Ilayout`. É essa a vantagem do Strategy: trocar de problema sem tocar no algoritmo.

---

## Parte 2: o Java mínimo que precisas de saber

| Conceito | Exemplo no código | O que significa |
|---|---|---|
| `class` | `class BestFirst { ... }` | Um molde para criar objetos. Agrupa dados (campos) e ações (métodos). |
| `interface` | `interface Ilayout { ... }` | Uma lista de métodos que uma classe **promete** ter, sem dizer como. |
| `implements` | `class BallSortLayout implements Ilayout` | "Esta classe cumpre o contrato da interface `Ilayout`." |
| Campo | `private int height;` | Uma variável que pertence a cada objeto. `private` = só a própria classe lhe mexe. |
| Construtor | `public BallSortLayout(String str)` | Método especial que cria o objeto. Tem o nome da classe e não tem tipo de retorno. |
| Método | `public double getK() { return 1; }` | Uma função do objeto. `double` é o tipo do que devolve. |
| Tipos simples | `int` (inteiro), `double` (real), `char` (um carácter, ex. `'R'`), `boolean` (`true`/`false`) | |
| Array | `int[] size`, `char[][] tubes` | Lista de tamanho fixo. `char[][]` é uma tabela (array de arrays). Índices começam em **0**. |
| `new` | `new int[nTubes]` | Cria um objeto ou array novo. Um array de `int` começa cheio de zeros. |
| `for` | `for (int i = 0; i < n; i++)` | Repete para `i = 0, 1, ..., n-1`. |
| `if` / `continue` / `return` | `if (size[i] == 0) continue;` | `continue` salta para a próxima volta do ciclo; `return` sai do método. |
| `x++` / `--x` | `size[t]++` | Soma/subtrai 1. `x++` usa o valor **antes** de somar; `--x` subtrai **antes** de usar. |
| `? :` | `r < size[t] ? tubes[t][r] : EMPTY` | "Se a condição for verdade, usa o primeiro; senão, o segundo." |
| `null` | `father = null` | "Não aponta para nenhum objeto." O estado inicial não tem pai. |
| `List` / `ArrayList` | `List<Ilayout> children = new ArrayList<>();` | Lista que cresce. `add()` acrescenta. |
| `Map` / `HashMap` | `fechados.put(chave, valor)`, `containsKey(chave)` | Dicionário chave → valor. Procura em tempo constante. |
| `Set` / `HashSet` | `emAbertos.add(x)`, `contains(x)` | Conjunto sem repetidos. Procura em tempo constante. |
| `PriorityQueue` | `abertos.remove()` | Fila que devolve sempre o **menor** elemento segundo um critério (aqui, o menor `g`). |
| Lambda | `(s1, s2) -> (int) Math.signum(s1.getG() - s2.getG())` | Função curta escrita no sítio. Aqui compara dois estados: negativo se `s1` tem menor `g`. |
| `equals` / `hashCode` | | Como o Java decide se dois objetos são "iguais". `HashMap` e `HashSet` dependem disto. Regra: se `a.equals(b)` então `a.hashCode() == b.hashCode()`. |
| `static class` dentro de outra | `static class State` dentro de `BestFirst` | Uma classe auxiliar que vive dentro de outra. Usa-se como `BestFirst.State`. |
| `Iterator` | `it.hasNext()`, `it.next()` | Objeto para percorrer uma sequência um a um. |

---

## Parte 3: o código, ficheiro a ficheiro

### 3.1 `Ilayout.java`: o contrato

```java
interface Ilayout {
    List<Ilayout> children();   // todos os estados alcançáveis com 1 movimento
    boolean isGoal(Ilayout l);  // este estado é objetivo?
    double getK();              // custo do movimento que levou a este estado
}
```

### 3.2 `BallSortLayout.java`: as regras do jogo

**Representação (linhas 6–9)**

```java
private static final char EMPTY = 'E';
private int height;      // capacidade H de cada tubo
private char[][] tubes;  // tubes[t][k] = cor da bola na posição k do tubo t (k = 0 é o FUNDO)
private int[] size;      // size[t] = quantas bolas tem o tubo t
```

Cada tubo é uma **pilha**: o fundo está em `tubes[t][0]` e o topo em `tubes[t][size[t] - 1]`.

Exemplo, Sample 2 (`H = 3`, 3 tubos):

```
R B E        tubo 0: fundo R, B, R topo  →  tubes[0] = {R, B, R}, size[0] = 3
B B E        tubo 1: fundo R, B, B topo  →  tubes[1] = {R, B, B}, size[1] = 3
R R E        tubo 2: vazio               →  size[2] = 0
```

**Construtor (linhas 12–29)**: lê o texto e enche os tubos.
- `str.split("\n")` parte o texto em linhas; `height` é o número de linhas.
- Lê as linhas **de baixo para cima** (`r` desce de `height-1` até `0`), porque a última linha do input é o fundo dos tubos.
- Para cada tubo `t`, se a cor não é `E`, empilha-a: `tubes[t][size[t]++] = c` (põe na posição `size[t]` e depois aumenta `size[t]`).

**`clone()` (linhas 37–42)**: faz uma **cópia profunda** (copia os arrays, não só as referências). Sem isto, mudar o filho também mudava o pai, porque partilhariam os mesmos arrays.

**`toString()` (linhas 45–55)**: o inverso do construtor. Escreve as linhas de cima para baixo, com `E` onde não há bola, separadas por um espaço. É o que o `Main0` imprime.

**`equals()` e `hashCode()` (linhas 57–66)**: dois layouts são iguais se têm as mesmas bolas nas mesmas posições. São usados pelo `HashMap` (`fechados`) e pelo `HashSet` (`emAbertos`) para saber se um estado **já foi visto**.

**`children()` (linhas 70–85)**: as regras do jogo. Para cada par de tubos origem `i` e destino `j`:

```java
if (size[i] == 0) continue;                         // origem vazia: não há bola para tirar
char ball = tubes[i][size[i] - 1];                  // a bola do topo da origem
if (j == i || size[j] == height) continue;          // não mover para o mesmo tubo nem para um tubo cheio
if (size[j] > 0 && tubes[j][size[j] - 1] != ball)   // destino não vazio com topo de outra cor: ilegal
    continue;
BallSortLayout child = clone();                     // copia o estado
child.tubes[i][--child.size[i]] = 0;                // tira a bola do topo da origem
child.tubes[j][child.size[j]++] = ball;             // põe a bola no topo do destino
children.add(child);
```

Com `T` tubos há no máximo `T × (T−1)` filhos.

**`isGoal()` (linhas 88–96)**: cada tubo tem de estar **vazio** ou **cheio e de uma só cor**.
- Ignora o argumento `l`, porque o `Main` passa `null` como objetivo: não há uma configuração objetivo única, há uma *condição*.
- Atenção: "cheio" não chega. No Sample 2, o estado inicial tem dois tubos cheios mas misturados, e a resposta é 5, não 0.

**`getK()` (linhas 98–100)**: cada movimento custa 1.

### 3.3 `BestFirst.java`: o algoritmo (igual ao do Tutorial 1)

**`State`** (classe interna): um nó do grafo de procura.
- `layout`: a configuração.
- `father`: o estado de onde veio (`null` no inicial). Permite reconstruir o caminho.
- `g`: custo acumulado desde o início. `g = g do pai + getK()`.

**`sucessores(n)`**: transforma cada filho de `n` num `State` com pai `n`. Não gera o filho que é igual ao avô (desfazer o último movimento), porque isso nunca ajuda.

**`solve(s, goal)`**: o diagrama do tutorial, linha a linha:

```java
abertos = new PriorityQueue<>(..., ordenada por g);   // estados por examinar
fechados = new HashMap<>();                            // estados já expandidos
abertos.add(new State(s, null));                       // começa no estado inicial (g = 0)
while (true) {
    if (abertos.isEmpty()) return null;                // nada mais para explorar: sem solução
    actual = abertos.remove();                         // tira o de menor g
    if (actual.layout.isGoal(objective))
        return path(actual);                           // encontrou: devolve o caminho
    sucs = sucessores(actual);                         // expande
    fechados.put(actual.layout, actual);               // marca como expandido
    for (State suc : sucs)
        if (suc não está em fechados nem em abertos)   // "not presented before"
            abertos.add(suc);
}
```

**A única coisa acrescentada ao tutorial**: o conjunto `emAbertos`. O tutorial diz "insere o sucessor se não estiver em `abertos` nem em `fechados`". Perguntar a uma `PriorityQueue` se contém um elemento é lento (percorre tudo). O `HashSet` guarda as mesmas configurações e responde de imediato. O comportamento é o mesmo; só é mais rápido.

**`path(n)`**: sobe pelos `father` desde o objetivo até ao início e inverte a ordem (`addFirst`), para dar o caminho início → objetivo.

### 3.4 `Main.java`: dado pelo professor (não se mexe)

Lê `H` e `T`, lê `H` linhas, cria o `BallSortLayout`, chama `solve(layout, null)` e imprime o `g` do último estado do caminho, ou `no solution found` se o `solve` devolver `null`.

---

## Parte 4: porque é que a resposta é mesmo a mínima

- A fila `abertos` devolve sempre o estado de **menor `g`**.
- Logo, os estados são examinados por ordem de custo: primeiro todos os de custo 0, depois os de custo 1, depois os de custo 2, etc.
- O primeiro estado objetivo examinado tem portanto o menor custo possível.
- Com custos todos iguais a 1, isto é o mesmo que uma procura em largura (BFS).
- O `fechados` evita repetir trabalho e evita ciclos infinitos (ir e voltar entre dois estados).
- O programa termina sempre: há um número finito de estados e nenhum é examinado duas vezes. Se esgotar todos sem encontrar objetivo, devolve `null`.

Exemplo de "sem solução": `H = 2`, 2 tubos, `R B / B R`. Os dois tubos estão cheios, por isso nenhum movimento é possível e o estado inicial não é objetivo.

---

## Parte 5: perguntas prováveis do professor (com as alterações)

### P1. "E se mover uma bola para um tubo vazio custasse 2?"

O `getK()` é chamado no filho, por isso o filho tem de guardar quanto custou o movimento que o criou.

```java
private double k = 1;                       // novo campo em BallSortLayout

// em children(), antes de children.add(child):
child.k = (size[j] == 0) ? 2 : 1;           // size[j] é do pai: destino estava vazio?

public double getK() { return k; }
```

O `equals`/`hashCode` não usam `k`, por isso dois estados iguais continuam iguais.

**Atenção (o professor pode puxar por isto):** o próprio tutorial diz que o diagrama "só é válido se todos os movimentos tiverem o mesmo custo". Com custos diferentes, um estado pode entrar em `abertos` com um `g` alto e mais tarde ser encontrado por um caminho mais barato. A regra "não inserir se já estiver em `abertos`" deitaria fora o caminho barato.

A correção no `solve`: em vez do conjunto `emAbertos`, guardar o melhor `g` conhecido de cada configuração, deixar entrar um sucessor se for mais barato do que o que já lá está, e ignorar, ao tirar de `abertos`, estados que já foram expandidos:

```java
Map<Ilayout, Double> melhorG = new HashMap<>();   // substitui emAbertos
melhorG.put(s, 0.0);
...
actual = abertos.remove();
if (fechados.containsKey(actual.layout)) continue;   // cópia antiga, mais cara: ignora
...
for (State suc : sucs) {
    Double g = melhorG.get(suc.layout);
    if (!fechados.containsKey(suc.layout) && (g == null || suc.getG() < g)) {
        abertos.add(suc);
        melhorG.put(suc.layout, suc.getG());
    }
}
```

Testado: com esta regra, os exemplos do enunciado dão 1, 6 e 7 (o Sample 2 e o Sample 3 fazem um movimento para um tubo vazio, que agora custa 2).

### P2. "E se o objetivo fosse uma configuração concreta, dada no input?"

```java
public boolean isGoal(Ilayout l) { return this.equals(l); }
```

E o `Main` passaria `new BallSortLayout(objetivo)` em vez de `null` no `solve`. Era assim no 8-puzzle.

### P3. "E se pudéssemos mover várias bolas da mesma cor de uma vez, contando como 1 movimento?" (como no jogo real)

Em `children()`, em vez de mover uma bola, move enquanto o topo da origem for da mesma cor e houver espaço no destino:

```java
BallSortLayout child = clone();
while (child.size[i] > 0 && child.tubes[i][child.size[i] - 1] == ball
       && child.size[j] < height) {
    child.tubes[i][--child.size[i]] = 0;
    child.tubes[j][child.size[j]++] = ball;
}
children.add(child);
```

Testado: o Sample 2 passa de 5 para 4 movimentos.

### P4. "E se houvesse mais cores, ou letras diferentes?"

Não muda nada. O código trata qualquer letra como uma cor; só o `E` tem significado especial.

### P5. "E se os tubos tivessem capacidades diferentes?"

Trocar `int height` por `int[] capacity` (uma capacidade por tubo) e usar `capacity[j]` no `children()` e `capacity[t]` no `isGoal()` e no `toString()`.

### P6. "E se usasse uma fila normal (FIFO) em vez da PriorityQueue?"

```java
abertos = new LinkedList<>();
```

Dá **o mesmo resultado**, porque com custo 1 a ordem por `g` é a ordem de chegada. Isso é a procura em largura (BFS). Só deixa de ser igual se os custos forem diferentes.

### P7. "E se usasse uma pilha (LIFO)?"

Isso é procura em profundidade (DFS). **Deixa de garantir o mínimo**: pode encontrar uma solução longa primeiro.

### P8. "Quantos estados foram expandidos?"

Acrescentar um contador em `solve`:

```java
int expandidos = 0;
...
sucs = sucessores(actual);
expandidos++;
```

Alternativa: no fim, `fechados.size()` é o número de estados expandidos.

### P9. "Para que serve o `if (n.father == null || !e.equals(n.father.layout))` em `sucessores`?"

Evita gerar o estado do avô (desfazer o último movimento). O `fechados` já o apanharia, mas assim nem se cria o objeto.

### P10. "Porque é que precisa do `clone()`?"

Os arrays em Java são partilhados por referência. Sem a cópia profunda, mexer no filho mexia também no pai e em todos os irmãos.

### P11. "Porque é que precisa de `equals` e `hashCode`?"

O `HashMap` e o `HashSet` usam-nos para saber se uma configuração já foi vista. Sem eles, o Java compara a *identidade* dos objetos (o endereço em memória), e dois tabuleiros iguais criados em sítios diferentes pareceriam diferentes. A procura repetiria estados para sempre.

### P12. "Porque é que o `isGoal` recebe um argumento que não usa?"

Porque o método vem da interface `Ilayout`, partilhada com o 8-puzzle, onde o objetivo era uma configuração concreta. Aqui o objetivo é uma condição, e o `Main` passa `null`.

### P13. "Quando é que o programa diz `no solution found`?"

Quando `abertos` fica vazio: todos os estados alcançáveis foram examinados e nenhum é objetivo. O `solve` devolve `null` e o `Main` imprime a mensagem.

### P14. "Como mostrar o caminho completo e não só o número?"

Imprimir cada estado no ciclo do `Main` (é o que o `Main0` faz):

```java
while (it.hasNext()) {
    BestFirst.State i = it.next();
    IO.println(i);
    if (!it.hasNext()) IO.println((int) i.getG());
}
```

### P15. "Que algoritmo é este? É informado ou não informado?"

Procura de custo uniforme, que é uma procura best-first ordenada por `g`. **Não informada**: não usa heurística (o enunciado proíbe heurísticas nesta fase). Com uma heurística `h`, ordenar por `g + h` seria o A* (isso é o Problem 2).

---

## Parte 6: como correr no VS Code

1. Instala o **JDK 25** (ou mais recente) e a extensão **Extension Pack for Java**.
2. Abre a pasta `IA-Problem1-BallSort/submission`.
3. No terminal:
   ```bash
   javac Main.java
   java Main
   ```
4. Escreve o input (por exemplo `3 3`, `R B E`, `B B E`, `R R E`) e carrega Enter. Deve aparecer `5`.

Para ver o caminho completo, troca o `Main` pelo `Main0` (em `test/Main0.java.txt`).
