import logging
from typing import Optional, List

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.settings import LlmProviderType
from core.models.settings import SettingsState, LlmModel

logger = logging.getLogger(__name__)


class InMemorySettingsService(SettingsService):
    def __init__(self, llama_provider: SettingsLLMProvider, ollama_provider: SettingsLLMProvider):
        super().__init__(llama_provider=llama_provider, ollama_provider=ollama_provider)
        self.llm_provider: LlmProviderType = LlmProviderType.LLAMA_CPP
        self.llm_model_name: Optional[str] = 'gemma-3n-E4B-it'
        self.llm_temperature: float = 0.5
        self.llm_temperature_enabled: bool = False
        self.llm_inference_timeout: int = 30

    def get_settings_state(self) -> SettingsState:
        return SettingsState(
            llm_provider=self.llm_provider,
            llm_model_name=self.llm_model_name,
            llm_temperature=self.llm_temperature,
            llm_temperature_enabled=self.llm_temperature_enabled,
        )

    def get_llm_provider(self) -> LlmProviderType:
        return self.llm_provider

    def get_llm_provider_list(self) -> List[LlmProviderType]:
        return [LlmProviderType.LLAMA_CPP, LlmProviderType.OLLAMA]

    def get_llm_model(self) -> Optional[LlmModel]:
        return LlmModel(
            id=self.llm_model_name,
            name=self.llm_model_name,
            is_available=False
        )

    def get_llm_models_for_selected_provider(self) -> List[LlmModel]:
        if self.llm_provider == LlmProviderType.OLLAMA:
            return self._ollama_provider.get_model_list()
        elif self.llm_provider == LlmProviderType.LLAMA_CPP:
            return self._llama_provider.get_model_list()
        else:
            return []

    def get_llm_temperature(self) -> float:
        return self.llm_temperature

    def get_llm_temperature_enabled(self) -> bool:
        return self.llm_temperature_enabled

    def set_llm_provider(self, value: LlmProviderType) -> None:
        self.llm_provider = value

    def set_llm_model_name(self, value: Optional[str]) -> None:
        self.llm_model_name = value

    def set_llm_temperature(self, value: float) -> None:
        self.llm_temperature = value

    def set_llm_temperature_enabled(self, value: bool) -> None:
        self.llm_temperature_enabled = value
