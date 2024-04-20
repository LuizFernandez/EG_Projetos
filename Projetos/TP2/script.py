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
        case "failed":
            (variable, var_type, value) = args
            errors.append({
                "type": "Failed to Declare", 
                "description": f"Variable {variable} of type {var_type} failed to be declared because variable {value} doesn't exist!", 
                "variable": variable
            })
        case "faildArgC":
            (variable, var_type, const) = args
            errors.append({
                "type": "Invalid Argument Type", 
                "description": f"Variable {variable} of type {var_type} is not of a type that the construct {const} accepts", 
                "variable": variable
            })