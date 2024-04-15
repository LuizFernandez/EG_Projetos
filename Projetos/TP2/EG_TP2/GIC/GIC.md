## Gramática Independente de Contexto
***
A especificação da **GIC** é constituída pelas regras sintáticas (regras sobre a estrutura da LI), e as regras léxicas (regras sobre os *Tokens*). 
***

A **GIC** estará dividida em duas partes:
	1. [[Regras Léxicas]];
	2. [[Regras Sintáticas]];

Nas **Regras Léxicas** estão definidas os *Tokens* da linguagem, isto é:
- Palavras reservadas (não podem ser usadas fora do seu contexto);
- Definição de tipos (*int* são números, *string* são palavras, etc.);
- Formato que os nomes das variáveis/funções podem tomar;
- etc (Conforme o trabalho evolua, adicionar a esta parte);

Nas **Regras Sintáticas** estão definidas as regras sobre a estrutura da LI. As regras estão definidas consoante o seu intuito, isto é, o que é pretendido obter/declarar com aquele formato de texto. ^d93f55

**Exemplo**: *declaration*, declaração de uma nova variável.

```
declaration: type ID ( | "=" value)
```

**Nota**: A definição das restantes regras verá a seu tempo.

```
body: cycle
    | atribution
    | selection  

value: function
     | ID "[" ( NUMBER | ID | function ) "]"
     | operation -> value_operation
     | ID "." function
     | function "." function

operation: value ("+"|"-"|"*"|"/"|"%"|"^") value
         | value (">"|"<"|">="|"<="|"=="|"&&"|"||"|"!=") value
         | value "in" ( ID | function )

type: TYPE

definition: "def" ID "(" ( | arguments) ")" "{" statment* ("return" value)? "}"

function: ID "(" ( | value ("," value)* ) ")"
        | "cons" "(" value "," ( ID | function ) ")"
        | "snoc" "(" value "," ( ID | function ) ")"
        | "head" "(" ( ID | function ) ")"
        | "tail" "(" ( ID | function ) ")"

arguments: argument ("," argument)*

argument: type ID

selection: "if" "(" value ")" "{" body* ( "break" | "return" value )?"}"
         | "if" "(" value ")" "{" body* ( "break" | "return" value )? "}" "else" ( "if" "(" value ")" "{" body* ( "break" | "return" value )? "}" "else")* "{" body* ( "break" | "return" value )? "}"
         | "switch" "(" value ")" "{" ("case" (NUMBER|STRING) ":" "{" ( body )* "break"?  "};")+ "default" ":" "{" ( body )* "}"

cycle: "while" "(" (value)+ ")" "{" ( body )* "}"
     | "do" "{" ( body )* "}" "while" "(" (value)+ ")"
     | "for" ID "in" ( collection | ID | function ) "{" ( body )* "}"


```

