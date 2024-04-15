[[GIC#^d93f55|GIC]]
***
Usando como exemplos as linguagens *Python* e *C*, define-se uma estrutura em que:
- não é necessário uma **função _main_** para que a execução do ficheiro seja inicializada;
- nem a **indentação** necessária para formar o corpo de uma função/ciclo/seleção.
- todas as variáveis e funções são tipadas;

Relativamente a outros aspetos que necessitam de estar implementados na **LI**:

- [[Tipos]]: ^b5446b

| Tipos                         | Significado                                                                          | Exemplos                 |
| ----------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| [[Tipos Primitivos]]          | Tipos simples da LI                                                                  | Int, String, Bool, Float |
| [[Tipos Compostos\|Coleções]] | Tipos complexos que são constituídos por uma coleção de tipos primitivos ou Coleções | Array, Set, List, Tuple  |


- **Declaração**, **Atribuição**, **Leitura**, **Escrita**;

| Classificação                           | Signidicado                 | Estrutura |
| --------------------------------------- | --------------------------- | --------- |
| [[Atribuição de Valores\|Atribuição]]   | Dar um valor a uma variável | x = 0     |
| Leitura                                 | Ler do input                | read()    |
| Escrita                                 | Escrever no output          | write()   |
| [[Declaração de Variáveis\|Declaração]] | Declarar uma variável       | tipo x    |
 - **Seleção**: 

| Estrutura         | Significado                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| if...             | Se algo verdadeiro executa x                                                    |
| if...else...      | Se algo verdadeiro executa x, senão executa y                                   |
| switch... case... | Verifica algo, e verifica em qual corpo *case* faz *match* e executa esse corpo |

- **Repetição**: 

| Estrutura  | Significado                                                                |
| ---------- | -------------------------------------------------------------------------- |
| foreach    | Percorrer todos os elementos de uma coleção                                |
| while      | Executar o corpo enquanto uma condição for verdadeira                      |
| do...while | Executa algo e testa se a condição se verifica e torna a executar em ciclo |
| for        | Executar um corpo num intervalo                                            |
- [[Operações]]:

| Símbolo/função | Significado                    | Exemplo                  |
| -------------- | ------------------------------ | ------------------------ |
| +              | Soma                           | 1 + 1 = 2                |
| -              | Subtração                      | 2 - 1 = 1                |
| *              | Multiplicação                  | 2 * 2 = 4                |
| /              | Divisão                        | 1 / 2 = 0.5              |
| %              | Resto                          | 3 % 2 = 1                |
| ^              | Potência                       | 2^2 = 4                  |
| []             | Acesso array                   | array[2]                 |
| cons           | Adicionar à cabeça             | cons(x,l) = [x\|l]       |
| snoc           | Adicionar à cauda              | snoc(x, l) = [l\|x]      |
| in             | Verificar se pertence ao grupo | x in [h\|t] = True/False |
| head           | Cabeça da Lista                | head([h\|t]) =h          |
| tail           | Cauda da Lista                 | tail([h\|t]) = t         |
| .              | Selecionar campo               | l.size                   |

- **Funções** com **parâmetro** e **Retorno**;

| Tipo                 | Significado                                                                                             | Estrutura                      |
| -------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------ |
| Declaração de função | Declarar o comportamento da função (corpo), que argumentos recebe (parâmetros) e se retorna algo ou não | def nome_função (args) {corpo} |
| Chamar função        | Chamar uma função para ser executada                                                                    | nome_função(args)              |
| Retorno              | Retorna algo numa função                                                                                | return x                       |
***

Como é utilizada a biblioteca *Lark*, a primeira regra a ser lida é a *start*, está é que dá inicio à análise da LI, assim sendo:

```
// Regras sintáticas
start: statments*
```

Todos os requisitos mencionados anteriormente, apresentam algo em comum, todos podem ser chamados no ficheiro, sem estarem num função, como acontece em *Python*.

Assim sendo, como podem aparecer múltiplas vezes, deduz-se que um ficheiro é constituído por zero ou mais declarações ([[Statments|statments]]).

