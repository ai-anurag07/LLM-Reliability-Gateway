from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Must return a standardized dictionary containing:
        - text: The generated response
        - prompt_tokens: int
        - completion_tokens: int
        - provider_name: str
        - model_name: str
        """
        pass

    def get_name(self): return "ProviderName"