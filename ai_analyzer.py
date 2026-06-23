import os
import requests
import sys
import json

def analyze_failure(test_output):
    """Send test failure to Gemini AI and get explanation."""

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("No Gemini API key found")
        sys.exit(1)

    if len(gemini_key) < 30:
        print("Invalid Gemini API key format")
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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code != 200:
            print(f"Gemini API error: {response.status_code}")
            print(response.text)
            return

        result = response.json()

        if "candidates" not in result:
            print("No candidates in response")
            return

        ai_analysis = result["candidates"][0]["content"]["parts"][0]["text"]

        print("\n" + "="*60)
        print("AI ANALYSIS OF TEST FAILURE (Powered by Gemini)")
        print("="*60)
        print(ai_analysis)
        print("="*60 + "\n")

    except requests.Timeout:
        print("Gemini API timed out after 30 seconds")
    except Exception as e:
        print(f"AI analysis failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_output = sys.stdin.read()
    if test_output.strip():
        analyze_failure(test_output)
    else:
        print("No test output received")