from abc import ABC, abstractmethod

from core.interfaces.llm_model.model_service_provider import ModelServiceProvider
from core.interfaces.processing.text_sanitization_service import TextSanitizationService
from core.interfaces.prompt.prompt_service import PromptService
from core.interfaces.settings.settings_service import SettingsService
from core.models.data_types import GenerationRequest, GenerationResponse, ProcessingContext


class TextProcessingService(ABC):
    """
    Abstract base class for text processing pipelines that generate and sanitize text.

    Coordinates prompt formatting, model execution, and response sanitization to produce
    final output text from structured input contexts. Manages dependencies through constructor injection.
    """

    def __init__(
        self,
        settings_service: SettingsService,
        sanitizer_service: TextSanitizationService,
        model_service_provider: ModelServiceProvider,
        prompt_service: PromptService,
    ):
        """
        Initialize the text processing service with required dependencies.

        Args:
            settings_service: Provides current LLM and application settings.
            sanitizer_service: Used to clean and validate generated text.
            model_service_provider: Provides access to the active model service.
            prompt_service: Manages prompt retrieval and parameterization.
        """
        self._settings_service = settings_service
        self._sanitizer_service = sanitizer_service
        self._model_service_provider = model_service_provider
        self._prompt_service = prompt_service

    @abstractmethod
    def process(self, processing_context: ProcessingContext) -> str:
        """
        Process input context into final text output through the generation pipeline.

        Args:
            processing_context: Contains prompt ID and parameters for generation.

        Returns:
            Sanitized generated text, or empty string if processing fails.

        Notes:
            Implementations should handle model loading, prompt preparation, generation,
            and sanitization. Should return empty string on any error condition.
        """

    @abstractmethod
    def _execute_task(self, request: GenerationRequest) -> GenerationResponse:
        """
        Execute a generation request using the underlying model service.

        Args:
            request: Contains system prompt, user prompt, and sampling parameters.

        Returns:
            GenerationResponse with the model-generated text content.

        Notes:
            This internal method performs the actual model inference call.
            Must be implemented by subclasses to use the appropriate model backend.
        """
