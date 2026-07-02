from deepeval.models.base_model import DeepEvalBaseLLM
from app.routing.providers.groq_provider import GroqProvider

class GroqJudge(DeepEvalBaseLLM):
    def __init__(self):
        self.provider = GroqProvider()

    def load_model(self):
        pass

    def generate(self, prompt: str) -> str:
        # We reuse the Groq provider we already built!
        response = self.provider.generate(prompt=prompt)
        return response["text"]

    async def a_generate(self, prompt: str) -> str:
        # DeepEval requires an async method, we just wrap the sync one
        return self.generate(prompt)

    def get_model_name(self):
        return "Groq Evaluator"