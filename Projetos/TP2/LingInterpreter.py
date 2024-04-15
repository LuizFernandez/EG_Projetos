from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.vars = {}
        self.erros = []

    def start(self, tree):
        print("Entrei na Raiz, vou visitar os Elementos")
        for statement in tree.children:
            self.visit(statement)
        return (self.vars, self.erros)
    
    def statment(self, tree):
        r =  self.visit_children(tree)
        self.vars = r
        pass
    
    def declaration(self, tree):
        r = self.visit_children(tree)
        type = str(r[0])
        variable = str(r[1])

        if len(r) < 3:
            value = None
        else:
            value = r[2]

        if variable not in self.vars.keys():
            self.vars[variable] = {}
            self.vars[variable]["type"] = type
            self.vars[variable]["value"] = value
            # self.vars[variable]["redeclared"] = False
            self.vars[variable]["declared"] = True
            self.vars[variable]["used"] = False
        else:
            # self.vars[variable]["redeclared"] = True Removi porque não faz sentido ocorrer, mas adicionei listagem de erros
            errorValue = ""
            if value:
                errorValue = f"= {value}"
                
            self.erros.append({"type": "variable already declared", "error": f"{type} {variable} {errorValue}"})

        return self.vars
    
    def attribution(self, tree):
        r = self.visit_children(tree)
        variable = str(r[0])
        value = self.visit(tree.children[1]) 
        if variable in self.vars.keys():
            self.vars[variable]["value"] = value
        else:
            self.erros.append({"type": "variable not declared", "error": f"{variable} = {value}"})
            #self.vars[variable] = {}
            #self.vars[variable]["type"] = None
            #self.vars[variable]["value"] = None
            #self.vars[variable]["redeclared"] = False
            #self.vars[variable]["declared"] = False

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
        value = None
        if variable in self.vars.keys():
            value = self.vars[variable]["value"]
            self.vars[variable]["used"] = True  

        return value
    
    def value_int(self, tree):
        r = self.visit_children(tree)
        return int(r[0])
    
    def value_float(self, tree):
        r = self.visit_children(tree)
        return float(r[0])
    
    def value_string(self, tree):
        r = self.visit_children(tree)
        return str(r[0])
    
    def value_bool(self, tree):
        r = self.visit_children(tree)
        return bool(r[0])

    def complex_value(self, tree):
        r = self.visit_children(tree)
        return r[0]
    
    def list_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        if len(r) == 2:
            value = []
        elif len(r) > 2:
            value = []
            for i in range(0, len(r) - 2):
                r = self.visit(tree.children[i+1]) 
                value.append(r)
        else:
            variable = str(r[0])
            if variable in self.vars.keys() and (self.vars[variable]["type"] == "array" or self.vars[variable]["type"] == "set"):
                value = list(self.vars[variable]["value"])
            else:
                if variable not in self.vars.keys():
                    self.erros.append({"type": "variable is used but not declared", "error": f"{variable} not declared, but is used with list()"})
                else:
                    self.erros.append({"type": "variable is not of type array or set", "error": f"list({variable}), {variable} is of type {self.vars[variable]['type']}"})

        return value
            
    def set_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        if len(r) > 0:
            variable = str(r[0])
            if variable in self.vars.keys() and (self.vars[variable]["type"] == "list" or self.vars[variable]["type"] == "array"):
                value = set(self.vars[variable]["value"])
            else:
                if variable not in self.vars.keys():
                    self.erros.append({"type": "variable is used but not declared", "error": f"{variable} not declared but is used with set()"})
                else:
                    self.erros.append({"type": "variable is not of type array or list", "error": f"set({variable}), {variable} is of type {self.vars[variable]['type']}"})
        else:
            value = set()

        return value
    
    def tuple_construct(self, tree):
        r = self.visit_children(tree)
        
        value = None
        if len(r) == 2:
            value = ()
        elif len(r) == 4:
            val1 = self.visit(tree.children[1])
            val2 = self.visit(tree.children[2])
            value = (val1, val2)

        return value
    
    def array_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        arg = str(r[0])
        if arg.isdigit():
            value = [None] * int(arg)
        elif arg in self.vars.keys():
            if self.vars[arg]["type"] == "int":
                value = [None] * int(self.vars[arg]["value"])
            elif self.vars[arg]["type"] == "list" or self.vars[arg]["type"] == "set":
                value = list(self.vars[arg]["value"])
        else:
            if arg not in self.vars.keys():
                self.erros.append({"type": "variable is used but not declared", "error": f"{arg} not declared and used with array()"})
            else:
                self.erros.append({"type": "variable is not of type list or set", "error": f"array({arg}), {arg} is of type {self.vars[arg]['type']}"})

        return value

    def value_operation(self, tree):
        print("Value Operation")