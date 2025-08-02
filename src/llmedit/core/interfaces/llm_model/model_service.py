from abc import ABC, abstractmethod

from llmedit.core.models.data_types import GenerationRequest, GenerationResponse
from llmedit.core.models.settings import ModelInformation


class ModelService(ABC):
    """
    Abstract base class defining the interface for language model management and text generation.

    Implementations handle model loading, unloading, and response generation. Provides access
    to model configuration and supports synchronous generation requests.
    """

    @abstractmethod
    def is_model_loaded(self) -> bool:
        """
        Check if a model is currently loaded and ready for inference.

        Returns:
            True if a model is loaded and available for generation, False otherwise.
        """

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the configured language model into memory.

        Raises:
            Exception: If model loading fails due to file not found, hardware constraints, or other errors.

        Notes:
            This method blocks until loading is complete or fails.
        """

    @abstractmethod
    def unload_model(self) -> None:
        """
        Unload the currently loaded model to free system resources.

        Notes:
            Safe to call even if no model is loaded. Should release all GPU/CPU memory associated with the model.
        """

    @abstractmethod
    def get_model_information(self) -> ModelInformation:
        """
        Retrieve metadata about the current model configuration.

        Returns:
            ModelInformation object containing model name, parameters, and generation settings.

        Notes:
            Returns configuration even if model is not currently loaded.
        """

    @abstractmethod
    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        """
        Generate a response using the loaded model based on the provided request.

        Args:
            request: Contains system prompt, user prompt, and generation parameters.

        Returns:
            GenerationResponse with the generated text content.

        Raises:
            Exception: If generation fails due to model errors, timeouts, or invalid input.

        Notes:
            This method blocks until generation is complete or an error occurs.
        """
