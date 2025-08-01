import logging
from pathlib import Path
from typing import Optional

from config.gguf_models import PREDEFINED_GGUF_MODELS
from core.interfaces.llm_model.model_service import ModelService
from core.interfaces.llm_model.model_service_provider import ModelServiceProvider
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.settings import LlmProviderType
from core.models.settings import ModelInformation
from infra.services.llama_cpp_model_service import LlamaCppModelService
from infra.services.ollama_model_service import OllamaModelService

logger = logging.getLogger(__name__)


class StandardModelServiceProvider(ModelServiceProvider):
    def __init__(self, settings_service: SettingsService, model_folder_path: Path):
        super().__init__(settings_service)
        self._model_folder_path = model_folder_path
        # Cache attributes
        self._cached_service: Optional[ModelService] = None
        self._cached_provider: Optional[LlmProviderType] = None
        self._cached_model_name: Optional[str] = None

        logger.debug(
            "__init__: Initialized with model folder '%s'",
            self._model_folder_path
        )

    def get_model_service(self) -> ModelService:
        """Retrieve or create model service based on current settings."""
        current_provider = self._settings_service.get_llm_provider()
        current_model = self._settings_service.get_llm_model()
        current_model_name = current_model.name if current_model else None

        logger.debug(
            "get_model_service: Requesting service for provider=%s, model=%s",
            current_provider.value,
            current_model_name or "None"
        )

        # Check if cached service is valid for current settings
        cache_reason = None
        if self._cached_service is not None:
            if self._cached_provider != current_provider:
                cache_reason = f"provider changed from {self._cached_provider.value} to {current_provider.value}"
            elif self._cached_model_name != current_model_name:
                cache_reason = f"model changed from '{self._cached_model_name}' to '{current_model_name}'"
            else:
                logger.debug(
                    "get_model_service: Using cached service (provider=%s, model=%s)",
                    current_provider.value,
                    current_model_name
                )
                return self._cached_service

        # Cache miss handling
        if cache_reason:
            logger.debug(
                "get_model_service: Cache miss - %s",
                cache_reason
            )
        else:
            logger.debug("get_model_service: No cached service available")

        # Unload previous model if exists
        if self._cached_service is not None:
            logger.debug(
                "get_model_service: Unloading previous model (provider=%s, model=%s)",
                self._cached_provider.value if self._cached_provider else "None",
                self._cached_model_name or "None"
            )
            self._cached_service.unload_model()

        # Create new service based on provider
        try:
            if current_provider == LlmProviderType.OLLAMA:
                if not current_model:
                    logger.error("get_model_service: No model selected for Ollama provider")
                    raise ValueError("No model selected for Ollama provider")

                model_info = ModelInformation(
                    name=current_model.name,
                    provider=LlmProviderType.OLLAMA
                )
                logger.debug(
                    "get_model_service: Creating Ollama service for model '%s'",
                    current_model.name
                )
                service = OllamaModelService(model_information=model_info)

            elif current_provider == LlmProviderType.LLAMA_CPP:
                if not current_model:
                    logger.error("get_model_service: No model selected for Llama.cpp provider")
                    raise ValueError("No model selected for Llama.cpp provider")

                found_model_info = None
                for model_info in PREDEFINED_GGUF_MODELS:
                    if model_info.name == current_model.name:
                        found_model_info = model_info
                        break

                if not found_model_info:
                    logger.error(
                        "get_model_service: Model '%s' not found in predefined GGUF models",
                        current_model.name
                    )
                    raise ValueError(f"Model {current_model.name} not found in predefined GGUF models.")

                logger.debug(
                    "get_model_service: Creating Llama.cpp service for model '%s' (file: %s)",
                    current_model.name,
                    found_model_info.fileName
                )
                service = LlamaCppModelService(
                    model_folder_path=self._model_folder_path,
                    model_information=found_model_info
                )

            else:
                logger.error(
                    "get_model_service: Unsupported provider '%s'",
                    current_provider.value
                )
                raise ValueError(f"Provider {current_provider} not supported.")

            # Update cache with new service
            self._cached_provider = current_provider
            self._cached_model_name = current_model_name
            self._cached_service = service

            logger.debug(
                "get_model_service: Successfully created service for provider=%s, model=%s",
                current_provider.value,
                current_model_name
            )
            return service

        except Exception as e:
            logger.error(
                "get_model_service: Failed to create model service",
                exc_info=True
            )
            raise e
