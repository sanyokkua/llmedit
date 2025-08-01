from abc import ABC, abstractmethod

from core.models.data_types import GenerationRequest, GenerationResponse
from core.models.settings import ModelInformation


class ModelService(ABC):
    @abstractmethod
    def is_model_loaded(self) -> bool:
        pass

    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    def unload_model(self) -> None:
        pass

    @abstractmethod
    def get_model_information(self) -> ModelInformation:
        pass

    @abstractmethod
    def generate_response(self, request: GenerationRequest) -> GenerationResponse:
        pass
