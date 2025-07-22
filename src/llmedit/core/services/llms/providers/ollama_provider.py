from typing import List

import ollama

from core.abstracts.providers import LLMModelClientProvider
from core.abstracts.services import LLMModelClient
from core.services.llms.clients.ollama_client import OllamaModelClient


class OllamaProvider(LLMModelClientProvider):
    def __init__(self, temperature: float = 0.5):
        self.last_used_model: str | None = None
        self.temperature = temperature

    def get_model_client(self) -> LLMModelClient:
        return OllamaModelClient(model_name=self.last_used_model, temperature=self.temperature)

    def get_available_models(self) -> List[str]:
        ollama_list = ollama.list()
        models = [model['model'] for model in ollama_list.models]
        print(models)
        return models

    def load_model(self, model_name: str) -> None:
        self.last_used_model = model_name

    def unload_model(self) -> None:
        self.last_used_model = None
