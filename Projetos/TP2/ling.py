from lark import Lark
from LingInterpreter import MyInterpreter
from GraphInterpreter import GraphInterpreter
from Graphfunctions import create_cfg_graph
import graphviz
import re

def buildVariaveis(data):
    file = open("./Tables/vars.md", "w")

    # Var Table in Markdown
    file.write("| Nome da Variável | Tipo | Valor | Usada |\n")
    file.write("|------------------|------|-------|-------|\n")

    html_content = "<h2>Variables and Types Used</h2>"
    html_content += "<table border='1'><tr>"
    
    # Add table headers
    html_content += "<th>Variable Name</th> <th>Type</th> <th>Value</th> <th>Used?</th>"
    html_content += "</tr>"
    
    # Add table rows
    for key in data.keys():
        file.write(f"|{key}|{data[key]['type']}|{data[key]['value']}|{data[key]['used']}|\n")
        html_content += "<tr>"
        html_content += "<td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>".format(key,data[key]['type'],data[key]['value'],data[key]['used'])
        html_content += "</tr>"
    file.close()
    
    html_content += "</table></body>"

    return html_content

def buildErros(erros):
    file = open("./Tables/error.md", "w")

    # Error Table in Markdown
    file.write("| Variable | Type | Description |\n")
    file.write("|----------|------|-------------|\n")

    html_content = "<h2>Errors</h2>"
    html_content += "<table border='1'><tr>"

    # Add table headers
    html_content += "<th style='background-color: #8B0000; color: white;'>Variable</th> <th style='background-color: #8B0000; color: white;'>Type</th> <th style='background-color: #8B0000; color: white;'>Description</th>"
    html_content += "</tr>"

    # Add table rows
    for erro in erros:
        file.write(f"{erro['variable']}|{erro['type']}|{erro['description']}\n")
        html_content += "<tr>"
        html_content += "<td>{}</td> <td>{}</td> <td>{}</td>".format(erro['variable'],erro['type'],erro['description'])
        html_content += "</tr>"

    file.close()

    html_content += "</table></body>"

    return html_content

def buildTipos(types):
    file = open("./Tables/types.md", "w")

    # Total de varíaveis declaradas por cada Tipo de dados usados
    file.write("| Type | Vars | Number |\n")
    file.write("|------|------|--------|\n")

    html_content = "<h2>Number of Variables Declared per Type</h2>"
    html_content += "<table border='1'><tr>"
    
    # Add table headers
    html_content += "<th>Type</th> <th>Vars</th> <th>Number</th>"
    html_content += "</tr>"
    
    # Add table rows
    for type, vars in types.items():
        str_vars = ""
        html_content += "<tr>"
        for v in vars:
            str_vars += f"{v}, "
        str_vars = str_vars[:-2]
        file.write(f"{type}|{str_vars}|{len(vars)}\n")
        html_content += "<td>{}</td> <td>{}</td> <td>{}</td>".format(type,str_vars,len(vars))
        html_content += "</tr>"
    
    file.close()

    html_content += "</table></body>"

    return html_content

def buildCount(count):
    file = open("./Tables/count.md", "w")

    # total de instruções que formam o corpo do program
    file.write("| Type | Number |\n")
    file.write("|------|--------|\n")

    html_content = "<h2>Number of Instructions Found in the Code</h2>"
    html_content += "<table border='1'><tr>"
    
    # Add table headers
    html_content += "<th>Type</th> <th>Number</th>"
    html_content += "</tr>"
    
    # Add table rows
    for type, number in count.items():
        file.write(f"{type}|{number}\n")
        html_content += "<tr>"
        html_content += "<td>{}</td> <td>{}</td>".format(type.capitalize(),number)
        html_content += "</tr>"
    
    file.close()

    html_content += "</table></body>"

    return html_content

def buildNesting(nesting):
    html_content = "<h2>Number of Control Structures Nested Within Other Control Structures</h2>"
    html_content += "<ul>"
    html_content += "<li><p style='font-size:24px;'>Found <b>{}</b> nested control structures.</p></li>".format(nesting)
    html_content += "</ul>"
    return html_content

def buildSubIf(sub_ifs):
    html_content = "<h2>Nested 'If' Conditions That Can be Combined</h2>"
    html_content += "<table border='1'><tr>"
    
    
    # Determine the number of conditions in the largest sublist
    if len(sub_ifs) > 0:
        max_conditions = max(len(sublist) for sublist in sub_ifs)
    else:
        max_conditions = 0
    
    # Add table headers based on the number of conditions
    for i in range(max_conditions):
        html_content += "<th>Condition Nº{}</th>".format(i+1)
    html_content += "<th>Suggestion</th></tr>"
    
    # Add table rows
    for sublist in sub_ifs:
        html_content += "<tr>"
        #for condition in sublist:
        #   html_content += "<td>if {}</td>".format(condition)
        for i in range(0,max_conditions):
            if i in range(0,len(sublist)):
                condition = sublist[i]
                html_content += "<td>if {}</td>".format(condition)
            else:
                html_content += "<td>N/A</td>"
        suggestion = " and ".join(sublist)
        html_content += "<td>if {}</td>".format(suggestion)
        html_content += "</tr>"
    
    html_content += "</table></body>"

    return html_content

def buildCFG(structure):
    # Define the graph
    graph = graphviz.Digraph(format='png')
    pattern = r'("[^"]+")\s+\[(\w+)=\"?(\w+)\"?\]'
    label = ''

    # Parse the graph data and add nodes and edges
    for line in structure.split('\n'):
        if line.strip():
            # Se for um edge/ligação
            if '->' in line:
                parts = line.strip().split(' -> ')
                if len(parts) == 2:
                    node1, node2 = parts
                    # se for so dois nodos
                    if node2.startswith('"') and node2.endswith('"'):
                        graph.node(node2[1:-1])
                    # se houver info adicional (label)
                    else:
                        match = re.match(pattern, node2)
                        node2 = match.group(1)
                        #print(node2)
                        atribute = match.group(2)
                        value = match.group(3)
                        if 'label' in atribute:
                            label = value
                        else:
                            graph.node(node2[1:-1])
                    graph.node(node1[1:-1])
                    # se for necessário acresncentar label 
                    if label != '':
                        graph.edge(node1[1:-1], node2[1:-1],label=label)
                        label = ''
                    else:
                        graph.edge(node1[1:-1], node2[1:-1])
            # caso seja info adicional de nodo ou nodo isolado
            else:
                match = re.match(pattern, line.strip())
                if match:
                    node = match.group(1)
                    atribute = match.group(2)
                    value = match.group(3)
                    if 'shape' in atribute:
                        graph.node(node[1:-1],shape=value)
                    else:
                        graph.node(node[1:-1])

    # Render the graph
    graph.render('graph')
    
    html_content = "<h2>CFG Graph of the code</h2>"
    html_content += '<img src="graph.png" alt="Graph">'

    return html_content

def buildHTML(data,erros,count,types,nesting,sub_ifs,structure):
    html_content = "<html><head><title>Analysis Result</title><style>"
    html_content += "body {font-family: Arial, sans-serif;}"
    html_content += "h2 {color: #333;}"
    html_content += "table {border-collapse: collapse; width: 100%; margin-top: 20px;}"
    html_content += "th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}"
    html_content += "th {background-color: #4CAF50; color: white;}"
    html_content += "ul {list-style-type: none; padding: 0;}"
    html_content += "li {margin-bottom: 10px;}"
    html_content += ".error-table {background-color: #ffcccc;}"
    html_content += "</style></head><body>"
    html_content += buildVariaveis(data)
    html_content += buildErros(erros)
    html_content += buildTipos(types)
    html_content += buildCount(count)
    html_content += buildNesting(nesting)
    html_content += buildSubIf(sub_ifs)
    html_content += buildCFG(structure)
    html_content += "</html>"
    
    # Write HTML content to a file
    with open('analise.html', 'w') as file:
        file.write(html_content)

    print("\nFicheiro HTML gerado com sucesso, os resultados da análise encontram-se no ficheiro 'analise.html'.")

with open("grammar.txt","r") as file:
    grammar = file.read()

with open("grammarGraph.txt","r") as file:
    grammarGraph = file.read()

with open("./Exemplos/ifelse.txt") as file:
    exemple = file.read()

p = Lark(grammar) # cria um objeto parser

tree = p.parse(exemple)  # retorna uma tree
(data, erros, types, count, nesting, sub_ifs) = MyInterpreter().visit(tree)

p = Lark(grammarGraph) # cria um objeto parser

tree = p.parse(exemple)  # retorna uma tree
structure = GraphInterpreter().visit(tree)
print(create_cfg_graph(structure))

#print("Quantidade de situações em que estruturas de controlo surgem aninhadas em outras estruturas de controlo do mesmo ou de tipos diferentes:", nesting)
#print("Lista de ifs aninhados que podem ser substituídos por um só if", sub_ifs)

buildHTML(data,erros,count,types,nesting,sub_ifs,create_cfg_graph(structure))