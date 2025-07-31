from pathlib import Path

from config.gguf_models import PREDEFINED_GGUF_MODELS
from core.interfaces.llm_model.model_service import ModelService
from core.interfaces.llm_model.model_service_provider import ModelServiceProvider
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.settings import LlmProviderType
from core.models.settings import ModelInformation
from infra.services.llama_cpp_model_service import LlamaCppModelService
from infra.services.ollama_model_service import OllamaModelService


class StandardModelServiceProvider(ModelServiceProvider):
    def __init__(self, settings_service: SettingsService, model_folder_path: Path):
        super().__init__(settings_service)
        self._model_folder_path = model_folder_path
        # Cache attributes
        self._cached_service: ModelService | None = None
        self._cached_provider: LlmProviderType | None = None
        self._cached_model_name: str | None = None

    def get_model_service(self) -> ModelService:
        current_provider = self._settings_service.get_llm_provider()
        current_model = self._settings_service.get_llm_model()
        current_model_name = current_model.name if current_model else None

        # Check if cached service is valid for current settings
        if (self._cached_service is not None and
                self._cached_provider == current_provider and
                self._cached_model_name == current_model_name):
            return self._cached_service

        if self._cached_service is not None:
            self._cached_service.unload_model()

        # Create new service if cache miss or settings changed
        if current_provider == LlmProviderType.OLLAMA:
            if current_model is None:
                raise ValueError("No model selected for Ollama provider")
            model_info = ModelInformation(
                name=current_model.name,
                provider=LlmProviderType.OLLAMA
            )
            service = OllamaModelService(model_information=model_info)

        elif current_provider == LlmProviderType.LLAMA_CPP:
            if current_model is None:
                raise ValueError("No model selected for Llama.cpp provider")

            found_model_info = None
            for model_info in PREDEFINED_GGUF_MODELS:
                if model_info.name == current_model.name:
                    found_model_info = model_info
                    break

            if found_model_info is None:
                raise ValueError(f"Model {current_model.name} not found in predefined GGUF models.")

            service = LlamaCppModelService(
                model_folder_path=self._model_folder_path,
                model_information=found_model_info
            )

        else:
            raise ValueError(f"Provider {current_provider} not supported.")

        # Update cache with new service
        self._cached_provider = current_provider
        self._cached_model_name = current_model_name
        self._cached_service = service

        return service
