from collections import defaultdict

def last_if(statment):
    last_if = None
    for elem in reversed(statment):
        if elem.startswith("if("):
            last_if = elem
            break
    return last_if

def create_cfg_graph(structure):
    graph = "digraph G {\n"
    cycle = None
    for node_id, statment in structure.items():
        if statment == "fim":
            pass

        elif isinstance(statment, str):
            if isinstance(structure[node_id+1], str):
                if cycle:
                    graph += f'  "{cycle}" -> "{statment}" [label="false"]\n'
                    cycle = None
                graph += f'  "{statment}" -> "{structure[node_id+1]}"\n'
            elif "IGNORE" not in structure[node_id+1]:
                graph += f'  "{statment}" -> "{structure[node_id+1][0]}"\n'
            else:
                graph += f'  "{statment}" -> "{last_if(structure[node_id+1])}"\n'

        elif isinstance(statment, list):
            print(statment)
            print('while' in statment)
            if "else" in statment:
                if statment.count("else") == 1:
                    index_of_else = statment.index('else')
                    if_list = statment[:index_of_else]
                    else_list = statment[index_of_else:]

                    if len(if_list) > 1:
                        graph += f'  "{statment[0]}" -> "{if_list[1]}" [label="true"]\n'
                        if len(if_list) > 2:
                            ant_stat = if_list[1]

                            for elem in if_list[2:]:
                                    graph += f'  "{ant_stat}" -> "{elem}"\n'
                                    ant_stat = elem
                        if isinstance(structure[node_id+1], str):
                            graph += f'  "{if_list[-1]}" -> "{structure[node_id+1]}"\n'
                        elif "IGNORE" not in structure[node_id+1]:
                            graph += f'  "{if_list[-1]}" -> "{structure[node_id+1][0]}"\n'
                        else:
                            graph += f'  "{if_list[-1]}" -> "{last_if(structure[node_id+1])}"\n'
                    else:
                        if isinstance(structure[node_id+1], str):
                            graph += f'  "{statment[0]}" -> "{structure[node_id+1]}" [label="true"]\n'
                        elif "IGNORE" not in structure[node_id+1]:
                            graph += f'  "{statment[0]}" -> "{structure[node_id+1][0]}"\n'
                        else:
                            graph += f'  "{statment[0]}" -> "{last_if(structure[node_id+1])}"\n'
  

                    if len(else_list) > 1:
                        graph += f'  "{statment[0]}" -> "{else_list[1]}" [label="false"]\n'
                        if len(else_list) > 2:
                            ant_stat = else_list[1]

                            for elem in else_list[2:]:
                                graph += f'  "{ant_stat}" -> "{elem}"\n'
                                ant_stat = elem
                        if isinstance(structure[node_id+1], str):
                            graph += f'  "{else_list[-1]}" -> "{structure[node_id+1]}"\n'
                        elif "IGNORE" not in structure[node_id+1]:
                            graph += f'  "{else_list[-1]}" -> "{structure[node_id+1][0]}"\n'
                        else:
                            graph += f'  "{else_list[-1]}" -> "{last_if(structure[node_id+1])}"\n'
                    else:
                        if isinstance(structure[node_id+1], str):
                            graph += f'  "{statment[0]}" -> "{structure[node_id+1]}" [label="false"]\n'
                        elif "IGNORE" not in structure[node_id+1]:
                            graph += f'  "{statment[0]}" -> "{structure[node_id+1][0]}"\n'
                        else:
                            graph += f'  "{statment[0]}" -> "{last_if(structure[node_id+1])}"\n'

                else:
                    if_lists = []
                    else_list = [] 
                    for index, elem in enumerate(statment):
                        create_list = []
                        if elem.startswith("if("):
                            create_list.append(elem)
                            for value in statment[(index + 1):]:
                                if value.startswith("if(") or value == "else":
                                    break
                                create_list.append(value)
                            if_lists = [create_list] + if_lists
                        elif elem == "else":
                            if statment[(index + 1)] != "IGNORE":
                                create_list.append(elem)
                                for value in statment[(index + 1):]:
                                    if value.startswith("if(") or value == "else":
                                        break
                                    create_list.append(value)
                                else_list = create_list

                    for index, if_list in enumerate(if_lists):
                        if len(if_list) > 1:
                            graph += f'  "{if_list[0]}" -> "{if_list[1]}" [label="true"]\n'
                            if len(if_list) > 2:
                                ant_stat = if_list[1]

                                for elem in if_list[2:]:
                                        graph += f'  "{ant_stat}" -> "{elem}"\n'
                                        ant_stat = elem
                            if isinstance(structure[node_id+1], str):
                                graph += f'  "{if_list[-1]}" -> "{structure[node_id+1]}"\n'
                            elif "IGNORE" not in structure[node_id+1]:
                                graph += f'  "{if_list[-1]}" -> "{structure[node_id+1][0]}"\n'
                            else:
                                graph += f'  "{if_list[-1]}" -> "{last_if(structure[node_id+1])}"\n'

                            if index + 1 <= len(if_list):
                                graph += f'  "{if_list[0]}" -> "{if_lists[index + 1][0]}" [label="false"]\n'
                            elif else_list != [] and len(else_list) > 1:
                                graph += f'  "{if_list[0]}" -> "{else_list[1]}" [label="false"]\n'
                                if len(else_list) > 2:
                                    ant_stat = else_list[1]

                                    for elem in else_list[2:]:
                                            graph += f'  "{ant_stat}" -> "{elem}"\n'
                                            ant_stat = elem
                                if isinstance(structure[node_id+1], str):
                                    graph += f'  "{else_list[-1]}" -> "{structure[node_id+1]}"\n'
                                elif "IGNORE" not in structure[node_id+1]:
                                    graph += f'  "{else_list[-1]}" -> "{structure[node_id+1][0]}"\n'
                                else:
                                    graph += f'  "{else_list[-1]}" -> "{last_if(structure[node_id+1])}"\n'
                            else:
                                graph += f'  "{if_list[0]}" -> "{structure[node_id+1][0]}" [label="false"]\n'                       
            else:
                print("AAAAAAAA")
                if len(statment) > 1:
                    graph += f'  "{statment[0]}" -> "{statment[1]}" [label="true"]\n'
                    if ('while' in statment[0]):
                        cycle = statment[0]
                    if len(statment) > 2:
                        ant_stat = statment[1]
                        for elem in statment[2:]:
                                graph += f'  "{ant_stat}" -> "{elem}"\n'
                                ant_stat = elem
                        if isinstance(structure[node_id+1], str):
                            if cycle:
                                graph += f'  "{statment[-1]}" -> "{cycle}"\n'
                            else:
                                graph += f'  "{statment[-1]}" -> "{structure[node_id+1]}"\n'
                        elif "IGNORE" not in structure[node_id+1]:
                            graph += f'  "{statment[-1]}" -> "{structure[node_id+1][0]}"\n'
                        else:
                            graph += f'  "{statment[-1]}" -> "{last_if(structure[node_id+1])}"\n'
                else:
                    if isinstance(structure[node_id+1], str):
                        graph += f'  "{statment[0]}" -> "{structure[node_id+1]}"\n'
                    elif "IGNORE" not in structure[node_id+1]:
                        graph += f'  "{statment[0]}" -> "{structure[node_id+1][0]}"\n'
                    else:
                        graph += f'  "{statment[0]}" -> "{last_if(structure[node_id+1])}"\n'

            

    for node_id, statment in structure.items():
        if isinstance(statment, list) and "IGNORE" not in statment:
            graph+= f'  "{statment[0]}" [shape=diamond];\n'
        elif isinstance(statment, list):
            for elem in statment:
                if elem.startswith("if("):
                    graph+= f'  "{elem}" [shape=diamond];\n'
            
        
    # Close the graph
    graph += "}\n"

    return graph

