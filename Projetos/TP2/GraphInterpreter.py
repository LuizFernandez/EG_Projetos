from lark.visitors import Interpreter
from icecream import ic

from script import get_type, validate_error, count_Control

class GraphInterpreter(Interpreter):
    def __init__(self):
        self.structure = { "statments": {}, "occor": 0}
        self.selections = { "statments": {}, "occor": 0}
        self.cycle = { "statments": {}, "occor": 0}
        self.declarations = { "statments": {}, "occor": 0}
        self.attributions = { "statments": {}, "occor": 0}

    def start(self, tree):
        r = self.visit_children(tree)
        for pos in range(0, len(r)):
            self.structure["statments"][pos] = r[pos]
        
        self.structure["occor"] = len(r)

        return (self.structure, self.declarations, self.attributions, self.selections, self.cycle)
    
    def statments(self, tree): 
        r = self.visit_children(tree)
        return r

    def declaration(self, tree):
        r = self.visit_children(tree)

        n = self.declarations["occor"]
        self.declarations["occor"] += 1

        result = r[0][0] + " " + r[1]
        if len(r) > 2:
            result += " = "
            if type(r[2]) is list:
                for elem in r[2]:
                    result += elem 
            else:
                result += r[2]
                
        self.declarations["statments"][n] = result
            
        return ("declaration", n)
    
    def attribution(self, tree):
        r = self.visit_children(tree)

        n = self.attributions["occor"]
        self.attributions["occor"] += 1

        result = r[0] + " = "
        if type(r[1]) is list:
            for elem in r[1]:
                result += elem 
        else:
            result += r[1]

        self.attributions["statments"][n] = result
        
        return ("attribution", n)

    def primitive_type(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def complex_type(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value_id(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value_int(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value_float(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value_string(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value_bool(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def complex_value(self, tree):
        r = self.visit_children(tree)
        return r[0]
    
    def list_construct(self, tree):
        r = self.visit_children(tree)
        value = None

        if len(r) == 2:
            value = "[]"
        elif len(r) > 2:
            value = []
            for i in range(0, len(r) - 2):
                r = self.visit(tree.children[i+1]) 
                value.append(r[0])
            value = str(value)
        else:
            variable = str(r[0])    
            value = f"list({variable})"
        return value
            
    def set_construct(self, tree):
        r = self.visit_children(tree)
        value = None

        if len(r) > 0:
            variable = str(r[0])
            value = f"set({variable})"
        else:
            value = "set()"

        return value
    
    def tuple_construct(self, tree):
        r = self.visit_children(tree)
        
        value = None

        if len(r) == 2:
            value = "()"
        elif len(r) == 4:
            val1 = self.visit(tree.children[1])
            val2 = self.visit(tree.children[2])
            value = f"({val1}, {val2})"

        return value
    
    def array_construct(self, tree):
        r = self.visit_children(tree)
        value = None

        variable = str(r[0])
        value = f"array({variable})"

        return value
    
    def operation(self, tree):
        r = self.visit_children(tree)
        if len(r) > 1:
            match (r[1]):
                case "==":
                    return f"{r[0]} == {r[2]}"
                case "!=":
                    return f"{r[0]} != {r[2]}"
                case ">":
                    return f"{r[0]} > {r[2]}"
                case ">=":
                    return f"{r[0]} >= {r[2]}"
                case "<":
                    return f"{r[0]} < {r[2]}"
                case "<=":
                    return f"{r[0]} <= {r[2]}"
                case _:
                    print("Invalid Operator")
        return r[0]
    
    def opr(self, tree):
        r = self.visit_children(tree)
        return(str(r[0]))
    
    def expr(self, tree):
        r = self.visit_children(tree)
        if (len(r) > 1):
            match r[1]:
                case "||":
                    return f"{r[0]} || {r[2]}"
                case "-":
                    return f"{r[0]} - {r[2]}"
                case "+":
                    return f"{r[0]} + {r[2]}"
                case _:
                    print("Invalid Operator")
        else:
            return str(r[0])

    def opa(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def term(self, tree):
        r = self.visit_children(tree)
        if (len(r) > 1):
            match r[1]:
                case "&&":
                    return f"{r[0]} && {r[2]}"
                case "*":
                    return f"{r[0]} * {r[2]}"
                case "/":
                    return f"{r[0]} / {r[2]}"
                case "%":
                    return f"{r[0]} % {r[2]}"
                case _:
                    print("Invalid Operator")

        return str(r[0])

    def opm(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def factor_par(self,tree):
        r = self.visit_children(tree)
        return r[1]
    
    def factor_pot(self, tree):
        r = self.visit_children(tree)
        return f"{r[0][0]}^{r[2][0]}"

    def selection_ifs(self, tree):
        n = self.selections["occor"]
        self.selections["occor"] += 1

        r = self.visit_children(tree)
        content = {}

        condiction = r[1][0]
        content["condition"] = f"if ({condiction})"

        body = []
        for st in r[2:]:
            body.append(st[0])
        content["body"] = body

        self.selections["statments"][n] = content
        
        return ("ifs", n)
    
    def selection_ifelses(self, tree):
        n = self.selections["occor"]
        self.selections["occor"] += 1

        r = self.visit_children(tree)
        content = {}

        condiction = r[1][0]
        content["condition"] = f"if ({condiction})"

        body = {"if": [], "else": []}
        key = "if"
        for st in r[2:]:
            if key == "else" and type(st) is tuple:
                body[key].append(st)
            elif type(st) is not list:
                key = "else"
            else:
                body[key].append(st[0])
        content["body"] = body

        self.selections["statments"][n] = content
        
        return ("ifelses", n)
    
    def cycle_while(self, tree):
        n = self.cycle["occor"]
        self.cycle["occor"] += 1

        r = self.visit_children(tree)
        content = {}

        condiction = r[1][0]
        content["condition"] = f"while ({condiction})"

        body = []
        for st in r[2:]:
            body.append(st[0])
        content["body"] = body

        self.cycle["statments"][n] = content

        return ("while", n)