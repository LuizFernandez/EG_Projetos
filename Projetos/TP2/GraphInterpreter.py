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
        #print((r[1][0]) + " " + str(self.in_selection))
        if(self.in_selection == False):
            self.node += 1
            result = r[0][0] + " " + r[1]
            if len(r) > 2:
                result += " ="
                for elem in r[2:]:
                    result += " " + elem[0]
            self.structure[self.node] = result
        else:
            result = r[0][0] + " " + r[1]
            if len(r) > 2:
                result += " ="
                for elem in r[2:]:
                    result += " " + elem[0]
        return result
    
    def attribution(self, tree):
        result = ""
        r = self.visit_children(tree)
        #print((r[1][0]) + " " + str(self.in_selection))
        if(self.in_selection == False):
            self.node += 1
            result = r[0][0] + " ="
            for elem in r[1:]:
                result += " " + elem[0]
            self.structure[self.node] = result
        else:
            result = r[0][0] + " ="
            for elem in r[1:]:
                result += " " + elem[0]
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

    def selection(self, tree):
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
        return r[1][0]