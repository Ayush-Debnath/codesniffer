def generate_feedback(structure, complexity, smells):
    feedback = []

    # 🚨 Complexity rules
    if complexity["nested_loops"] > 0:
        feedback.append("⚠️ Nested loops detected → potential O(n^2) slowdown")

    if complexity["total_loops"] > 3:
        feedback.append("⚠️ Too many loops → code may be inefficient")

    for func in complexity["long_functions"]:
        feedback.append(f"⚠️ Function '{func['name']}' is too long → consider breaking it down")

    # 🚨 Code smell rules
    if smells["too_many_arguments"]:
        for func in smells["too_many_arguments"]:
            feedback.append(f"⚠️ Function '{func}' has too many arguments → reduce complexity")

    if smells["bad_function_names"]:
        for func in smells["bad_function_names"]:
            feedback.append(f"⚠️ Function name '{func}' is not descriptive")

    if smells["empty_functions"]:
        for func in smells["empty_functions"]:
            feedback.append(f"⚠️ Function '{func}' is empty → useless code")

    # ✅ Positive reinforcement (important!)
    if not feedback:
        feedback.append("✅ Code looks clean and efficient (for now 👀)")

    return feedback