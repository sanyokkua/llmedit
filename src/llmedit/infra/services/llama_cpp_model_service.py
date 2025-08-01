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

        logger.debug(
            "__init__: Initialized for model '%s' (file: '%s')",
            self._model_information.name,
            self._model_information.fileName
        )

    def get_model_information(self) -> ModelInformation:
        """Retrieve model configuration details."""
        logger.debug(
            "get_model_information: Returning model '%s' (provider: %s)",
            self._model_information.name,
            self._model_information.provider.value
        )
        return self._model_information

    def is_model_loaded(self) -> bool:
        """Check if model is currently loaded in memory."""
        loaded = self._model is not None
        logger.debug("is_model_loaded: Model status: %s", "LOADED" if loaded else "UNLOADED")
        return loaded

    def load_model(self) -> None:
        """Load model into memory if not already loaded."""
        if self.is_model_loaded():
            logger.debug("load_model: Model already loaded - skipping reload")
            return

        model_path = self._model_folder_path / self._model_information.fileName
        logger.debug(
            "load_model: Loading model '%s' from '%s'",
            self._model_information.name,
            model_path
        )

        try:
            self._model = Llama(
                model_path=str(model_path.absolute()),
                n_ctx=0,  # Context length from model
                n_gpu_layers=-1,  # Use GPU for all layers
                n_threads=8,  # Generation threads
                use_mlock=True,  # Keep in RAM
                verbose=False  # Suppress verbose output
            )
            logger.info(
                "load_model: Successfully loaded model '%s'",
                self._model_information.name
            )
        except Exception as e:
            logger.error(
                "load_model: Failed to load model '%s'",
                self._model_information.name,
                exc_info=True
            )
            raise RuntimeError(f"Failed to load model: {str(e)}") from e

    def unload_model(self) -> None:
        """Unload model from memory if loaded."""
        if not self.is_model_loaded():
            logger.info("unload_model: No model loaded - nothing to unload")
            return

        logger.debug("unload_model: Unloading model '%s'", self._model_information.name)
        try:
            del self._model
            self._model = None
            logger.info("unload_model: Model successfully unloaded")
        except Exception as e:
            logger.warning(
                "unload_model: Failed to unload model '%s'",
                self._model_information.name,
                e,
                exc_info=True,
            )
            self._model = None

    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """Generate response using loaded model."""
        if not self.is_model_loaded():
            logger.info(
                "generate_response: Model not loaded - loading '%s'",
                self._model_information.name
            )
            self.load_model()

        # Log request parameters without sensitive data
        logger.debug(
            "generate_response: Starting generation - system_len=%d, user_len=%d, temp=%.2f, top_k=%d, top_p=%.2f, min_p=%.2f",
            len(request.system_prompt),
            len(request.user_prompt),
            request.temperature,
            request.top_k,
            request.top_p,
            request.min_p
        )

        try:
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

            generated_text = response["choices"][0]["message"]["content"].strip()
            logger.info(
                "generate_response: Generated %d characters",
                len(generated_text)
            )

            return GenerationResponse(
                text_content=generated_text,
                metadata={
                    "model_name": self._model_information.name,
                },
                original_request=request,
            )

        except Exception as e:
            logger.error(
                "generate_response: Generation failed for model '%s'",
                self._model_information.name,
                exc_info=True
            )
            raise RuntimeError(f"Failed to generate response: {str(e)}") from e
