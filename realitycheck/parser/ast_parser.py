import ast

def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    try:
        tree = ast.parse(code)
        return tree
    except SyntaxError as e:
        return {"error": str(e)}

def extract_structure(tree):
    structure = {
        "functions": [],
        "loops": 0,
        "imports": [],
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            structure["functions"].append(node.name)
        
        elif isinstance(node, (ast.For, ast.While)):
            structure["loops"] += 1
        
        elif isinstance(node, ast.Import):
            for alias in node.names:
                structure["imports"].append(alias.name)

    return structure