[[Statments]]
***
Só é possível atribuir valores a variáveis previamente declaradas.

Uma atribuição pode ocorrer numa:
- Declaração de uma variável, ao criar a variável atribuir um valor inicial;
	- Contudo, com maneira de simplificar a atribuição, a regra sintática de uma declaração apresenta o caso de inicialização da variável;
- Durante o ciclo de vida da variável:
	- Pode ser um valor inicial, no caso na sua declaração não ter recebido uma;
	- Ou uma re-atribuição de um valor, ou seja, a variável está a ser atualizada;

Para abrangir ambas as situações, as sua regras sintática apresenta o seguinte formato:

```
atribution: ID "=" value
```

**ID** é o nome da variável a receber o valor;
[[Valores|value]] é o novo valor da variável;