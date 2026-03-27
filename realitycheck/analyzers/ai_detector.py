import os
from google import genai

def get_ai_feedback(code):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return ["⚠️ AI disabled (no API key)"]

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""You are a senior software engineer.

Analyze the following Python code and give short, brutally honest feedback.

Focus on:
- performance issues
- bad design
- readability
- production readiness

Keep it concise.

Code:
{code}"""
        )

        response_text = response.text.strip()
        lines = [line.strip("* ").strip() for line in response_text.split("\n") if line.strip()]

        return lines

    except Exception:
        return ["⚠️ AI analysis unavailable (fallback mode active)"]