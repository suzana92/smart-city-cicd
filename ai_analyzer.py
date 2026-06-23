import os
import requests
import sys
import json

def analyze_failure(test_output):
    """Send test failure to Groq AI and get explanation."""

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("No Groq API key found")
        sys.exit(1)

    prompt = f"""You are a Python testing expert for Smart City software.

A CI/CD pipeline test just failed with this output:

{test_output}

Explain in clear simple language:
1. Why did this test fail?
2. Exactly how to fix it?
3. What impact does this bug have on the Smart City system?

Be specific. Reference the actual values and function names."""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0
            },
            timeout=30
        )

        if response.status_code != 200:
            print(f"Groq API error: {response.status_code}")
            print(response.text)
            return

        result = response.json()
        ai_analysis = result["choices"][0]["message"]["content"]

        print("\n" + "="*60)
        print("AI ANALYSIS OF TEST FAILURE (Powered by Groq)")
        print("="*60)
        print(ai_analysis)
        print("="*60 + "\n")

    except requests.Timeout:
        print("Groq API timed out")
    except Exception as e:
        print(f"AI analysis failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_output = sys.stdin.read()
    if test_output.strip():
        analyze_failure(test_output)
    else:
        print("No test output received")