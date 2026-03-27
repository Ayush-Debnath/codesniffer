import os
from google import genai

def get_project_ai_insights(summary, results):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return ["⚠️ AI project analysis disabled (no API key)"]

    try:
        client = genai.Client(api_key=api_key)

        # 📊 Compact project summary
        file_info = "\n".join([
            f"{r['file']} → Score: {r['score']}"
            for r in results
        ])

        prompt = f"""
You are a senior software engineer reviewing a codebase.

Project Summary:
- Files analyzed: {summary['total_files']}
- Average score: {summary['avg_score']}
- Total issues: {summary['total_issues']}

File Breakdown:
{file_info}

Give concise, high-level feedback about:
- code quality
- design consistency
- performance risks
- production readiness

Keep it short, structured, and practical.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # 🧹 Clean into bullet points
        lines = [line.strip("* ").strip() for line in text.split("\n") if line.strip()]

        return lines

    except Exception:
        return ["⚠️ AI project-level analysis failed"]