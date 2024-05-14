from collections import defaultdict

def create_cfg_graph(structure):
    print(structure)
    graph = "digraph G {\n"
    for node_id, statement in structure.items():
        if statement == "fim":
            pass

        elif isinstance(statement, str):
            if isinstance(structure[node_id+1], str):
                graph += f'  "{statement}" -> "{structure[node_id+1]}"\n'
            else:
                graph += f'  "{statement}" -> "{structure[node_id+1][0]}"\n'

        elif isinstance(statement, list):
            if "else" in statement:
                index_of_else = statement.index('else')
                if_list = statement[:index_of_else]
                else_list = statement[index_of_else:]

                if len(if_list) > 1:
                    graph += f'  "{statement[0]}" -> "{if_list[1]}" [label="true"]\n'
                    if len(if_list) > 2:
                        ant_stat = if_list[1]

                        for elem in if_list[2:]:
                                graph += f'  "{ant_stat}" -> "{elem}"\n'
                                ant_stat = elem
                if isinstance(structure[node_id+1], str):
                    graph += f'  "{if_list[-1]}" -> "{structure[node_id+1]}"\n'
                else:
                    graph += f'  "{if_list[-1]}" -> "{structure[node_id+1][0]}"\n'

                if len(else_list) > 1:
                    graph += f'  "{statement[0]}" -> "{else_list[1]}" [label="false"]\n'
                    if len(else_list) > 2:
                        ant_stat = else_list[1]

                        for elem in else_list[2:]:
                            graph += f'  "{ant_stat}" -> "{elem}"\n'
                            ant_stat = elem
                        if isinstance(structure[node_id+1], str):
                            graph += f'  "{else_list[-1]}" -> "{structure[node_id+1]}"\n'
                        else:
                            graph += f'  "{else_list[-1]}" -> "{structure[node_id+1][0]}"\n'

            else:
                if len(statement) > 1:
                    graph += f'  "{statement[0]}" -> "{statement[1]}" [label="true"]\n'
                    if len(statement) > 2:
                        ant_stat = statement[1]

                        for elem in statement[2:]:
                                graph += f'  "{ant_stat}" -> "{elem}"\n'
                                ant_stat = elem
                        if isinstance(structure[node_id+1], str):
                            graph += f'  "{statement[-1]}" -> "{structure[node_id+1]}"\n'
                        else:
                            graph += f'  "{statement[-1]}" -> "{structure[node_id+1][0]}"\n'
                else:
                    if isinstance(structure[node_id+1], str):
                        graph += f'  "{statement[0]}" -> "{structure[node_id+1]}"\n'
                    else:
                        graph += f'  "{statement[0]}" -> "{structure[node_id+1][0]}"\n'

            

    for node_id, statement in structure.items():
        if isinstance(statement, list):
            graph+= f'  "{statement[0]}" [shape=diamond];\n'
    # Close the graph
    graph += "}\n"

    return graph

