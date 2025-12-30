import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'NOT FOUND'}")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    print("Gemini Flash model initialized successfully!")

    # Test a simple generation
    response = model.generate_content("What is 2+2?")
    print(f"Test response: {response.text}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
