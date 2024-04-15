***
Valores Compostos são valores associados a tipos compostos.

Os seus formatos variam muito consoante o tipo composto, como também a sua utilidade.

Tipo/Valor:
- List:
	- Construtor vazio => []
	- Construtor com elementos => [números/string/bool/outros valores compostos]
	- Construtor função => list()
		- Função pode receber => um set e transforma numa lista, ou um array e transforma numa lista
- Sets:
	- Construtor vazio => set()
		- Pode receber uma outra coleção, mas aplica as regras dos sets
- Tuplo:
	- Construtor vazio => ()
	- Construtor com valores => (valor1, valor2)
		- Só pode apresentar dois valores por tuplo
		- Não precisam de ser do mesmo tipo
- Array:
	- Construtor simples => array(n), n é o tamanho do array
	- Construtor baseado noutra coleção => transforma uma outra coleção num array

Regra Sintática:

```
complex_value : list_construct
			  | set_construct
			  | tuple_construct
			  | array_construct

list_construct : LRPAR RRPAR
			   | LRPAR value (, value)* RRPAR
			   | "list(" ID ")" # ID apenas pode ser do tipo arrary ou set                                      mas tem que ser uma variável

set_construct : "set()"
			  | "set(" ID ")"
			  
tuple_cosntruct : LPAR RPAR
				| LPAR value VIRG value RPAR

array_construct : "array(" INT ")"
				| "array(" ID ")" # ID é uma vairável do tipo lista, set ou tuple
 
``` 
