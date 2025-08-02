from abc import ABC, abstractmethod
from typing import List, Optional

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.models.enums.llm_provider_type import LlmProviderType
from core.models.settings import LlmModel, SettingsState


class SettingsService(ABC):
    """
    Abstract base class defining the interface for application settings management.

    Handles storage and retrieval of LLM-related configuration including provider,
    model selection, and generation parameters. Supports both getting and updating settings.
    """

    def __init__(
        self,
        llama_provider: SettingsLLMProvider,
        ollama_provider: SettingsLLMProvider,
    ):
        """
        Initialize the settings service with model providers for each backend.

        Args:
            llama_provider: Provider for llama.cpp-compatible models.
            ollama_provider: Provider for Ollama-compatible models.

        Notes:
            Providers are used to fetch available models based on the selected LLM provider.
        """
        self._llama_provider = llama_provider
        self._ollama_provider = ollama_provider

    @abstractmethod
    def get_settings_state(self) -> SettingsState:
        """
        Retrieve the complete current settings state.

        Returns:
            SettingsState object containing all LLM configuration values.

        Notes:
            Used to synchronize UI components with current settings.
        """

    @abstractmethod
    def get_llm_provider(self) -> LlmProviderType:
        """
        Get the currently selected LLM provider.

        Returns:
            The active LLM provider type (e.g., LLAMA_CPP, OLLAMA).
        """

    @abstractmethod
    def get_llm_provider_list(self) -> List[LlmProviderType]:
        """
        Get the list of available LLM providers.

        Returns:
            List of supported LLM provider types.

        Notes:
            Reflects the providers available in the current runtime environment.
        """

    @abstractmethod
    def get_llm_model(self) -> Optional[LlmModel]:
        """
        Get the currently selected LLM model.

        Returns:
            LlmModel object representing the current model, or None if not set.

        Notes:
            Returns basic model info; availability status may not be up-to-date.
        """

    @abstractmethod
    def get_llm_models_for_selected_provider(self) -> List[LlmModel]:
        """
        Get all models available for the currently selected provider.

        Returns:
            List of LlmModel objects that can be used with the current provider.

        Notes:
            Delegates to the appropriate SettingsLLMProvider based on current selection.
        """

    @abstractmethod
    def get_llm_temperature(self) -> float:
        """
        Get the current temperature setting for text generation.

        Returns:
            Temperature value (higher = more random, lower = more deterministic).
        """

    @abstractmethod
    def get_llm_temperature_enabled(self) -> bool:
        """
        Check if temperature adjustment is currently enabled.

        Returns:
            True if temperature should be applied during generation, False otherwise.
        """

    @abstractmethod
    def set_llm_provider(self, value: LlmProviderType) -> None:
        """
        Set the LLM provider.

        Args:
            value: The new LLM provider type to use.

        Notes:
            Changing provider may affect available models and settings.
        """

    @abstractmethod
    def set_llm_model_name(self, value: Optional[str]) -> None:
        """
        Set the name of the LLM model to use.

        Args:
            value: Model name to set, or None to clear selection.

        Notes:
            Does not validate that the model exists for the current provider.
        """

    @abstractmethod
    def set_llm_temperature(self, value: float) -> None:
        """
        Set the temperature value for text generation.

        Args:
            value: New temperature value (typically between 0.0 and 2.0).

        Notes:
            Value is stored even if temperature adjustment is currently disabled.
        """

    @abstractmethod
    def set_llm_temperature_enabled(self, value: bool) -> None:
        """
        Enable or disable temperature adjustment.

        Args:
            value: True to enable temperature application, False to ignore it.

        Notes:
            Does not change the stored temperature value.
        """

    @abstractmethod
    def set_source_language(self, value: str) -> None:
        """
        Set the default source language"""

    @abstractmethod
    def set_target_language(self, value: str) -> None:
        """
        Set the default target language"""

    @abstractmethod
    def get_source_language(self) -> str:
        """Get the default source language"""

    @abstractmethod
    def get_target_language(self) -> str:
        """Get the default source language"""
