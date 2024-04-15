[[Road Map]]
***

Construir uma tabela que vai conter as informações relativas às variáveis presentes no ficheiro.
Comportamento da tabela é restringido por regras:
- Não pode haver nomes de variáveis repetidos;
- Guardar posição de declaração e associação;
- Valor atual da variável;
- Valor tem que corresponder ao tipo que lhe foi atribuída;
- Uma associação não pode ocorrer antes de uma declaração, mas podem ocorrer ambas ao mesmo tempo (Y >= X);
- Pode ocorrer múltiplas associações, logo valor e associação tem a ocorrência mais recente;

| Tipo         | Nome             | Valor       | Declaração | Associação | Visão        | Local |
| ------------ | ---------------- | ----------- | ---------- | ---------- | ------------ | ----- |
| nome do tipo | nome da variável | valor atual | Linha X    | Linha Y    | Local/Global |       |

Descrição da tabela:
- **Tipo** => Tipo da variável;
- **Nome** => Nome da variável;
- **Valor** => Valor atual da variável;
- **Declaração** => Quando a variável é criada;
- **Associação** => Posição sempre que recebe um novo valor;
- **Visão** => Grau de visibilidade dentro do código;
	- Declarada dentro de uma função => Local;
	- Declarada fora de uma função => Global;
- **Local** => Depende da visão
	- Visão Local => nome da função;
	- Visão global => Vazio pois pode ser usada em qualquer sitio;

Objetivo da tabela:
- Manter um estado atualizado das variáveis usadas;
- Dar sugestões quando ocorrem problemas de tipagem ou de nomes de variáveis;
- Quando está fora do seu alcance