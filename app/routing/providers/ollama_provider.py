import httpx
from app.routing.providers.base import BaseProvider

class OllamaProvider(BaseProvider):
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.default_model = "llama3" 

    def generate(self, prompt: str, **kwargs) -> dict:
        model = kwargs.get("model", self.default_model)
        payload = {"model": model, "prompt": prompt, "stream": False}
        
        with httpx.Client() as client:
            response = client.post(self.base_url, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
        return {
            "text": data.get("response", ""),
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": data.get("eval_count", 0),
            "provider_name": "Ollama",
            "model_name": model
        }
    def get_name(self): return "ProviderName"