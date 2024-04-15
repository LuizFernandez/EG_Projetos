[[Tipos]]
***
Tipos compostos são também definidos como coleções. Variáveis associadas a estes tipos, são multi valoradas, isto é, apresentam uma coleção de valores do mesmo tipo primitivo ou tipo compostos.

Este tipo apresentam diferentes tipos de coleções, sendo que cada uma apresenta o seu próprio comportamento  e o seu método de inicialização:
- Listas:
	- [] => Inicializar uma lista a vazio
	- [valor*] => Inicializar uma lista com elementos
	- list(coleção) =>Cria uma lista com base uma outra coleção (Apenas funciona para arrays, set, etc.)
- Sets:
	- set() => Inicializa uma set a vazio
	- set(coleção) => Cria um set, baseado noutra coleção (Apenas arrays e listas)
- Array:
	- array(n) => Inicializa um array com tamanho n
	- array(coleção) => Recebe uma outra coleção e criar um array estático com os seus elementos
- Tuplo:
	- () => Inicializa um tuplo vazio
	- (valor, valor) => Tuplo com dois valores

O **GIC** do tipo é a seguinte:

```
complex_type : COMPLEX_TYPE
```

Tal como no tipos primitivos, a definição do tipo complexo fica a cabo das regras léxicas. 
**Nota**: Formato pode estar sujeito a alterações