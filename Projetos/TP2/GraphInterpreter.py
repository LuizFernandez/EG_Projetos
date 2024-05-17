from lark.visitors import Interpreter

from script import get_type, validate_error, count_Control

class GraphInterpreter(Interpreter):
    def __init__(self):
        self.structure = {0 : "inicio"}
        self.node = 0
        self.in_selection = False

    def start(self, tree):
        r = self.visit_children(tree)
        self.structure[self.node + 1] = "fim"
        return self.structure
    
    def statments(self, tree): 
        r = self.visit_children(tree)
        return r

    def declaration(self, tree):
        result = ""
        r = self.visit_children(tree)

        result = r[0][0] + " " + r[1]
        if len(r) > 2:
            result += " = "
            if type(r[2]) is list:
                for elem in r[2]:
                    result += elem 
            else:
                result += r[2]
                
        if(self.in_selection == False):
            self.node += 1
            self.structure[self.node] = result
            
        #print(result)
        return result
    
    def attribution(self, tree):
        result = ""
        r = self.visit_children(tree)

        result = r[0][0] + " = "
        if type(r[1]) is list:
            for elem in r[1]:
                result += elem 
        else:
            result += r[1]

        if(self.in_selection == False):
            self.node += 1
            self.structure[self.node] = result
        
        return result

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
                    return f"{r[0][0]} == {r[2][0]}"
                case "!=":
                    return f"{r[0][0]} != {r[2][0]}"
                case ">":
                    return f"{r[0][0]} > {r[2][0]}"
                case ">=":
                    return f"{r[0][0]} >= {r[2][0]}"
                case "<":
                    return f"{r[0][0]} < {r[2][0]}"
                case "<=":
                    return f"{r[0][0]} <= {r[2][0]}"
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
                    return f"{r[0][0]} || {r[2][0]}"
                case "-":
                    return f"{r[0][0]} - {r[2][0]}"
                case "+":
                    return f"{r[0][0]} + {r[2][0]}"
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
                    return f"{r[0][0]} && {r[2][0]}"
                case "*":
                    return f"{r[0][0]} * {r[2][0]}"
                case "/":
                    return f"{r[0][0]} / {r[2][0]}"
                case "%":
                    return f"{r[0][0]} % {r[2][0]}"
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

    def selection(self, tree):
        if not self.in_selection:
            self.node += 1
        self.in_selection = True
        self.structure[self.node] = []
        r = self.visit_children(tree)
        self.structure[self.node].append(f"if({r[1][0]})")
        for elem in r[2:]:
            if isinstance(elem, list):
                self.structure[self.node].append(elem[0])
            else:
                self.structure[self.node].append(str(elem))
        self.in_selection = False
        return "IGNORE"