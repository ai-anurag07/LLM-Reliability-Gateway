import os
from groq import Groq
from app.routing.providers.base import BaseProvider

class GroqProvider(BaseProvider):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.default_model = "llama-3.1-8b-instant" # Updated free Groq model

    def generate(self, prompt: str, **kwargs) -> dict:
        model = kwargs.get("model", self.default_model)
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )
        
        return {
            "text": response.choices[0].message.content,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "provider_name": "Groq",
            "model_name": model
        }
    
    def get_name(self): return "ProviderName"