import os
import requests
import sys

def analyze_failure(test_output):
    """Send test failure to Gemini AI and get explanation."""
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("No Gemini API key found")
        return
    
    prompt = f"""You are a Python testing expert for Smart City software.

A CI/CD pipeline test just failed with this output:

{test_output}

Explain in clear simple language:
1. Why did this test fail?
2. Exactly how to fix it?
3. What impact does this bug have on the Smart City system?

Be specific. Reference the actual values and function names from the output."""

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={gemini_key}"
        
        response = requests.post(url, json={
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        })
        
        result = response.json()
        ai_analysis = result["candidates"][0]["content"]["parts"][0]["text"]
        
        print("\n" + "="*60)
        print("AI ANALYSIS OF TEST FAILURE (Powered by Gemini)")
        print("="*60)
        print(ai_analysis)
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"AI analysis error: {e}")

if __name__ == "__main__":
    test_output = sys.stdin.read()
    if test_output:
        analyze_failure(test_output)