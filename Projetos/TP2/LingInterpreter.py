from lark.visitors import Interpreter

from script import get_type, validate_error

class MyInterpreter(Interpreter):
    def __init__(self):
        self.vars = {}
        self.erros = []

    def start(self, tree):
        for statement in tree.children:
            self.visit(statement)
        return (self.vars, self.erros)
    
    def statment(self, tree):
        r =  self.visit_children(tree)
        self.vars = r
        pass

    def declaration(self, tree):
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
        else:
            if variable in self.vars.keys():
                validate_error(self.erros, "redeclaration", (variable))
            if not flag_type:
                validate_error(self.erros, "typing", (var_type, variable, value))
            if not flag_val:
                validate_error(self.erros, "failed", (variable, var_type, value_name))

    def attribution(self, tree):
        r = self.visit_children(tree)
        variable = str(r[0])
        value = self.visit(tree.children[1]) 
        if variable in self.vars.keys():
            self.vars[variable]["value"] = value
        else:
            self.erros.append({"type": "variable not declared", "error": f"{variable} = {value}"})

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
                flag = False
                validate_error(self.erros, "faildArgC", (variable, self.vars[variable]["type"], "list"))

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
                flag = False
                validate_error(self.erros, "faildArgC", (variable, self.vars[variable]["type"], "set"))
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
        variable = None
        flag = True

        arg = str(r[0])
        if arg.isdigit():
            value = [None] * int(arg)
        elif arg in self.vars.keys():
            if self.vars[arg]["type"] == "int":
                value = [None] * int(self.vars[arg]["value"])
            elif self.vars[arg]["type"] == "list" or self.vars[arg]["type"] == "set":
                value = list(self.vars[arg]["value"])
            else:
                validate_error(self.erros, "faildArgC", (variable, self.vars[arg]["type"], "array"))
        else:
            flag = False

        return (value, arg, flag)

    def value_operation(self, tree):
        print("Value Operation")