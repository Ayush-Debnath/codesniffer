import ast

def analyze_design(tree):
    issues = []

    for node in ast.walk(tree):

        # 🚨 God function (too many statements)
        if isinstance(node, ast.FunctionDef):
            if len(node.body) > 15:
                issues.append(f"⚠️ Function '{node.name}' is too large → possible God function")

        # 🚨 Too many arguments (design smell)
        if isinstance(node, ast.FunctionDef):
            if len(node.args.args) > 5:
                issues.append(f"⚠️ Function '{node.name}' has too many parameters → poor API design")

        # 🚨 Deep nesting (hard to maintain)
        if isinstance(node, (ast.For, ast.While, ast.If)):
            depth = get_nesting_depth(node)
            if depth > 3:
                issues.append("⚠️ Deep nesting detected → code is hard to maintain")

    return issues


def get_nesting_depth(node, level=0):
    max_depth = level

    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.For, ast.While, ast.If)):
            depth = get_nesting_depth(child, level + 1)
            max_depth = max(max_depth, depth)

    return max_depth