import logging

import ollama

from core.interfaces.llm_model.model_service import ModelService
from core.models.data_types import GenerationRequest, GenerationResponse
from core.models.settings import ModelInformation

logger = logging.getLogger(__name__)


class OllamaModelService(ModelService):
    def __init__(self, model_information: ModelInformation) -> None:
        self._model_information = model_information
        logger.debug(f"Model information: {self._model_information}")

    def get_model_information(self) -> ModelInformation:
        return self._model_information

    def is_model_loaded(self) -> bool:
        response = ollama.list()
        model_names = [model["model"] for model in response["models"]]
        is_available = self._model_information.name in model_names
        logger.debug(f"Model available: {self._model_information.name} = {is_available}")
        return is_available

    def load_model(self) -> None:
        logger.debug(f"Loading model: {self._model_information.name}")
        # NA for Ollama

    def unload_model(self) -> None:
        logger.debug(f"Unloading model: {self._model_information.name}")
        # NA for Ollama

    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        try:
            logger.debug(f"Generating response for request: {request}")

            messages = [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_prompt}
            ]

            # Generate response using Ollama
            response = ollama.chat(
                model=self._model_information.name,
                messages=messages,
                options={
                    "temperature": request.temperature,
                }
            )

            # Extract the generated text
            generated_text = response["message"]["content"].strip()

            logger.info(f"Generated {len(generated_text)} characters")

            return GenerationResponse(
                text_content=generated_text,
                metadata={
                    "model_name": self._model_information.name,
                },
                original_request=request,
            )

        except Exception as e:
            error_msg = f"Failed to generate response: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e
