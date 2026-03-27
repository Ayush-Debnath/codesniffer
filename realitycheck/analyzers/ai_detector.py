import os
from google import genai

def get_ai_feedback(code):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return ["⚠️ Gemini API key not found"]

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are a senior software engineer.

Analyze the following Python code and give short, brutally honest feedback.

Focus on:
- performance issues
- bad design
- readability
- production readiness

Keep it concise.

Code:
{code}
"""
        )

        return [response.text.strip()]

    except Exception as e:
        return [f"⚠️ AI analysis failed: {str(e)}"]