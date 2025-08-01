import logging

import ollama

from core.interfaces.llm_model.model_service import ModelService
from core.models.data_types import GenerationRequest, GenerationResponse
from core.models.settings import ModelInformation

logger = logging.getLogger(__name__)


class OllamaModelService(ModelService):
    def __init__(self, model_information: ModelInformation) -> None:
        self._model_information = model_information
        logger.debug(
            "__init__: Initialized for Ollama model '%s'",
            self._model_information.name
        )

    def get_model_information(self) -> ModelInformation:
        """Retrieve model configuration details."""
        logger.debug(
            "get_model_information: Returning model '%s'",
            self._model_information.name
        )
        return self._model_information

    def is_model_loaded(self) -> bool:
        """Check if model is available in Ollama."""
        logger.debug(
            "is_model_loaded: Checking availability of model '%s'",
            self._model_information.name
        )

        try:
            response = ollama.list()
            model_names = [model["model"] for model in response["models"]]
            is_available = self._model_information.name in model_names

            logger.debug(
                "is_model_loaded: Model '%s' availability: %s (found in %d models)",
                self._model_information.name,
                "AVAILABLE" if is_available else "NOT AVAILABLE",
                len(model_names)
            )
            return is_available

        except Exception as e:
            logger.warning(
                "is_model_loaded: Failed to check model availability",
                e,
                exc_info=True
            )
            return False

    def load_model(self) -> None:
        """No-op for Ollama (models managed externally)."""
        logger.debug(
            "load_model: No-op for Ollama (model loading handled externally)"
        )

    def unload_model(self) -> None:
        """No-op for Ollama (models managed externally)."""
        logger.debug(
            "unload_model: No-op for Ollama (model unloading handled externally)"
        )

    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """Generate response using Ollama API."""
        logger.debug(
            "generate_response: Starting generation for model '%s' - system_len=%d, user_len=%d, temp=%.2f",
            self._model_information.name,
            len(request.system_prompt),
            len(request.user_prompt),
            request.temperature
        )

        try:
            messages = [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt}
            ]

            # Generate response using Ollama
            response = ollama.chat(
                model=self._model_information.name,
                messages=messages,
                options={"temperature": request.temperature}
            )

            generated_text = response["message"]["content"].strip()
            char_count = len(generated_text)

            logger.info(
                "generate_response: Generated %d characters for model '%s'",
                char_count,
                self._model_information.name
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
                e,
                exc_info=True
            )
            raise RuntimeError(f"Failed to generate response: {str(e)}") from e
