import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the API key from your .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY is not loading correctly.")
else:
    genai.configure(api_key=api_key)
    print("✅ Connected to Google! Here are the models you can use:")
    
    # Ask Google for all available models
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")