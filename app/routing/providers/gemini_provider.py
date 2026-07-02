import os
import google.generativeai as genai
from app.routing.providers.base import BaseProvider

class GeminiProvider(BaseProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing")
        genai.configure(api_key=api_key)
        # Use the newest free model from your list!
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate(self, prompt: str, **kwargs) -> dict:
        response = self.model.generate_content(prompt)
        
        return {
            "text": response.text,
            "prompt_tokens": 0, 
            "completion_tokens": 0,
            "provider_name": "Gemini",
            "model_name": "gemini-2.5-flash"
        }
    
    def get_name(self): return "ProviderName"