import ast

def analyze_performance(tree):
    issues = []

    for node in ast.walk(tree):

        # 🚨 range(len(arr)) pattern
        if isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call):
                if getattr(node.iter.func, "id", "") == "range":
                    if node.iter.args:
                        arg = node.iter.args[0]
                        if isinstance(arg, ast.Call):
                            if getattr(arg.func, "id", "") == "len":
                                issues.append("⚠️ Use direct iteration instead of range(len(...))")

        # 🚨 membership check in list (slow)
        if isinstance(node, ast.Compare):
            if any(isinstance(op, ast.In) for op in node.ops):
                if isinstance(node.comparators[0], ast.List):
                    issues.append("⚠️ Using 'in' on list → consider using set for faster lookup")

        # 🚨 repeated computation inside loop
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        issues.append("⚠️ Possible repeated computation inside loop")

    return issues