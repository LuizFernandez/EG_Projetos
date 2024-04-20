from lark import Token

def get_type(value):

    type = None

    match (value):

        case "int":
            type = int
        case "string":
            type = str
        case "float":
            type = float
        case "bool":
            type = bool
        case "list":
            type = list
        case "set":
            type = set
        case "tuple":
            type = tuple
        case "array":
            type = list
        case _:
            print("Invalid Typing!!!")

    return type



def validate_error(errors, error_type, args):
    match error_type:
        case "redeclaration":
            variable = args[0]
            errors.append({
                "type": "Redeclaration", 
                "description": "variable is already declare", 
                "variable": variable
            })
        case "notDeclared":
            variable = args[0]
            errors.append({
                "type": "Not Declared", 
                "description": "Variable is not declared", 
                "variable": variable
            })
        case "typing":
            (var_type, variable, value) = args
            errors.append({
                "type": "Type", 
                "description": f"Value type ({value} => {str(type(value))})  doesn't match variable type ({var_type})", 
                "variable": variable
            })
        case "missing":
            (value) = args
            errors.append({
                "type": "Missing", 
                "description": f"Variable {value} isn't declared for use",
                "variable": value
            })
        case "failedD":
            (variable, var_type, value) = args
            errors.append({
                "type": "Failed to Declare", 
                "description": f"Variable {variable} of type {var_type} failed to be declared because variable {value} doesn't exist!", 
                "variable": variable
            })
        case "failedA":
            (variable, var_type, value) = args
            errors.append({
                "type": "Failed to Assign", 
                "description": f"Variable {variable} of type {var_type} failed to recive a new value", 
                "variable": variable
            })
        case "faildArgC":
            (variable, var_type, function_name) = args
            errors.append({
                "type": "Invalid Argument Type", 
                "description": f"Function {function_name} does not accept variable {variable} of type {var_type}, because of being of a different type",
                "variable": variable
            })

def count_Control(tokens):
    count = 0
    for token in tokens:
        if isinstance(token, Token) and (token.type == 'IF' or token.type == 'WHILE' or token.type == 'DO' or token.type == 'FOR'):
            count += 1
        elif isinstance(token, list):
            count += count_Control(token)
    return count

