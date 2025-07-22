from abc import ABC, abstractmethod
from typing import List

from core.abstracts.services import LLMModelClient, DBClient, TextTranslation, TextTransformation
from core.abstracts.types import PromptType


class LLMModelClientProvider(ABC):
    @abstractmethod
    def get_model_client(self, ) -> LLMModelClient:
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        pass

    @abstractmethod
    def load_model(self, model_name: str) -> None:
        pass

    @abstractmethod
    def unload_model(self) -> None:
        pass


# ollama, openai, llamacpp, etc
class LLMProvider(ABC):
    @abstractmethod
    def get_llm_provider(self) -> LLMModelClientProvider:
        pass

    @abstractmethod
    def get_available_providers(self) -> List[str]:
        pass


class PromptProvider(ABC):
    @abstractmethod
    def get_prompt(self, prompt_type: PromptType) -> str:
        pass


class LanguageProvider(ABC):
    @abstractmethod
    def get_supported_languages(self) -> list[str]:
        pass


class DBClientProvider(ABC):
    @abstractmethod
    def get_client(self) -> DBClient:
        pass


class TextTranslationProvider(ABC):
    @abstractmethod
    def get_translation_service(self) -> TextTranslation:
        pass


class TextTransformationProvider(ABC):
    @abstractmethod
    def get_text_transformation_service(self, ) -> TextTransformation:
        pass
