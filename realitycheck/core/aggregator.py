def aggregate_project(results):
    summary = {
        "total_files": len(results),
        "avg_score": 0,
        "worst_file": None,
        "total_issues": 0
    }

    if not results:
        return summary

    # 📊 Average score
    total_score = sum(r["score"] for r in results)
    summary["avg_score"] = round(total_score / len(results), 2)

    # ❌ Worst file
    worst = min(results, key=lambda x: x["score"])
    summary["worst_file"] = worst["file"]

    # ⚠️ Total issues
    summary["total_issues"] = sum(r["issues"] for r in results)

    return summary

def generate_project_insights(results):
    insights = []

    if not results:
        return insights

    # 🚨 Low quality project
    avg_score = sum(r["score"] for r in results) / len(results)
    if avg_score < 6:
        insights.append("🚨 Overall project quality is low → needs major refactoring")

    # ⚠️ Many issues
    total_issues = sum(r["issues"] for r in results)
    if total_issues > 10:
        insights.append("⚠️ High number of issues detected across project")

    # ⚡ Consistency check
    scores = [r["score"] for r in results]
    if max(scores) - min(scores) > 4:
        insights.append("⚠️ Inconsistent code quality across files")

    # 🔥 High performer
    if avg_score > 8:
        insights.append("✅ Project is generally well-structured")

    return insights