from pathlib import Path
from typing import List

from core.abstracts.providers import LLMProvider, LLMModelClientProvider
from core.abstracts.services import SettingsService
from core.abstracts.types import AppLLMProviderType
from core.services.llms.providers.llama_cpp_provider import LlamaCppProvider
from core.services.llms.providers.ollama_provider import OllamaProvider


class AppLlmProvider(LLMProvider):
    def __init__(self, local_model_dir: Path, settings_service: SettingsService):
        self.local_model_dir = local_model_dir
        self.settings_service = settings_service
        self.ollama_provider: OllamaProvider | None = None
        self.llama_cpp_provider: LlamaCppProvider | None = None

    def get_llm_provider(self) -> LLMModelClientProvider:
        settings = self.settings_service.get_settings()
        temperature = settings.model_temperature
        provider = settings.app_llm_provider

        if provider == AppLLMProviderType.OLLAMA:
            if self.llama_cpp_provider is not None:
                self.llama_cpp_provider.unload_model()
            if self.ollama_provider is None:
                self.ollama_provider = OllamaProvider(temperature=temperature)
            return self.ollama_provider
        elif provider == AppLLMProviderType.LLAMA_CPP:
            if self.ollama_provider is not None:
                self.ollama_provider.unload_model()
            if self.llama_cpp_provider is None:
                self.llama_cpp_provider = LlamaCppProvider(model_dir=self.local_model_dir, temperature=temperature)
            return self.llama_cpp_provider

        raise ValueError(f"Invalid LLM provider: {provider}")

    def get_available_providers(self) -> List[str]:
        return [AppLLMProviderType.LLAMA_CPP, AppLLMProviderType.OLLAMA]
