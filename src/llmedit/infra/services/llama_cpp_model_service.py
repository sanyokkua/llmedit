import logging
from pathlib import Path
from typing import Optional

from llama_cpp import Llama, ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, \
    ChatCompletionRequestUserMessage

from core.interfaces.llm_model.model_service import ModelService
from core.models.data_types import GenerationRequest, GenerationResponse
from core.models.settings import ModelInformation

logger = logging.getLogger(__name__)


class LlamaCppModelService(ModelService):
    def __init__(self, model_folder_path: Path, model_information: ModelInformation) -> None:
        self._model_folder_path = model_folder_path
        self._model_information = model_information
        self._model: Optional[Llama] = None
        logger.debug(f"Model folder path: {self._model_folder_path}")
        logger.debug(f"Model information: {self._model_information}")

    def get_model_information(self) -> ModelInformation:
        return self._model_information

    def is_model_loaded(self) -> bool:
        logger.debug(f"Model loaded: {self._model is not None}")
        return self._model is not None

    def load_model(self) -> None:
        if self.is_model_loaded():
            logger.debug("Model already loaded")
            return
        try:
            model_path: Path = self._model_folder_path / self._model_information.fileName
            logger.debug(f"Loading model from path: {model_path}")
            self._model = Llama(
                model_path=str(model_path.absolute()),
                n_ctx=0,  # text context, 0 = from a model
                n_gpu_layers=-1,  # Load all layers to GPU
                n_threads=8,  # Number of threads to use for generation
                use_mlock=True,  # Force the system to keep the model in RAM.
                verbose=False  # Print verbose output to stderr.
            )
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to load model: {str(e)}") from e

    def unload_model(self) -> None:
        if not self.is_model_loaded():
            logger.info("No model to unload")
            return
        try:
            del self._model
            self._model = None
            logger.info("Model unloaded successfully")
        except Exception as e:
            logger.warning(f"Failed to unload model: {str(e)}", exc_info=True)
            self._model = None

    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        if not self.is_model_loaded():
            self.load_model()

        try:
            logger.debug(f"Generating response for request: {request}")

            messages: list[ChatCompletionRequestMessage] = [
                ChatCompletionRequestSystemMessage(role="system", content=request.system_prompt),
                ChatCompletionRequestUserMessage(role="user", content=request.user_prompt),
            ]
            response = self._model.create_chat_completion(
                messages=messages,
                temperature=request.temperature,
                top_k=request.top_k,
                top_p=request.top_p,
                min_p=request.min_p,
            )
            logger.debug(f"Response: {response}")
            generated_text = response["choices"][0]["message"]["content"].strip()

            logger.info(f"Generated {len(generated_text)} characters")

            return GenerationResponse(
                text_content=generated_text,
                metadata={
                    "prompt_tokens": response["usage"]["prompt_tokens"],
                    "completion_tokens": response["usage"]["completion_tokens"],
                    "total_tokens": response["usage"]["total_tokens"],
                    "model_name": self._model_information.name,
                },
                original_request=request,
            )

        except Exception as e:
            error_msg = f"Failed to generate response: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg) from e
