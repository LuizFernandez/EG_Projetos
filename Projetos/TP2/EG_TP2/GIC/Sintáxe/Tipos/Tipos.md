[[Regras Sintáticas#^b5446b|Regras Sintáticas]]
*** 
Os tipos básicos que a linguagem apresenta podem ser divididos em dois grupos:
- [[Tipos primitivos]];
- [[Tipos compostos]];

Os tipos primitivos, são valores únicos, neste caso, uma variável desse tipo, apresenta um único valor associado.

	 int x = 0; // x apenas apresenta o valor de 0

Os tipos compostos, são constituídos por valores de tipos primitivos, podendo apresentar mistura de tipos. Variáveis destes tipos são também denominadas por coleções, devido à sua natureza de conter múltiplos valores associados a si.

	 list l = [1,2,3,"Hello", 3.4] // Uma lista de inteiros, strings, e floats

Os tipos terão a seguinte estrutura:

```
type: primitive_type
	| complex_type
```

Conforme a evolução da GIC, alterar o comportamento conforme necessário