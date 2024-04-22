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

def type_table_output(types):
    file = open("./Tables/types.md", "w")

    # Total de varíaveis declaradas por cada Tipo de dados usados
    file.write("| Type | Vars | Number |\n")
    file.write("|------|------|--------|\n")
    for type, vars in types.items():
        str_vars = ""
        for v in vars:
            str_vars += f"{v}, "
        str_vars = str_vars[:-2]
        file.write(f"{type}|{str_vars}|{len(vars)}\n")

    file.close()

def count_table_output(count):
    file = open("./Tables/count.md", "w")

    # otal de instruções que formam o corpo do program
    file.write("| Type | Number |\n")
    file.write("|------|--------|\n")
    for type, number in count.items():
        file.write(f"{type}|{number}\n")

    file.close()


with open("grammar.txt","r") as file:
    grammar = file.read()

with open("./Exemplos/VarsExample.txt") as file:
    exemple = file.read()

p = Lark(grammar) # cria um objeto parser

tree = p.parse(exemple)  # retorna uma tree
(data, erros, types, count, nesting, sub_ifs) = MyInterpreter().visit(tree)

var_table_output(data)
error_table_output(erros)
count_table_output(count)
type_table_output(types)
print("Quantidade de situações em que estruturas de controlo surgem aninhadas em outras estruturas de controlo do mesmo ou de tipos diferentes:", nesting)
print("Lista de ifs aninhados que podem ser substituídos por um só if", sub_ifs)