import logging
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.settings import LlmProviderType
from core.models.settings import LlmModel, SettingsState

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LlmSettings:
    """Immutable container for LLM settings."""
    provider: LlmProviderType
    model_name: Optional[str]
    temperature: float
    temperature_enabled: bool
    inference_timeout: int


class InMemorySettingsService(SettingsService):
    def __init__(self, llama_provider: SettingsLLMProvider, ollama_provider: SettingsLLMProvider):
        super().__init__(llama_provider=llama_provider, ollama_provider=ollama_provider)

        # Initialize settings with defaults
        self._settings = LlmSettings(
            provider=LlmProviderType.LLAMA_CPP,
            model_name='gemma-3n-E4B-it',
            temperature=0.5,
            temperature_enabled=False,
            inference_timeout=30,
        )

        # Map providers to their respective model providers
        self._provider_model_getters: Dict[LlmProviderType, Callable[[], List[LlmModel]]] = {
            LlmProviderType.LLAMA_CPP: self._llama_provider.get_model_list,
            LlmProviderType.OLLAMA: self._ollama_provider.get_model_list
        }

        logger.debug(
            "InMemorySettingsService: Initialized with provider=%s, model=%s, temperature=%.1f",
            self._settings.provider.value,
            self._settings.model_name,
            self._settings.temperature,
        )

    def get_settings_state(self) -> SettingsState:
        """Retrieve full settings state."""
        logger.debug(
            "get_settings_state: Returning state - provider=%s, model=%s, temp=%.1f, temp_enabled=%s",
            self._settings.provider.value,
            self._settings.model_name,
            self._settings.temperature,
            self._settings.temperature_enabled,
        )
        return SettingsState(
            llm_provider=self._settings.provider,
            llm_model_name=self._settings.model_name,
            llm_temperature=self._settings.temperature,
            llm_temperature_enabled=self._settings.temperature_enabled,
        )

    def get_llm_provider(self) -> LlmProviderType:
        """Retrieve current LLM provider."""
        logger.debug("get_llm_provider: Returning %s", self._settings.provider.value)
        return self._settings.provider

    def get_llm_provider_list(self) -> List[LlmProviderType]:
        """Retrieve available LLM providers."""
        providers = list(self._provider_model_getters.keys())
        logger.debug("get_llm_provider_list: Returning %d providers", len(providers))
        return providers

    def get_llm_model(self) -> Optional[LlmModel]:
        """Retrieve current LLM model."""
        if not self._settings.model_name:
            logger.debug("get_llm_model: No model name set")
            return None

        logger.debug("get_llm_model: Returning model %s", self._settings.model_name)
        return LlmModel(
            id=self._settings.model_name,
            name=self._settings.model_name,
            is_available=False,  # TODO: Implement actual availability check
        )

    def get_llm_models_for_selected_provider(self) -> List[LlmModel]:
        """Retrieve models for current provider."""
        current_provider = self._settings.provider
        logger.debug(
            "get_llm_models_for_selected_provider: Fetching models for %s",
            current_provider.value,
        )

        # Use mapping to get the appropriate model getter
        model_getter = self._provider_model_getters.get(current_provider)
        if not model_getter:
            logger.warning(
                "get_llm_models_for_selected_provider: Unknown provider %s",
                current_provider.value,
            )
            return []

        models = model_getter()
        logger.debug(
            "get_llm_models_for_selected_provider: Found %d %s models",
            len(models),
            current_provider.value,
        )
        return models

    def get_llm_temperature(self) -> float:
        """Retrieve current temperature setting."""
        logger.debug("get_llm_temperature: Returning %.1f", self._settings.temperature)
        return self._settings.temperature

    def get_llm_temperature_enabled(self) -> bool:
        """Check if temperature adjustment is enabled."""
        logger.debug("get_llm_temperature_enabled: Returning %s", self._settings.temperature_enabled)
        return self._settings.temperature_enabled

    def set_llm_provider(self, value: LlmProviderType) -> None:
        """Set LLM provider."""
        logger.debug(
            "set_llm_provider: Changing from %s to %s",
            self._settings.provider.value,
            value.value,
        )
        self._settings = LlmSettings(
            provider=value,
            model_name=self._settings.model_name,
            temperature=self._settings.temperature,
            temperature_enabled=self._settings.temperature_enabled,
            inference_timeout=self._settings.inference_timeout,
        )

    def set_llm_model_name(self, value: Optional[str]) -> None:
        """Set LLM model name."""
        logger.debug("set_llm_model_name: Setting model to '%s'", value or "None")
        self._settings = LlmSettings(
            provider=self._settings.provider,
            model_name=value,
            temperature=self._settings.temperature,
            temperature_enabled=self._settings.temperature_enabled,
            inference_timeout=self._settings.inference_timeout,
        )

    def set_llm_temperature(self, value: float) -> None:
        """Set LLM temperature."""
        logger.debug("set_llm_temperature: Setting temperature to %.1f", value)
        self._settings = LlmSettings(
            provider=self._settings.provider,
            model_name=self._settings.model_name,
            temperature=value,
            temperature_enabled=self._settings.temperature_enabled,
            inference_timeout=self._settings.inference_timeout,
        )

    def set_llm_temperature_enabled(self, value: bool) -> None:
        """Enable/disable temperature adjustment."""
        logger.debug("set_llm_temperature_enabled: Setting to %s", value)
        self._settings = LlmSettings(
            provider=self._settings.provider,
            model_name=self._settings.model_name,
            temperature=self._settings.temperature,
            temperature_enabled=value,
            inference_timeout=self._settings.inference_timeout,
        )
