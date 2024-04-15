from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.vars = {}
        self.currentType = ""

    def start(self, tree):
        print("Entrei na Raiz, vou visitar os Elementos")
        for statement in tree.children:
            self.visit(statement)
        return self.vars
    
    def statment(self, tree):
        r =  self.visit_children(tree)
        self.vars = r
        pass
    
    def declaration(self, tree):
        r = self.visit_children(tree)
        type = self.visit(tree.children[0])
        variable = str(r[1])

        if len(r) < 3:
            value = None
        else:
            value = self.visit(tree.children[2]) 

        if variable not in self.vars.keys():
            r = self.visit(tree.children[0])
            self.vars[variable] = {}
            self.vars[variable]["type"] = type
            self.vars[variable]["value"] = value
            self.vars[variable]["redeclared"] = False
            self.vars[variable]["declared"] = True
        else:
            self.vars[variable]["redeclared"] = True

        return self.vars
    
    def attribution(self, tree):
        r = self.visit_children(tree)
        variable = str(r[0])
        if variable in self.vars.keys():
            value = self.visit(tree.children[1]) 
            self.vars[variable]["value"] = value
        else:
            self.vars[variable] = {}
            self.vars[variable]["type"] = None
            self.vars[variable]["value"] = None
            self.vars[variable]["redeclared"] = False
            self.vars[variable]["declared"] = False

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

        return value
            
    def set_construct(self, tree):
        r = self.visit_children(tree)

        value = None
        if len(r) > 0:
            variable = str(r[0])
            if variable in self.vars.keys() and (self.vars[variable]["type"] == "list" or self.vars[variable]["type"] == "array"):
                value = set(self.vars[variable]["value"])
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

        return value

    def value_operation(self, tree):
        print("Value Operation")

grammar = '''
// Regras Sintáticas
start: statments*

statments: declaration
         | attribution

declaration: type ID ( | "=" value)

attribution: ID "=" value

type: primitive_type
	| complex_type

primitive_type: PRIMITIVE_TYPES

complex_type  : COMPLEX_TYPE

value: ID                  -> value_id
     | primitive_value
     | complex_value

primitive_value : INT      -> value_int
				| FLOAT    -> value_float
				| STRING   -> value_string
				| BOOL     -> value_bool

complex_value : list_construct
			  | set_construct
			  | tuple_construct
			  | array_construct

list_construct : LRPAR RRPAR
			   | LRPAR value ("," value)* RRPAR
			   | "list(" ID ")" # ID apenas pode ser do tipo arrary ou set                                      mas tem que ser uma variável

set_construct : "set()"
			  | "set(" ID ")"
			  
tuple_construct : LPAR RPAR
				| LPAR value "," value RPAR

array_construct : "array(" INT ")"
				| "array(" ID ")" # ID é uma vairável do tipo lista, set ou tuple

                
// Regras Lexicográficas

ID:/(?!int|float|bool|string|set|list|array|tuple|True|False\b)[_aA-zZ][aA-zZ_\d]*/

INT: /(-)?\d+/
FLOAT: /(-)?\d+\.\d*/
STRING: /"[^"]*"/
BOOL: "True"|"False"

RRPAR: "]"
LRPAR: "["
LPAR: "("
RPAR: ")"

PRIMITIVE_TYPES: /int|float|bool|string/
COMPLEX_TYPE: /set|list|tuple|array/


// Tratamento dos espaços em branco
%import common.WS
%ignore WS

'''

frase1 = """

int a = 10
float b = -3.9
bool c = True
string s = "Hello"

e = 1

float a = 2.4

float t = b

string l
l = "World"

list z = [2,3,4,5,2,a,3]

set conj = set(z)
set conj2 = set()
list temp = list(conj)


tuple tp = ()

tuple tp2 = (z, conj)

array r = array(3)
array r2 = array(a)
array r3 = array(conj)
"""

frase = """int a = 0

for elem in [1,2,3,4,5]{
    a = a + 1
}

def subtract(int num, int num2){
    if(num >= num2){
        return num - num2
    } else {
        return num2 - num
    }
}

a = subtract(1,2)

"""

p = Lark(grammar) # cria um objeto parser

tree = p.parse(frase1)  # retorna uma tree
data = MyInterpreter().visit(tree)

# Var Table in Markdown
print("| Nome da Variável | Tipo | Valor | Redeclarada | Declarada |")
print("|------------------|------|-------|-------------|-----------|")
for key in data.keys():
    print(f"|{key}|{data[key]['type']}|{data[key]['value']}|{data[key]['redeclared']}|{data[key]['declared']}")
