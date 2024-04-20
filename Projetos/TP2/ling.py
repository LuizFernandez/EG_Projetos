from lark import Lark
from LingInterpreter import MyInterpreter

def var_table_output(data):
    file = open("./Tables/vars.md", "w")

    # Var Table in Markdown
    file.write("| Nome da Variável | Tipo | Valor | Usada |\n")
    file.write("|------------------|------|-------|-------|\n")
    for key in data.keys():
        file.write(f"|{key}|{data[key]['type']}|{data[key]['value']}|{data[key]['used']}|\n")

    file.close()

def error_table_output(errors):
    file = open("./Tables/error.md", "w")

    # Error Table in Markdown
    file.write("| Variable | Type | Description |\n")
    file.write("|----------|------|-------------|\n")
    for erro in erros:
        file.write(f"{erro['variable']}|{erro['type']}|{erro['description']}\n")

    file.close()


with open("grammar.txt","r") as file:
    grammar = file.read()

with open("./Exemplos/VarsExample.txt") as file:
    exemple = file.read()

p = Lark(grammar) # cria um objeto parser

tree = p.parse(exemple)  # retorna uma tree
(data, erros) = MyInterpreter().visit(tree)

var_table_output(data)
error_table_output(erros)
