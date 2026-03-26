import ast

def analyze_complexity(tree):
    result = {
        "total_loops": 0,
        "nested_loops": 0,
        "long_functions": []
    }

    for node in ast.walk(tree):
        # Count loops
        if isinstance(node, (ast.For, ast.While)):
            result["total_loops"] += 1

            # Check for nested loops
            for child in ast.walk(node):
                if child != node and isinstance(child, (ast.For, ast.While)):
                    result["nested_loops"] += 1
                    break

        # Detect long functions
        if isinstance(node, ast.FunctionDef):
            length = len(node.body)
            if length > 10:  # threshold (we can tune later)
                result["long_functions"].append({
                    "name": node.name,
                    "length": length
                })

    return result