import logging

from config.prompts_objects import ID_PROMPT_SYSTEM
from core.interfaces.processing.text_processing_service import TextProcessingService
from core.models.data_types import ProcessingContext, GenerationRequest, GenerationResponse

logger = logging.getLogger(__name__)


class TextProcessingServiceBase(TextProcessingService):

    def process(self, processing_context: ProcessingContext) -> str:
        logger.debug(f"Processing context: {processing_context}")
        is_temperature_enabled = self._settings_service.get_llm_temperature_enabled()
        settings_temp = self._settings_service.get_llm_temperature()
        model_service = self._model_service_provider.get_model_service()
        model_info = model_service.get_model_information()

        temp: float = settings_temp if is_temperature_enabled else model_info.temperature
        top_k: int = model_info.top_k
        top_p: float = model_info.top_p
        min_p: float = model_info.min_p

        if not model_service.is_model_loaded():
            logger.debug("Model not loaded, loading model")
            try:
                model_service.load_model()
            except Exception as e:
                logger.warning(f"Failed to load model: {str(e)}", exc_info=True)
                return ''

        system_prompt = self._prompt_service.get_prompt(ID_PROMPT_SYSTEM)
        logger.debug(f"System prompt: {system_prompt}")

        user_prompt = self._prompt_service.get_prompt(processing_context.user_prompt_id)
        logger.debug(f"User prompt: {user_prompt}")

        is_valid_params, err = self._prompt_service.validate_prompt_parameters(user_prompt,
                                                                               processing_context.prompt_parameters)
        if not is_valid_params:
            logger.warning(f"Invalid prompt parameters: {err}. Returning empty response.")
            return ''

        system_prompt_template = model_info.system_prompt_prefix + system_prompt.template
        user_prompt_template = self._prompt_service.apply_prompt_parameters(user_prompt,
                                                                            processing_context.prompt_parameters)
        user_prompt_template = f"{model_info.user_prompt_prefix}\n{user_prompt_template}\n{model_info.user_prompt_suffix}"
        logger.debug(f"User prompt template: {user_prompt_template}")

        request = GenerationRequest(
            system_prompt=system_prompt_template,
            user_prompt=user_prompt_template,
            temperature=temp,
            top_k=top_k,
            top_p=top_p,
            min_p=min_p,
        )

        try:
            generated = self._execute_task(request)
        except Exception as e:
            logger.error(f"Failed to create generation request: {str(e)}", exc_info=True)
            return ''

        sanitized_text = self._sanitizer_service.sanitize_text(generated.text_content)
        logger.debug(f"Sanitized text: {sanitized_text}")
        return sanitized_text

    def _execute_task(self, request: GenerationRequest) -> GenerationResponse:
        logger.debug(f"Executing task with request: {request}")
        model_service = self._model_service_provider.get_model_service()
        response = model_service.generate_response(request)
        logger.debug(f"Response: {response}")
        return response
