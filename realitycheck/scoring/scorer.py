def calculate_score(complexity, smells):
    score = 10.0

    breakdown = {
        "performance": 10,
        "readability": 10,
        "design": 10
    }

    # 🚨 Performance penalties
    if complexity["nested_loops"] > 0:
        breakdown["performance"] -= 3

    if complexity["total_loops"] > 3:
        breakdown["performance"] -= 2

    # 🚨 Readability penalties
    if smells["bad_function_names"]:
        breakdown["readability"] -= len(smells["bad_function_names"]) * 1

    if smells["empty_functions"]:
        breakdown["readability"] -= 2

    # 🚨 Design penalties
    if smells["too_many_arguments"]:
        breakdown["design"] -= len(smells["too_many_arguments"]) * 2

    for func in complexity["long_functions"]:
        breakdown["design"] -= 2

    # Clamp values between 0 and 10
    for key in breakdown:
        breakdown[key] = max(0, breakdown[key])

    # Final score (average)
    final_score = sum(breakdown.values()) / len(breakdown)

    return round(final_score, 2), breakdown