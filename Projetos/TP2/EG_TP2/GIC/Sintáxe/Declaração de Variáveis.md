[[Statments]]
***
Na nova linguagem de programação imperativa, uma **declaração**, não necessitam obrigatoriamente de um valor inicial, a única obrigação que existem é a definição de um tipo.

A sua estrutura é a seguinte:

	 tipo nome_variável

A estrutura anterior é a **base** por detrás de uma declaração de uma variável. No caso, em que se deseja atribuir um **valor inicial** a uma variável, quando esta está a ser declarada, a **declaração** apresenta o seguinte formato:

	 tipo nome_variável = valor

Assim sendo, as declarações de variáveis podem ser traduzidas no seguinte:

```
declaration: type ID ( | "=" value)
```

- [[Tipos|Tipo]] terá as suas regras sintáticas;
- **ID** terá regras léxicas aplicadas; 
- [[Valores|Value]] terá as suas regras sintáticas; 
