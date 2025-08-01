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

        logger.debug(
            "InMemorySettingsService: Initialized with provider=%s, model=%s, temperature=%.1f",
            self.llm_provider.value,
            self.llm_model_name,
            self.llm_temperature
        )

    def get_settings_state(self) -> SettingsState:
        """Retrieve full settings state."""
        logger.debug(
            "get_settings_state: Returning state - provider=%s, model=%s, temp=%.1f, temp_enabled=%s",
            self.llm_provider.value,
            self.llm_model_name,
            self.llm_temperature,
            self.llm_temperature_enabled
        )
        return SettingsState(
            llm_provider=self.llm_provider,
            llm_model_name=self.llm_model_name,
            llm_temperature=self.llm_temperature,
            llm_temperature_enabled=self.llm_temperature_enabled,
        )

    def get_llm_provider(self) -> LlmProviderType:
        """Retrieve current LLM provider."""
        logger.debug("get_llm_provider: Returning %s", self.llm_provider.value)
        return self.llm_provider

    def get_llm_provider_list(self) -> List[LlmProviderType]:
        """Retrieve available LLM providers."""
        providers = [LlmProviderType.LLAMA_CPP, LlmProviderType.OLLAMA]
        logger.debug("get_llm_provider_list: Returning %d providers", len(providers))
        return providers

    def get_llm_model(self) -> Optional[LlmModel]:
        """Retrieve current LLM model."""
        logger.debug("get_llm_model: Returning model %s", self.llm_model_name)
        return LlmModel(
            id=self.llm_model_name,
            name=self.llm_model_name,
            is_available=False
        )

    def get_llm_models_for_selected_provider(self) -> List[LlmModel]:
        """Retrieve models for current provider."""
        current_provider = self.llm_provider
        logger.debug("get_llm_models_for_selected_provider: Fetching models for %s", current_provider.value)

        if current_provider == LlmProviderType.OLLAMA:
            models = self._ollama_provider.get_model_list()
            logger.debug("get_llm_models_for_selected_provider: Found %d Ollama models", len(models))
            return models
        elif current_provider == LlmProviderType.LLAMA_CPP:
            models = self._llama_provider.get_model_list()
            logger.debug("get_llm_models_for_selected_provider: Found %d LLAMA_CPP models", len(models))
            return models

        logger.warning("get_llm_models_for_selected_provider: Unknown provider %s", current_provider.value)
        return []

    def get_llm_temperature(self) -> float:
        """Retrieve current temperature setting."""
        logger.debug("get_llm_temperature: Returning %.1f", self.llm_temperature)
        return self.llm_temperature

    def get_llm_temperature_enabled(self) -> bool:
        """Check if temperature adjustment is enabled."""
        logger.debug("get_llm_temperature_enabled: Returning %s", self.llm_temperature_enabled)
        return self.llm_temperature_enabled

    def set_llm_provider(self, value: LlmProviderType) -> None:
        """Set LLM provider."""
        logger.debug("set_llm_provider: Changing from %s to %s", self.llm_provider.value, value.value)
        self.llm_provider = value

    def set_llm_model_name(self, value: Optional[str]) -> None:
        """Set LLM model name."""
        logger.debug("set_llm_model_name: Setting model to '%s'", value or "None")
        self.llm_model_name = value

    def set_llm_temperature(self, value: float) -> None:
        """Set LLM temperature."""
        logger.debug("set_llm_temperature: Setting temperature to %.1f", value)
        self.llm_temperature = value

    def set_llm_temperature_enabled(self, value: bool) -> None:
        """Enable/disable temperature adjustment."""
        logger.debug("set_llm_temperature_enabled: Setting to %s", value)
        self.llm_temperature_enabled = value
