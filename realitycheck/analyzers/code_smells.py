import ast

def analyze_code_smells(tree):
    result = {
        "too_many_arguments": [],
        "bad_function_names": [],
        "empty_functions": [],
    }

    for node in ast.walk(tree):

        # Detect functions
        if isinstance(node, ast.FunctionDef):

            # 🚨 Too many arguments
            if len(node.args.args) > 4:
                result["too_many_arguments"].append(node.name)

            # 🚨 Bad naming (very basic for now)
            if len(node.name) <= 2:
                result["bad_function_names"].append(node.name)

            # 🚨 Empty function
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                result["empty_functions"].append(node.name)

    return result