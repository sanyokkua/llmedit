import logging
from pathlib import Path
from typing import Optional, override

from llmedit.config.predefined_gguf_models import PREDEFINED_GGUF_MODELS
from llmedit.core.interfaces.llm_model.model_service import ModelService
from llmedit.core.interfaces.llm_model.model_service_provider import ModelServiceProvider
from llmedit.core.interfaces.settings.settings_service import SettingsService
from llmedit.core.models.enums.llm_provider_type import LlmProviderType
from llmedit.core.models.settings import ModelInformation
from llmedit.infra.services.llama_cpp_model_service import LlamaCppModelService
from llmedit.infra.services.ollama_model_service import OllamaModelService

logger = logging.getLogger(__name__)


class StandardModelServiceProvider(ModelServiceProvider):
    """
    Concrete implementation of ModelServiceProvider that creates and caches ModelService instances.

    Provides model services based on current settings, with caching to avoid unnecessary
    model reloading. Supports both Llama.cpp and Ollama providers.
    """

    def __init__(self, settings_service: SettingsService, model_folder_path: Path):
        """
        Initialize provider with settings service and model storage path.

        Args:
            settings_service: Service providing current LLM configuration.
            model_folder_path: Directory where GGUF model files are stored.

        Notes:
            Maintains a cache of the current model service to optimize performance
            when repeatedly requesting the same model.
        """
        super().__init__(settings_service)
        self._model_folder_path = model_folder_path
        self._cached_service: Optional[ModelService] = None
        self._cached_provider: Optional[LlmProviderType] = None
        self._cached_model_name: Optional[str] = None

        logger.debug(
            "__init__: Initialized with model folder '%s'",
            self._model_folder_path,
        )

    @override
    def get_model_service(self) -> ModelService:
        """
        Retrieve or create model service based on current settings.

        Returns:
            ModelService instance configured for the currently selected provider and model.

        Raises:
            ValueError: If selected provider is unsupported or model is not found.
            Exception: If service creation fails for any reason.

        Notes:
            Returns cached service if settings haven't changed. Otherwise, creates
            new service and unloads previous one. Thread-safety is not guaranteed.
        """
        current_provider = self._settings_service.get_llm_provider()
        current_model = self._settings_service.get_llm_model()
        current_model_name = current_model.name if current_model else None

        logger.debug(
            "get_model_service: Requesting service for provider=%s, model=%s",
            current_provider.value,
            current_model_name or "None",
        )

        if self._is_cache_valid(current_provider, current_model_name):
            logger.debug(
                "get_model_service: Using cached service (provider=%s, model=%s)",
                current_provider.value,
                current_model_name,
            )
            return self._cached_service

        self._handle_cache_miss()

        if self._cached_service is not None:
            logger.debug(
                "get_model_service: Unloading previous model (provider=%s, model=%s)",
                self._cached_provider.value if self._cached_provider else "None",
                self._cached_model_name or "None",
            )
            self._cached_service.unload_model()

        try:
            service = self._create_service_for_provider(current_provider, current_model)

            self._cached_provider = current_provider
            self._cached_model_name = current_model_name
            self._cached_service = service

            logger.debug(
                "get_model_service: Successfully created service for provider=%s, model=%s",
                current_provider.value,
                current_model_name,
            )
            return service

        except Exception:
            logger.error(
                "get_model_service: Failed to create model service",
                exc_info=True,
            )
            raise

    def _is_cache_valid(self, current_provider: LlmProviderType, current_model_name: Optional[str]) -> bool:
        """
        Check if the cached service is valid for current settings.

        Args:
            current_provider: The currently selected LLM provider.
            current_model_name: The currently selected model name, or None.

        Returns:
            True if cached service can be reused, False otherwise.

        Notes:
            Cache is invalid if provider or model name has changed since last service creation.
        """
        if self._cached_service is None:
            return False

        if self._cached_provider != current_provider:
            logger.debug(
                "get_model_service: Cache miss - provider changed from %s to %s",
                self._cached_provider.value,
                current_provider.value,
            )
            return False

        if self._cached_model_name != current_model_name:
            logger.debug(
                "get_model_service: Cache miss - model changed from '%s' to '%s'",
                self._cached_model_name,
                current_model_name,
            )
            return False

        return True

    def _handle_cache_miss(self) -> None:
        """
        Log cache miss information.

        Notes:
            Currently only logs when no cached service exists. More detailed logging
            is handled by the _is_cache_valid method.
        """
        if self._cached_service is None:
            logger.debug("get_model_service: No cached service available")

    def _create_service_for_provider(self, provider: LlmProviderType, model) -> ModelService:
        """
        Create model service based on provider type.

        Args:
            provider: The LLM provider type to create service for.
            model: The model configuration to use.

        Returns:
            Newly created ModelService instance.

        Raises:
            ValueError: If provider is not supported.
        """
        if provider == LlmProviderType.OLLAMA:
            return self._create_ollama_service(model)
        elif provider == LlmProviderType.LLAMA_CPP:
            return self._create_llama_cpp_service(model)
        else:
            logger.error(
                "get_model_service: Unsupported provider '%s'",
                provider.value,
            )
            raise ValueError(f"Provider {provider} not supported.")

    @staticmethod
    def _create_ollama_service(model) -> ModelService:
        """
        Create Ollama model service for the given model.

        Args:
            model: The model configuration to use.

        Returns:
            OllamaModelService instance.

        Raises:
            ValueError: If no model is selected.
        """
        if not model:
            logger.error("get_model_service: No model selected for Ollama provider")
            raise ValueError("No model selected for Ollama provider")

        model_info = ModelInformation(
            name=model.name,
            provider=LlmProviderType.OLLAMA,
        )
        logger.debug(
            "get_model_service: Creating Ollama service for model '%s'",
            model.name,
        )
        return OllamaModelService(model_information=model_info)

    def _create_llama_cpp_service(self, model) -> ModelService:
        """
        Create Llama.cpp model service for the given model.

        Args:
            model: The model configuration to use.

        Returns:
            LlamaCppModelService instance.

        Raises:
            ValueError: If no model is selected or model is not found in predefined list.
        """
        if not model:
            logger.error("get_model_service: No model selected for Llama.cpp provider")
            raise ValueError("No model selected for Llama.cpp provider")

        found_model_info = None
        for model_info in PREDEFINED_GGUF_MODELS:
            if model_info.name == model.name:
                found_model_info = model_info
                break

        if not found_model_info:
            logger.error(
                "get_model_service: Model '%s' not found in predefined GGUF models",
                model.name,
            )
            raise ValueError(f"Model {model.name} not found in predefined GGUF models.")

        logger.debug(
            "get_model_service: Creating Llama.cpp service for model '%s' (file: %s)",
            model.name,
            found_model_info.fileName,
        )
        return LlamaCppModelService(
            model_folder_path=self._model_folder_path,
            model_information=found_model_info,
        )
