from lark.visitors import Interpreter
from icecream import ic

from script import get_type, validate_error, count_Control

class MyInterpreter(Interpreter):
    def __init__(self):
        self.vars = {}
        self.erros = []
        self.types = {}
        self.count= {"attributions" : 0, "declarations" : 0, "selections" : 0, "cycles" : 0}
        self.nesting = 0
        self.sub_ifs = []

    def start(self, tree):
        for statement in tree.children:
            self.visit(statement)
        return (self.vars, self.erros, self.types, self.count, self.nesting, self.sub_ifs)
    
    def statment(self, tree): 
        r =  self.visit_children(tree)
        self.vars = r
        pass

    def declaration(self, tree):
        self.count["declarations"] += 1
        r = self.visit_children(tree)
        var_type = str(r[0])
        variable = str(r[1])
        value = None

        # Flag de controlo
        flag_type = True 
        flag_init = False
        flag_val = True

        if len(r) >= 3:
            flag_init = True
            (value, value_name, flag_val) = r[2] # value = (valor, nome, flag) 
            if flag_val and get_type(var_type) is not type(value):
                flag_type = False
                if value_name != None:
                    self.vars[value_name]["used"] = False
        

        if variable not in self.vars.keys() and flag_val and flag_type:
            self.vars[variable] = {}
            self.vars[variable]["type"] = var_type
            self.vars[variable]["value"] = value
            self.vars[variable]["used"] = False
            self.vars[variable]["init"] = flag_init
            if var_type not in self.types.keys():
                self.types[var_type] = []
            self.types[var_type].append(variable)
        else:
            if variable in self.vars.keys():
                validate_error(self.erros, "redeclaration", (variable))
            if not flag_type:
                validate_error(self.erros, "typing", (var_type, variable, value))
            if not flag_val:
                validate_error(self.erros, "failedD", (variable, var_type, value_name))

    def attribution(self, tree):
        self.count["attributions"] += 1
        r = self.visit_children(tree)
        variable = str(r[0])
        (value, var_name, flag_val) = self.visit(tree.children[1])
        flag_type = True

        if variable in self.vars.keys() and flag_val and get_type(self.vars[variable]["type"]) is not type(value):
                flag_type = False
                if var_name != None:
                    self.vars[var_name]["used"] = False

        if variable in self.vars.keys() and flag_type and flag_val:
            self.vars[variable]["value"] = value
        else:
            if variable not in self.vars.keys():
                validate_error(self.erros, "notDeclared", (variable))
            if not flag_type:
                validate_error(self.erros, "typing", (self.vars[variable]["type"], variable, value))
            if not flag_val and variable in self.vars.keys():
                validate_error(self.erros, "failedA", (variable, self.vars[variable]["type"], var_name))

        return self.vars
    
    def type(self,tree):
        r = self.visit_children(tree)
        return r[0]
    
    def primitive_type(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def complex_type(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value(self, tree):
        r = self.visit_children(tree)
        return r[0]
    
    def value_id(self, tree):
        r = self.visit_children(tree)
        variable = str(r[0])
        flag = True
        value = None
        if variable in self.vars.keys():
            value = self.vars[variable]["value"]
            self.vars[variable]["used"] = True
        else:
            validate_error(self.erros, "missing", (variable))
            flag = False  

        return (value, variable, flag)
    
    def value_int(self, tree):
        r = self.visit_children(tree)
        return (int(r[0]), None, True)
    
    def value_float(self, tree):
        r = self.visit_children(tree)
        return (float(r[0]), None, True)
    
    def value_string(self, tree):
        r = self.visit_children(tree)
        return (str(r[0]), None, True)
    
    def value_bool(self, tree):
        r = self.visit_children(tree)
        return (bool(r[0]), None, True)

    def complex_value(self, tree):
        r = self.visit_children(tree)
        return r[0]
    
    def list_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        flag = True
        variable = None

        if len(r) == 2:
            value = []
        elif len(r) > 2:
            value = []
            for i in range(0, len(r) - 2):
                r = self.visit(tree.children[i+1]) 
                value.append(r[0])
        else:
            variable = str(r[0])
            if variable in self.vars.keys() and (self.vars[variable]["type"] == "array" or self.vars[variable]["type"] == "set"):
                value = list(self.vars[variable]["value"])
                self.vars[variable]["used"] = True
            else:
                if variable not in self.vars.keys():
                    validate_error(self.erros, "missing", (variable))
                else:
                    validate_error(self.erros, "faildArgC", (variable, self.vars[variable]["type"], "list()"))
                flag = False
                

        return (value, variable, flag)
            
    def set_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        variable = None
        flag = True

        if len(r) > 0:
            variable = str(r[0])
            if variable in self.vars.keys() and (self.vars[variable]["type"] == "list" or self.vars[variable]["type"] == "array"):
                value = set(self.vars[variable]["value"])
                self.vars[variable]["used"] = True
            else:
                if variable not in self.vars.keys():
                    validate_error(self.erros, "missing", (variable))
                else:
                    validate_error(self.erros, "faildArgC", (variable, self.vars[variable]["type"], "set()"))
                flag = False
        else:
            value = set()

        return (value, variable, flag)
    
    def tuple_construct(self, tree):
        r = self.visit_children(tree)
        
        value = None

        if len(r) == 2:
            value = ()
        elif len(r) == 4:
            val1 = self.visit(tree.children[1])
            val2 = self.visit(tree.children[2])
            value = (val1, val2)

        return (value, None, True)
    
    def array_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        flag = True

        variable = str(r[0])
        if variable.isdigit():
            value = [None] * int(variable)
        elif variable in self.vars.keys():
            if self.vars[variable]["type"] == "int":
                value = [None] * int(self.vars[variable]["value"])
            elif self.vars[variable]["type"] == "list" or self.vars[variable]["type"] == "set":
                value = list(self.vars[variable]["value"])
            else:
                validate_error(self.erros, "faildArgC", (variable, self.vars[variable]["type"], "array()"))
        else:
            validate_error(self.erros, "missing", (variable))
            flag = False

        return (value, variable, flag)

    def operation(self, tree):
        r = self.visit_children(tree)
        if len(r) > 1:
            match (r[1]):
                case "==":
                    return (r[0][0] == r[2][0], f"{r[0][0]} == {r[2][0]}", True)
                case "!=":
                    return (r[0][0] != r[2][0], f"{r[0][0]} != {r[2][0]}", True)
                case ">":
                    return (r[0][0] > r[2][0], f"{r[0][0]} > {r[2][0]}", True)
                case ">=":
                    return (r[0][0] >= r[2][0], f"{r[0][0]} >= {r[2][0]}", True)
                case "<":
                    return (r[0][0] < r[2][0], f"{r[0][0]} < {r[2][0]}", True)
                case "<=":
                    return (r[0][0] <= r[2][0], f"{r[0][0]} <= {r[2][0]}", True)
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
                    if type(r[0][0]) is bool and type(r[2][0]) is bool:
                        return (r[0][0] or r[2][0], f"{r[0][0]} || {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} || {r[2][0]}", False)
                case "-":
                    if type(r[0][0]) is not (bool or str) and type(r[2][0]) is not (bool or str):
                        return (r[0][0] - r[2][0], f"{r[0][0]} - {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} - {r[2][0]}", False)
                case "+":
                    if type(r[0][0]) is not (bool or str) and type(r[2][0]) is not (bool or str):
                        return (r[0][0] + r[2][0], f"{r[0][0]} + {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} + {r[2][0]}", False)
                case _:
                    print("Invalid Operator")
        else:
            return r[0]

    def opa(self, tree):
        r = self.visit_children(tree)
        return (str(r[0]))
    
    def term(self, tree):
        r = self.visit_children(tree)
        if (len(r) > 1):
            match r[1]:
                case "&&":
                    if type(r[0][0]) is bool and type(r[2][0]) is bool:
                        return (r[0][0] and r[2][0], f"{r[0][0]} && {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} && {r[2][0]}", False)
                case "*":
                    if type(r[0][0]) is not (bool or str) and type(r[2][0]) is not (bool or str):
                        return (r[0][0] * r[2][0], f"{r[0][0]} * {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} * {r[2][0]}", False)
                case "/":
                    if type(r[0][0]) is not (bool or str) and type(r[2][0]) is not (bool or str):
                        return (r[0][0] / r[2][0], f"{r[0][0]} / {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} / {r[2][0]}", False)
                case "%":
                    if type(r[0][0]) is not (bool or str) and type(r[2][0]) is not (bool or str):
                        return (r[0][0] % r[2][0], f"{r[0][0]} % {r[2][0]}", True)
                    else:
                        return (None, f"{r[0][0]} % {r[2][0]}", False)
                case _:
                    print("Invalid Operator")

        return r[0]

    def opm(self, tree):
        r = self.visit_children(tree)
        return (str(r[0]))
    
    def factor_par(self,tree):
        r = self.visit_children(tree)
        return r[1]
    
    def factor_pot(self, tree):
        r = self.visit_children(tree)
        if type(r[0][0]) is (bool or str) or type(r[2][0]) is (bool or str):
            return (None, f"{r[0][0]} ^ {r[2][0]}", False)
        else:
            return (r[0][0] ** r[2][0], f"{r[0][0]} ^ {r[2][0]}", True)
    
    def selection(self, tree):
        self.count["selections"] += 1
        r = self.visit_children(tree)
        if_list = []
        if len(r) >= 3: 
            for child in r[2:]:
                if isinstance(child[0], tuple):
                    self.nesting += 1
            if isinstance(r[2][0], tuple):
                if len(r[2:]) == 1 and r[2][0][0] == "if":
                    if_list = r[2][0][2]
                    if r[1][1] != None:
                        self.sub_ifs.append([r[1][1]] + if_list)
        return ("if", r[1][1], [r[1][1]] + if_list)

    def cycle(self, tree):
        self.count["selections"] += 1
        r = self.visit_children(tree)
        if len(r) >= 3: 
            for child in r[2:]:
                if isinstance(child[0], tuple):
                    self.nesting += 1

        return ("cycle", 0)
