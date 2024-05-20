from collections import defaultdict

conditions = []

def true_value(tuple, declarations, attributions, selections, cycle):

    match (tuple[0]):
        case "declaration":
            return declarations["statments"][tuple[1]]
        case "attribution":
            return attributions["statments"][tuple[1]]
        case "ifs":
            return selections["statments"][tuple[1]]["condition"]
        case "ifelses":
            return selections["statments"][tuple[1]]["condition"]
        case "while":
            return cycle["statments"][tuple[1]]["condition"]
        case _:
            return ""
    
def nesting(tuple, next_value, declarations, attributions, selections, cycle):
    graph = ""
     
    match (tuple[0]):
        case "ifs":
            condition = selections["statments"][tuple[1]]["condition"]
            conditions.append(condition)
            body = selections["statments"][tuple[1]]["body"]
            if len(body) > 0:
                ant = body[0]
                value = true_value(ant, declarations, attributions, selections, cycle)
                graph += f'"{condition}" -> "{value}" [label="true"]\n'
                if len(body) > 1:
                    for elem in body[1:]:
                        elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                        match (ant[0]):
                            case "declaration" | "attribution" :
                                graph += f'"{value}" -> "{elem_value}"\n'
                            case "ifs" | "ifelses" | "while":
                                graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                        ant = elem
                        value = elem_value
                    match (body[-1][0]):
                        case "declaration" | "attribution" :
                            graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{next_value}"\n'
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
                        case "ifs" | "ifelses" | "while":
                            graph += nesting(body[-1], next_value, declarations, attributions, selections, cycle)
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
                else:
                    match (ant[0]):
                        case "declaration" | "attribution" :
                            graph += f'"{value}" -> "{next_value}"\n'
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
                        case "ifs" | "ifelses" | "while":
                            graph += nesting(ant, next_value, declarations, attributions, selections, cycle)
            else:
                graph += f'"{condition}" -> "{next_value}"\n'

        case "ifelses":
            condition = selections["statments"][tuple[1]]["condition"]
            conditions.append(condition)
            body = selections["statments"][tuple[1]]["body"]
            if_list = body["if"]
            else_list = body["else"]
            if len(if_list) > 0 and len(else_list) > 0:
                if len(if_list) > 0:
                    ant = if_list[0]
                    value = true_value(ant, declarations, attributions, selections, cycle)
                    graph += f'"{condition}" -> "{value}" [label="true"]\n'
                    if len(if_list) > 1:
                        for elem in if_list[1:]:
                            elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                            match (ant[0]):
                                case "declaration" | "attribution" :
                                    graph += f'"{value}" -> "{elem_value}"\n'
                                case "ifs" | "ifelses" | "while":
                                    graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                            ant = elem
                            value = elem_value
                        match (if_list[-1][0]):
                            case "declaration" | "attribution" :
                                graph += f'"{true_value(if_list[-1], declarations, attributions, selections, cycle)}" -> "{next_value}"\n'
                            case "ifs" | "ifelses" | "while":
                                graph += nesting(if_list[-1], next_value, declarations, attributions, selections, cycle)
                    else:
                        match (ant[0]):
                            case "declaration" | "attribution" :
                                graph += f'"{value}" -> "{next_value}"\n'
                            case "ifs" | "ifelses" | "while":
                                graph += nesting(ant, next_value, declarations, attributions, selections, cycle)
                else:
                    graph += f'"{condition}" -> "{next_value}" [label="true"]\n'

                if len(else_list) > 0:
                    ant = else_list[0]
                    value = true_value(ant, declarations, attributions, selections, cycle)
                    graph += f'"{condition}" -> "{value}" [label="false"]\n'
                    if len(else_list) > 1:
                        for elem in else_list[1:]:
                            elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                            match (ant[0]):
                                case "declaration" | "attribution" :
                                    graph += f'"{value}" -> "{elem_value}"\n'
                                case "ifs" | "ifelses" | "while":
                                    graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                            ant = elem
                            value = elem_value
                        match (else_list[-1][0]):
                            case "declaration" | "attribution" :
                                graph += f'"{true_value(else_list[-1], declarations, attributions, selections, cycle)}" -> "{next_value}"\n'
                            case "ifs" | "ifelses" | "while":
                                graph += nesting(else_list[-1], next_value, declarations, attributions, selections, cycle)
                    else:
                        match (ant[0]):
                            case "declaration" | "attribution" :
                                graph += f'"{value}" -> "{next_value}"\n'
                            case "ifs" | "ifelses" | "while":
                                graph += nesting(ant, next_value, declarations, attributions, selections, cycle)
                else:
                    graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
            else:
                graph += f'"{condition}" -> "{next_value}"\n'
            
        case "while":
            condition = cycle["statments"][tuple[1]]["condition"]
            conditions.append(condition)
            body = cycle["statments"][tuple[1]]["body"]
            if len(body) > 0:
                ant = body[0]
                value = true_value(ant, declarations, attributions, selections, cycle)
                graph += f'"{condition}" -> "{value}" [label="true"]\n'
                if len(body) > 1:
                    for elem in body[1:]:
                        elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                        match (ant[0]):
                            case "declaration" | "attribution" :
                                graph += f'"{value}" -> "{elem_value}"\n'
                            case "ifs" | "ifelses" | "while":
                                graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                        ant = elem
                        value = elem_value
                    match (body[-1][0]):
                        case "declaration" | "attribution" :
                            graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{condition}"\n'
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
                        case "ifs" | "ifelses" | "while":
                            graph += nesting(body[-1], condition, declarations, attributions, selections, cycle)
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
                else:
                    match (ant[0]):
                        case "declaration" | "attribution" :
                            graph += f'"{value}" -> "{condition}"\n'
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
                        case "ifs" | "ifelses" | "while":
                            graph += nesting(ant, condition, declarations, attributions, selections, cycle)
                            graph += f'"{condition}" -> "{next_value}" [label="false"]\n'
        case _:
            return ""
         
    return graph



def create_cfg_graph(structure, declarations, attributions, selections, cycle):
    graph = "digraph G {\n"

    if structure["occor"] > 0:
        statment = structure["statments"][0][0]
        match (statment[0]):
            case "declaration":
                value = true_value(statment, declarations, attributions, selections, cycle)
                graph += f'"inicio" -> "{value}"\n'
                if structure["occor"] > 1:
                    graph += f'"{value}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                else:
                    graph += f'"{value}" -> "fim"\n'
            case "attribution":
                value = true_value(statment, declarations, attributions, selections, cycle)
                graph += f'"inicio" -> "{value}"\n'
                if structure["occor"] > 1:
                    graph += f'"{value}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                else:
                    graph += f'"{value}" -> "fim"\n'
            case "ifs":
                condition = selections["statments"][statment[1]]["condition"]
                conditions.append(condition)
                body = selections["statments"][statment[1]]["body"]
                graph += f'"inicio" -> "{condition}"\n'

                if len(body) > 0:
                    ant = body[0]
                    value = true_value(ant, declarations, attributions, selections, cycle)
                    graph += f'"{condition}" -> "{value}" [label="true"]\n'
                    if len(body) > 1:
                        for elem in body[1:]:
                            elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                            match (ant[0]):
                                case "declaration" | "attribution" :
                                    graph += f'"{value}" -> "{elem_value}"\n'
                                case "ifs" | "ifelses" | "while":
                                    graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                            ant = elem
                            value = elem_value
                        match (body[-1][0]):
                            case "declaration" | "attribution" :
                                if structure["occor"] > 1:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "fim"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":
                                if structure["occor"] > 1:
                                    graph += nesting(body[-1], true_value(structure["statments"][1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += nesting(body[-1], "fim", declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                
                    else:
                        match (ant[0]):
                            case "declaration" | "attribution" :  
                                if structure["occor"] > 1:
                                    graph += f'"{value}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{value}" -> "fim"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":

                                if structure["occor"] > 1:
                                    graph += nesting(ant, true_value(structure["statments"][1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                else:
                                    graph += nesting(ant, "fim", declarations, attributions, selections, cycle)

                else:
                    if structure["occor"] > 1:
                        graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                    else:
                        graph += f'"{condition}" -> "fim"\n'

            case "ifelses":
                condition = selections["statments"][statment[1]]["condition"]
                conditions.append(condition)
                body = selections["statments"][statment[1]]["body"]
                if_list = body["if"]
                else_list = body["else"]
                graph += f'"inicio" -> "{condition}"\n'

                if len(if_list) > 0 and len(else_list) > 0:
                    #--------------------------Caso de if----------------------------------
                    if len(if_list) > 0:
                        ant = if_list[0]
                        value = true_value(ant, declarations, attributions, selections, cycle)
                        graph += f'"{condition}" -> "{value}" [label="true"]\n'
                        if len(if_list) > 1:
                            for elem in if_list[1:]:
                                elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                                match (ant[0]):
                                    case "declaration" | "attribution" :
                                        graph += f'"{value}" -> "{elem_value}"\n'
                                    case "ifs" | "ifelses" | "while":
                                        graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                                ant = elem
                                value = elem_value
                            match (if_list[-1][0]):
                                case "declaration" | "attribution" :
                                    if structure["occor"] > 1:
                                        graph += f'"{true_value(if_list[-1], declarations, attributions, selections, cycle)}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{true_value(if_list[-1], declarations, attributions, selections, cycle)}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":
                                    if structure["occor"] > 1:
                                        graph += nesting(if_list[-1], true_value(structure["statments"][1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(if_list[-1], "fim", declarations, attributions, selections, cycle)
                        else:
                            match (ant[0]):
                                case "declaration" | "attribution" :  
                                    if structure["occor"] > 1:
                                        graph += f'"{value}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{value}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":

                                    if structure["occor"] > 1:
                                        graph += nesting(ant, true_value(structure["statments"][1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(ant, "fim", declarations, attributions, selections, cycle)

                    else:
                        if structure["occor"] > 1:
                            graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="true"]\n'
                        else:
                            graph += f'"{condition}" -> "fim" [label="true"]\n'
                    
                    #--------------------------Caso de else----------------------------------
                    if len(else_list) > 0:
                        ant = else_list[0]
                        value = true_value(ant, declarations, attributions, selections, cycle)
                        graph += f'"{condition}" -> "{value}" [label="false"]\n'
                        if len(else_list) > 1:
                            for elem in else_list[1:]:
                                elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                                match (ant[0]):
                                    case "declaration" | "attribution" :
                                        graph += f'"{value}" -> "{elem_value}"\n'
                                    case "ifs" | "ifelses" | "while":
                                        graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                                ant = elem
                                value = elem_value
                            match (else_list[-1][0]):
                                case "declaration" | "attribution" :
                                    if structure["occor"] > 1:
                                        graph += f'"{true_value(else_list[-1], declarations, attributions, selections, cycle)}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{true_value(else_list[-1], declarations, attributions, selections, cycle)}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":
                                    if structure["occor"] > 1:
                                        graph += nesting(else_list[-1], true_value(structure["statments"][1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(else_list[-1], "fim", declarations, attributions, selections, cycle)
                        
                        else:
                            match (ant[0]):
                                case "declaration" | "attribution" :  
                                    if structure["occor"] > 1:
                                        graph += f'"{value}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{value}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":

                                    if structure["occor"] > 1:
                                        graph += nesting(ant, true_value(structure["statments"][1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(ant, "fim", declarations, attributions, selections, cycle)

                    else:
                        if structure["occor"] > 1:
                            graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                        else:
                            graph += f'"{condition}" -> "fim" [label="false"]\n'
                else:
                    if structure["occor"] > 1:
                        graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                    else:
                        graph += f'"{condition}" -> "fim"\n'


            case "while":
                condition = cycle["statments"][statment[1]]["condition"]
                conditions.append(condition)
                body = cycle["statments"][statment[1]]["body"]
                graph += f'"inicio" -> "{condition}"\n'

                if len(body) > 0:
                    ant = body[0]
                    value = true_value(ant, declarations, attributions, selections, cycle)
                    graph += f'"{condition}" -> "{value}" [label="true"]\n'
                    if len(body) > 1:
                        for elem in body[1:]:
                            elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                            match (ant[0]):
                                case "declaration" | "attribution" :
                                    graph += f'"{value}" -> "{elem_value}"\n'
                                case "ifs" | "ifelses" | "while":
                                    graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                            ant = elem
                            value = elem_value
                        match (body[-1][0]):
                            case "declaration" | "attribution" :
                                if structure["occor"] > 1:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}"-> "{condition}"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":
                                if structure["occor"] > 1:
                                    graph += nesting(body[-1], condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += nesting(body[-1], condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                    else:
                        match (ant[0]):
                            case "declaration" | "attribution" :  
                                if len(structure) > 1:
                                    graph += f'"{value}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{value}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":

                                if structure["occor"] > 1:
                                    graph += nesting(ant, condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += nesting(ant, condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'

                else:
                    if structure["occor"] > 1:
                        graph += f'"{condition}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                    else:
                        graph += f'"{condition}" -> "fim"\n'
    else:
        return 'digraph G {\n"inicio" -> "fim"\n}'

    
    for node_id, statment in structure["statments"].items():
        if(node_id == 0):
            continue

        match (statment[0][0]):
            case "declaration":
                value = true_value(statment[0], declarations, attributions, selections, cycle)
                if structure["occor"] != node_id + 1:
                    graph += f'"{value}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                else:
                    graph += f'"{value}" -> "fim"\n'
            case "attribution":
                value = true_value(statment[0], declarations, attributions, selections, cycle)
                if structure["occor"] != node_id + 1:
                    graph += f'"{value}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                else:
                    graph += f'"{value}" -> "fim"\n'
            case "ifs":
                condition = selections["statments"][statment[0][1]]["condition"]
                conditions.append(condition)
                body = selections["statments"][statment[0][1]]["body"]

                if len(body) > 0:
                    ant = body[0]
                    value = true_value(ant, declarations, attributions, selections, cycle)
                    graph += f'"{condition}" -> "{value}" [label="true"]\n'
                    if len(body) > 1:
                        for elem in body[1:]:
                            elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                            match (ant[0]):
                                case "declaration" | "attribution" :
                                    graph += f'"{value}" -> "{elem_value}"\n'
                                case "ifs" | "ifelses" | "while":
                                    graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                            ant = elem
                            value = elem_value
                        match (body[-1][0]):
                            case "declaration" | "attribution" :
                                if structure["occor"] != node_id + 1:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{true_value(structure["statments"][1][0], declarations, attributions, selections, cycle)}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "fim"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":
                                if structure["occor"] != node_id + 1:
                                    graph += nesting(body[-1], true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += nesting(body[-1], "fim", declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                
                    else:
                        match (ant[0]):
                            case "declaration" | "attribution" :  
                                if structure["occor"] != node_id + 1:
                                    graph += f'"{value}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{value}" -> "fim"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":

                                if structure["occor"] != node_id + 1:
                                    graph += nesting(ant, true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                else:
                                    graph += nesting(ant, "fim", declarations, attributions, selections, cycle)

                else:
                    if structure["occor"] != node_id + 1:
                        graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                    else:
                        graph += f'"{condition}" -> "fim"\n'

            case "ifelses":
                condition = selections["statments"][statment[0][1]]["condition"]
                conditions.append(condition)
                body = selections["statments"][statment[0][1]]["body"]
                if_list = body["if"]
                else_list = body["else"]

                if len(if_list) > 0 and len(else_list) > 0:
                    #--------------------------Caso de if----------------------------------
                    if len(if_list) > 0:
                        ant = if_list[0]
                        value = true_value(ant, declarations, attributions, selections, cycle)
                        graph += f'"{condition}" -> "{value}" [label="true"]\n'
                        if len(if_list) > 1:
                            for elem in if_list[1:]:
                                elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                                match (ant[0]):
                                    case "declaration" | "attribution" :
                                        graph += f'"{value}" -> "{elem_value}"\n'
                                    case "ifs" | "ifelses" | "while":
                                        graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                                ant = elem
                                value = elem_value
                            match (if_list[-1][0]):
                                case "declaration" | "attribution" :
                                    if structure["occor"] != node_id + 1:
                                        graph += f'"{true_value(if_list[-1], declarations, attributions, selections, cycle)}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{true_value(if_list[-1], declarations, attributions, selections, cycle)}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":
                                    if structure["occor"] != node_id + 1:
                                        graph += nesting(if_list[-1], true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(if_list[-1], "fim", declarations, attributions, selections, cycle)
                        else:
                            match (ant[0]):
                                case "declaration" | "attribution" :  
                                    if structure["occor"] != node_id + 1:
                                        graph += f'"{value}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{value}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":

                                    if structure["occor"] != node_id + 1:
                                        graph += nesting(ant, true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(ant, "fim", declarations, attributions, selections, cycle)

                    else:
                        if structure["occor"] != node_id + 1:
                            graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="true"]\n'
                        else:
                            graph += f'"{condition}" -> "fim" [label="true"]\n'
                    
                    #--------------------------Caso de else----------------------------------
                    if len(else_list) > 0:
                        ant = else_list[0]
                        value = true_value(ant, declarations, attributions, selections, cycle)
                        graph += f'"{condition}" -> "{value}" [label="false"]\n'
                        if len(else_list) > 1:
                            for elem in else_list[1:]:
                                elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                                match (ant[0]):
                                    case "declaration" | "attribution" :
                                        graph += f'"{value}" -> "{elem_value}"\n'
                                    case "ifs" | "ifelses" | "while":
                                        graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                                ant = elem
                                value = elem_value
                            match (else_list[-1][0]):
                                case "declaration" | "attribution" :
                                    if structure["occor"] != node_id + 1:
                                        graph += f'"{true_value(else_list[-1], declarations, attributions, selections, cycle)}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{true_value(else_list[-1], declarations, attributions, selections, cycle)}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":
                                    if structure["occor"] != node_id + 1:
                                        graph += nesting(else_list[-1], true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(else_list[-1], "fim", declarations, attributions, selections, cycle)
                        
                        else:
                            match (ant[0]):
                                case "declaration" | "attribution" :  
                                    if structure["occor"] != node_id + 1:
                                        graph += f'"{value}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                                    else:
                                        graph += f'"{value}" -> "fim"\n'
                                case "ifs" | "ifelses" | "while":

                                    if structure["occor"] != node_id + 1:
                                        graph += nesting(ant, true_value(structure["statments"][node_id +1][0], declarations, attributions, selections, cycle), declarations, attributions, selections, cycle)
                                    else:
                                        graph += nesting(ant, "fim", declarations, attributions, selections, cycle)

                    else:
                        if structure["occor"] != node_id + 1:
                            graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                        else:
                            graph += f'"{condition}" -> "fim" [label="false"]\n'
                else:
                    if structure["occor"] != node_id + 1:
                        graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                    else:
                        graph += f'"{condition}" -> "fim"\n'


            case "while":
                condition = cycle["statments"][statment[0][1]]["condition"]
                conditions.append(condition)
                body = cycle["statments"][statment[0][1]]["body"]

                if len(body) > 0:
                    ant = body[0]
                    value = true_value(ant, declarations, attributions, selections, cycle)
                    graph += f'"{condition}" -> "{value}" [label="true"]\n'
                    if len(body) > 1:
                        for elem in body[1:]:
                            elem_value = true_value(elem, declarations, attributions, selections, cycle) 
                            match (ant[0]):
                                case "declaration" | "attribution" :
                                    graph += f'"{value}" -> "{elem_value}"\n'
                                case "ifs" | "ifelses" | "while":
                                    graph += nesting(ant, elem_value, declarations, attributions, selections, cycle)
                            ant = elem
                            value = elem_value
                        match (body[-1][0]):
                            case "declaration" | "attribution" :
                                if structure["occor"] != node_id + 1:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{true_value(body[-1], declarations, attributions, selections, cycle)}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":
                                if structure["occor"] != node_id + 1:
                                    graph += nesting(body[-1], condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += nesting(body[-1], condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                    else:
                        match (ant[0]):
                            case "declaration" | "attribution" :  
                                if structure["occor"] != node_id + 1:
                                    graph += f'"{value}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += f'"{value}" -> "{condition}"\n'
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'
                            case "ifs" | "ifelses" | "while":
                                if structure["occor"] != node_id + 1:
                                    graph += nesting(ant, condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}" [label="false"]\n'
                                else:
                                    graph += nesting(ant, condition, declarations, attributions, selections, cycle)
                                    graph += f'"{condition}" -> "fim" [label="false"]\n'

                else:
                    if structure["occor"] != node_id + 1:
                        graph += f'"{condition}" -> "{true_value(structure["statments"][node_id + 1][0], declarations, attributions, selections, cycle)}"\n'
                    else:
                        graph += f'"{condition}" -> "fim"\n'

    for cond in conditions:
        graph+= f'"{cond}" [shape=diamond];\n'


    graph += "}\n"

    return graph

