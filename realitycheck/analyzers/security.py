import ast

def analyze_security(tree):
    issues = []

    for node in ast.walk(tree):

        # 🚨 eval / exec usage
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ["eval", "exec"]:
                    issues.append("🚨 Use of eval/exec detected → potential security risk")

        # 🚨 hardcoded secrets (basic detection)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id.lower()
                    if any(keyword in name for keyword in ["password", "secret", "api_key", "token"]):
                        if isinstance(node.value, ast.Constant):
                            issues.append(f"🚨 Hardcoded secret detected in variable '{target.id}'")

        # 🚨 unsafe file operations
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id == "open":
                    issues.append("⚠️ File opened without context manager or validation")

    return issues