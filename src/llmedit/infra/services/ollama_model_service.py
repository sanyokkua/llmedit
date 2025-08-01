import logging
from typing import override

import ollama

from core.interfaces.llm_model.model_service import ModelService
from core.models.data_types import GenerationRequest, GenerationResponse
from core.models.settings import ModelInformation

logger = logging.getLogger(__name__)


class OllamaModelService(ModelService):
    """
    Implementation of ModelService for Ollama backend.

    Delegates model management and text generation to the Ollama service.
    Models are not loaded/unloaded directly as they are managed externally by Ollama.
    """

    def __init__(self, model_information: ModelInformation) -> None:
        """
        Initialize service with model configuration.

        Args:
            model_information: Configuration object containing model name and settings.

        Notes:
            The model name must match a model known to the Ollama service.
            No local model files are managed by this class.
        """
        self._model_information = model_information
        logger.debug(
            "__init__: Initialized for Ollama model '%s'",
            self._model_information.name,
        )

    @override
    def get_model_information(self) -> ModelInformation:
        """
        Retrieve model configuration details.

        Returns:
            ModelInformation object containing the model's metadata and settings.

        Notes:
            Returns the configuration provided at initialization.
        """
        logger.debug(
            "get_model_information: Returning model '%s'",
            self._model_information.name,
        )
        return self._model_information

    @override
    def is_model_loaded(self) -> bool:
        """
        Check if model is available in Ollama.

        Returns:
            True if the model is present in Ollama's model list, False otherwise.

        Notes:
            Queries Ollama API to get list of available models and checks membership.
            Returns False if connection to Ollama fails.
        """
        logger.debug(
            "is_model_loaded: Checking availability of model '%s'",
            self._model_information.name,
        )

        try:
            response = ollama.list()
            model_names = [model["model"] for model in response["models"]]
            is_available = self._model_information.name in model_names

            logger.debug(
                "is_model_loaded: Model '%s' availability: %s (found in %d models)",
                self._model_information.name,
                "AVAILABLE" if is_available else "NOT AVAILABLE",
                len(model_names),
            )
            return is_available

        except Exception as e:
            logger.warning(
                "is_model_loaded: Failed to check model availability",
                exc_info=True,
            )
            return False

    @override
    def load_model(self) -> None:
        """
        No-op for Ollama (models managed externally).

        Notes:
            Model loading is handled by the Ollama service.
            This method exists to satisfy the ModelService interface but does nothing.
        """
        logger.debug(
            "load_model: No-op for Ollama (model loading handled externally)",
        )

    @override
    def unload_model(self) -> None:
        """
        No-op for Ollama (models managed externally).

        Notes:
            Model unloading is handled by the Ollama service.
            This method exists to satisfy the ModelService interface but does nothing.
        """
        logger.debug(
            "unload_model: No-op for Ollama (model unloading handled externally)",
        )

    @override
    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """
        Generate response using Ollama API.

        Args:
            request: Contains system prompt, user prompt, and generation parameters.

        Returns:
            GenerationResponse with the generated text content and metadata.

        Raises:
            RuntimeError: If generation fails due to connection issues or invalid input.

        Notes:
            Uses ollama.chat() to generate responses with the specified model.
            Strips whitespace from the generated response.
        """
        logger.debug(
            "generate_response: Starting generation for model '%s' - system_len=%d, user_len=%d, temp=%.2f",
            self._model_information.name,
            len(request.system_prompt),
            len(request.user_prompt),
            request.temperature,
        )

        try:
            messages = [
                { "role": "system", "content": request.system_prompt },
                { "role": "user", "content": request.user_prompt }
            ]

            response = ollama.chat(
                model=self._model_information.name,
                messages=messages,
                options={ "temperature": request.temperature },
            )

            generated_text = response["message"]["content"].strip()
            char_count = len(generated_text)

            logger.info(
                "generate_response: Generated %d characters for model '%s'",
                char_count,
                self._model_information.name,
            )

            return GenerationResponse(
                text_content=generated_text,
                metadata={
                    "model_name": self._model_information.name,
                    "character_count": char_count
                },
                original_request=request,
            )

        except Exception as e:
            logger.error(
                "generate_response: Generation failed for model '%s'",
                self._model_information.name,
                exc_info=True,
            )
            raise RuntimeError(f"Failed to generate response: {str(e)}") from e
