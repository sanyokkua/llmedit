import logging
from typing import Tuple

from typing_extensions import override

from config.prompts_objects import ID_PROMPT_SYSTEM
from core.interfaces.processing.text_processing_service import TextProcessingService
from core.models.data_types import (GenerationRequest, GenerationResponse, ProcessingContext, Prompt)

logger = logging.getLogger(__name__)


class TextProcessingServiceBase(TextProcessingService):
    @override
    def process(self, processing_context: ProcessingContext) -> str:
        """
        Process text through the generation pipeline.

        Args:
            processing_context: Context containing prompt information and parameters

        Returns:
            Sanitized generated text or empty string on failure
        """
        logger.debug("process: Starting text processing")
        logger.debug(
            "process: Context received - prompt_id=%s, params_count=%d",
            processing_context.user_prompt_id,
            len(processing_context.prompt_parameters),
        )

        # Guard clause for model loading
        if not self._ensure_model_loaded():
            return ''

        # Validate prompt parameters early
        validation_result, error_message = self._validate_processing_context(processing_context)
        if not validation_result:
            logger.warning("process: Invalid processing context - %s", error_message)
            return ''

        # Prepare generation request
        try:
            request = self._prepare_generation_request(processing_context)
        except Exception as e:
            logger.error("process: Failed to prepare generation request", exc_info=True)
            return ''

        # Execute generation
        try:
            generated_response = self._execute_task(request)
        except Exception as e:
            logger.error("process: Generation request failed", exc_info=True)
            return ''

        # Sanitize and return result
        sanitized_text = self._sanitizer_service.sanitize_text(generated_response.text_content)
        logger.debug(
            "process: Text sanitized - original_len=%d, sanitized_len=%d",
            len(generated_response.text_content),
            len(sanitized_text),
        )

        return sanitized_text

    def _ensure_model_loaded(self) -> bool:
        """Ensure the model is loaded, loading it if necessary."""
        model_service = self._model_service_provider.get_model_service()

        if model_service.is_model_loaded():
            return True

        logger.debug("process: Model not loaded, loading model")
        try:
            model_service.load_model()
            return True
        except Exception as e:
            logger.warning("process: Failed to load model", e, exc_info=True)
            return False

    def _validate_processing_context(self, processing_context: ProcessingContext) -> Tuple[bool, str]:
        """
        Validate the processing context and its parameters.

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            user_prompt = self._prompt_service.get_prompt(processing_context.user_prompt_id)
        except Exception as e:
            return False, f"Failed to retrieve user prompt: {str(e)}"

        is_valid_params, err = self._prompt_service.validate_prompt_parameters(
            user_prompt,
            processing_context.prompt_parameters,
        )

        return is_valid_params, err

    def _prepare_generation_request(self, processing_context: ProcessingContext) -> GenerationRequest:
        """
        Prepare the generation request from processing context.

        Raises:
            Exception: If prompt preparation fails
        """
        # Get model information and settings
        model_service = self._model_service_provider.get_model_service()
        model_info = model_service.get_model_information()

        is_temperature_enabled = self._settings_service.get_llm_temperature_enabled()
        settings_temp = self._settings_service.get_llm_temperature()

        temperature: float = settings_temp if is_temperature_enabled else model_info.temperature

        # Retrieve prompts
        system_prompt = self._prompt_service.get_prompt(ID_PROMPT_SYSTEM)
        user_prompt = self._prompt_service.get_prompt(processing_context.user_prompt_id)

        logger.debug("process: System prompt retrieved - id=%s", system_prompt.id)
        logger.debug(
            "process: User prompt retrieved - id=%s, category=%s",
            user_prompt.id,
            user_prompt.category.value,
        )

        # Prepare prompt templates
        system_prompt_template = self._build_system_prompt(model_info, system_prompt)
        user_prompt_template = self._build_user_prompt(model_info, user_prompt, processing_context)

        logger.debug(
            "process: Prompt templates prepared - system_len=%d, user_len=%d",
            len(system_prompt_template),
            len(user_prompt_template),
        )

        return GenerationRequest(
            system_prompt=system_prompt_template,
            user_prompt=user_prompt_template,
            temperature=temperature,
            top_k=model_info.top_k,
            top_p=model_info.top_p,
            min_p=model_info.min_p,
        )

    @staticmethod
    def _build_system_prompt(model_info, system_prompt: Prompt) -> str:
        """Build the system prompt with a model prefix."""
        return model_info.system_prompt_prefix + system_prompt.template

    def _build_user_prompt(self, model_info, user_prompt: Prompt, processing_context: ProcessingContext) -> str:
        """Build the user prompt with parameters and model formatting."""
        user_prompt_template = self._prompt_service.apply_prompt_parameters(
            user_prompt,
            processing_context.prompt_parameters,
        )

        # Apply model-specific formatting
        formatted_prompt = "\n".join([
            model_info.user_prompt_prefix,
            user_prompt_template,
            model_info.user_prompt_suffix
        ],
        )

        return formatted_prompt

    @override
    def _execute_task(self, request: GenerationRequest) -> GenerationResponse:
        """
        Execute generation task with model service.

        Args:
            request: Generation request parameters

        Returns:
            Generation response from model service

        Raises:
            Exception: If generation fails
        """
        logger.debug("_execute_task: Starting generation request")
        logger.debug(
            "_execute_task: Request params - temp=%.2f, top_k=%d, top_p=%.2f, min_p=%.2f",
            request.temperature,
            request.top_k,
            request.top_p,
            request.min_p,
        )

        model_service = self._model_service_provider.get_model_service()
        response = model_service.generate_response(request)

        logger.debug(
            "_execute_task: Response received - content_len=%d",
            len(response.text_content),
        )
        return response
