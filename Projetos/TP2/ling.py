from lark import Lark
from LingInterpreter import MyInterpreter

with open("grammar.txt","r") as file:
    grammar = file.read()

with open("./Exemplos/VarsExample.txt") as file:
    frase1 = file.read()

p = Lark(grammar) # cria um objeto parser

tree = p.parse(frase1)  # retorna uma tree
(data, erros) = MyInterpreter().visit(tree)

# Var Table in Markdown
print("| Nome da Variável | Tipo | Valor | Usada | Declarada |")
print("|------------------|------|-------|-------|-----------|")
for key in data.keys():
    print(f"|{key}|{data[key]['type']}|{data[key]['value']}|{data[key]['used']}|{data[key]['declared']}")

print()

# Error Table in Markdown
print("| Erro | Tipo |")
print("|------|------|")
for erro in erros:
    print(f"{erro['error']}|{erro['type']}")