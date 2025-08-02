import logging
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.llm_provider_type import LlmProviderType
from core.models.settings import LlmModel, SettingsState

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LlmSettings:
    """Immutable container for LLM settings.

    Holds all LLM-related configuration as an immutable snapshot to ensure
    consistent state throughout the application.
    """
    provider: LlmProviderType
    model_name: Optional[str]
    temperature: float
    temperature_enabled: bool
    inference_timeout: int


class InMemorySettingsService(SettingsService):
    """
    In-memory implementation of SettingsService using LlmSettings dataclass.

    Stores and manages LLM configuration including provider, model, and generation parameters.
    All settings are kept in a single immutable LlmSettings instance that is replaced on update.
    """

    def __init__(self, llama_provider: SettingsLLMProvider, ollama_provider: SettingsLLMProvider):
        """
        Initialize service with model providers for each LLM backend.

        Args:
            llama_provider: Provider for llama.cpp-compatible models.
            ollama_provider: Provider for Ollama-compatible models.

        Notes:
            Initializes with default settings and maps providers to their model retrieval functions.
        """
        super().__init__(llama_provider=llama_provider, ollama_provider=ollama_provider)

        self._settings = LlmSettings(
            provider=LlmProviderType.LLAMA_CPP,
            model_name='gemma-3n-E4B-it',
            temperature=0.5,
            temperature_enabled=False,
            inference_timeout=30,
        )

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
        """
        Retrieve full settings state as a SettingsState object.

        Returns:
            Current state of all LLM settings including provider, model, and temperature.

        Notes:
            Used to synchronize UI components with current configuration.
        """
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
        """
        Retrieve current LLM provider.

        Returns:
            The currently selected LLM provider type.
        """
        logger.debug("get_llm_provider: Returning %s", self._settings.provider.value)
        return self._settings.provider

    def get_llm_provider_list(self) -> List[LlmProviderType]:
        """
        Retrieve available LLM providers.

        Returns:
            List of all supported LLM providers (e.g., LLAMA_CPP, OLLAMA).

        Notes:
            Derived from initialized provider getters; reflects runtime capabilities.
        """
        providers = list(self._provider_model_getters.keys())
        logger.debug("get_llm_provider_list: Returning %d providers", len(providers))
        return providers

    def get_llm_model(self) -> Optional[LlmModel]:
        """
        Retrieve current LLM model.

        Returns:
            LlmModel instance representing the currently selected model, or None if not set.

        Notes:
            Returns a minimal LlmModel with is_available=False until availability checking is implemented.
        """
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
        """
        Retrieve models available for the currently selected provider.

        Returns:
            List of LlmModel instances supported by the current provider.

        Notes:
            Delegates to the provider-specific model getter function.
            Returns empty list if provider is unknown or retrieval fails.
        """
        current_provider = self._settings.provider
        logger.debug(
            "get_llm_models_for_selected_provider: Fetching models for %s",
            current_provider.value,
        )

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
        """
        Retrieve current temperature setting.

        Returns:
            Temperature value used for text generation (controls randomness).
        """
        logger.debug("get_llm_temperature: Returning %.1f", self._settings.temperature)
        return self._settings.temperature

    def get_llm_temperature_enabled(self) -> bool:
        """
        Check if temperature adjustment is enabled.

        Returns:
            True if temperature parameter should be applied, False otherwise.
        """
        logger.debug("get_llm_temperature_enabled: Returning %s", self._settings.temperature_enabled)
        return self._settings.temperature_enabled

    def set_llm_provider(self, value: LlmProviderType) -> None:
        """
        Set LLM provider.

        Args:
            value: The new LLM provider type to use.

        Notes:
            Preserves other settings while updating provider.
            Triggers internal settings state replacement.
        """
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
        """
        Set LLM model name.

        Args:
            value: Name of the model to use, or None to clear selection.

        Notes:
            Does not validate model existence; validation occurs at usage time.
        """
        logger.debug("set_llm_model_name: Setting model to '%s'", value or "None")
        self._settings = LlmSettings(
            provider=self._settings.provider,
            model_name=value,
            temperature=self._settings.temperature,
            temperature_enabled=self._settings.temperature_enabled,
            inference_timeout=self._settings.inference_timeout,
        )

    def set_llm_temperature(self, value: float) -> None:
        """
        Set LLM temperature.

        Args:
            value: New temperature value between 0.0 (deterministic) and high values (more random).

        Notes:
            Value is stored regardless of temperature_enabled flag.
        """
        logger.debug("set_llm_temperature: Setting temperature to %.1f", value)
        self._settings = LlmSettings(
            provider=self._settings.provider,
            model_name=self._settings.model_name,
            temperature=value,
            temperature_enabled=self._settings.temperature_enabled,
            inference_timeout=self._settings.inference_timeout,
        )

    def set_llm_temperature_enabled(self, value: bool) -> None:
        """
        Enable or disable temperature adjustment.

        Args:
            value: True to enable temperature application, False to ignore it.

        Notes:
            Disabling does not change the stored temperature value.
        """
        logger.debug("set_llm_temperature_enabled: Setting to %s", value)
        self._settings = LlmSettings(
            provider=self._settings.provider,
            model_name=self._settings.model_name,
            temperature=self._settings.temperature,
            temperature_enabled=value,
            inference_timeout=self._settings.inference_timeout,
        )
