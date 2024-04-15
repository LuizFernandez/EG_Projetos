***
Regras léxicas são as expressões regulares que vão apanhar diferentes Token na LI;

Nesta altura existem as seguintes Regex:

```
// Regras Lexicográficas

ID:/(?!int|float|bool|string|set|list|array|tuple\b)[_aA-zZ][aA-zZ_\d]*/

INT: /(-)?\d+/
FLOAT: /(-)\d+\.\d*/
STTRING: /"[^"]*"/
BOOL: "True"|"False"

RRPAR: "]"
LRPAR: "["
VIRG: ","
LPAR: "("
RPAR: ")"

PRIMITIVE_TYPES: /int|float|bool|string/
COMPLEX_TYPE: /set|list|tuple|array/


// Tratamento dos espaços em branco
%import common.WS
%ignore WS

``` 
