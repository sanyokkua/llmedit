from abc import ABC, abstractmethod
from typing import List, Optional

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.models.enums.settings import LlmProviderType
from core.models.settings import LlmModel, SettingsState


class SettingsService(ABC):
    def __init__(self,
                 llama_provider: SettingsLLMProvider,
                 ollama_provider: SettingsLLMProvider,
                 ):
        self._llama_provider = llama_provider
        self._ollama_provider = ollama_provider

    @abstractmethod
    def get_settings_state(self) -> SettingsState: pass

    @abstractmethod
    def get_llm_provider(self) -> LlmProviderType: pass

    @abstractmethod
    def get_llm_provider_list(self) -> List[LlmProviderType]: pass

    @abstractmethod
    def get_llm_model(self) -> Optional[LlmModel]: pass

    @abstractmethod
    def get_llm_models_for_selected_provider(self) -> List[LlmModel]: pass

    @abstractmethod
    def get_llm_temperature(self) -> float: pass

    @abstractmethod
    def get_llm_temperature_enabled(self) -> bool: pass

    @abstractmethod
    def set_llm_provider(self, value: LlmProviderType) -> None: pass

    @abstractmethod
    def set_llm_model_name(self, value: Optional[str]) -> None: pass

    @abstractmethod
    def set_llm_temperature(self, value: float) -> None: pass

    @abstractmethod
    def set_llm_temperature_enabled(self, value: bool) -> None: pass
