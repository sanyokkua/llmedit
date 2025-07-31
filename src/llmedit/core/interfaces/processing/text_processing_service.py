from abc import ABC, abstractmethod

from core.interfaces.llm_model.model_service_provider import ModelServiceProvider
from core.interfaces.processing.text_sanitization_service import TextSanitizationService
from core.interfaces.prompt.prompt_service import PromptService
from core.interfaces.settings.settings_service import SettingsService
from core.models.data_types import ProcessingContext, GenerationRequest, GenerationResponse


class TextProcessingService(ABC):
    def __init__(self,
                 settings_service: SettingsService,
                 sanitizer_service: TextSanitizationService,
                 model_service_provider: ModelServiceProvider,
                 prompt_service: PromptService
                 ):
        self._settings_service = settings_service
        self._sanitizer_service = sanitizer_service
        self._model_service_provider = model_service_provider
        self._prompt_service = prompt_service

    @abstractmethod
    def process(self, processing_context: ProcessingContext) -> str:
        pass

    @abstractmethod
    def _execute_task(self, request: GenerationRequest) -> GenerationResponse: pass
