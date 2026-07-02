from typing import List
import random
from app.routing.providers.base import BaseProvider

class Router:
    def __init__(self, providers: List[BaseProvider]):
        self.providers = providers

    def fallback_route(self, prompt: str, **kwargs) -> dict:
        """Tries providers in order. If one fails, goes to the next."""
        errors = []
        for provider in self.providers:
            provider_name = provider.__class__.__name__
            try:
                print(f"🔄 Trying provider: {provider_name}...")
                return provider.generate(prompt, **kwargs)
            except Exception as e:
                errors.append(f"{provider_name}: {str(e)}")
                continue
        raise Exception(f"All providers failed! Errors: {errors}")

    def cheapest_route(self, prompt: str, **kwargs) -> dict:
        """Picks the cheapest provider. Since Groq/Gemini are free, it picks Groq (it's faster)."""
        # In a real paid environment, you would sort by cost-per-token here.
        print("💰 Routing to the cheapest provider (Groq - Free)...")
        # Assuming Groq is the first one in our list
        return self.providers[0].generate(prompt, **kwargs)

    def fastest_route(self, prompt: str, **kwargs) -> dict:
        """
        In production, this would read rolling average latency from Redis.
        For now, we know Groq is generally faster than Gemini.
        """
        print("⚡ Routing based on speed...")
        return self.fallback_route(prompt, **kwargs)

    def generate(self, prompt: str, policy: str = "fallback", **kwargs) -> dict:
        if policy == "cheapest":
            return self.cheapest_route(prompt, **kwargs)
        elif policy == "fastest":
            return self.fastest_route(prompt, **kwargs)
        else:
            return self.fallback_route(prompt, **kwargs)