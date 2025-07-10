from abc import ABC, abstractmethod

from src.llm_inference.client import ILLMClient


class ILLMProvider(ABC):

    @abstractmethod
    def get_available_models(self) -> list[str]:
        pass

    @abstractmethod
    def load_model(self, model_name: str):
        pass

    @abstractmethod
    def get_loaded_model(self) -> str:
        pass

    @abstractmethod
    def get_client(self) -> ILLMClient:
        pass


class ILanguageProvider(ABC):

    @abstractmethod
    def get_supported_languages(self) -> list[str]:
        pass


class IPromptProvider(ABC):

    @abstractmethod
    def get_translation_prompt(self, source_language: str, target_language: str) -> str:
        pass

    @abstractmethod
    def get_proofread_prompt(self) -> str: pass

    @abstractmethod
    def get_rewrite_prompt(self) -> str: pass

    @abstractmethod
    def get_regenerate_prompt(self) -> str: pass

    @abstractmethod
    def get_formal_prompt(self) -> str: pass

    @abstractmethod
    def get_casual_prompt(self) -> str: pass

    @abstractmethod
    def get_friendly_prompt(self) -> str: pass

    @abstractmethod
    def get_email_prompt(self) -> str: pass

    @abstractmethod
    def get_chat_prompt(self) -> str: pass

    @abstractmethod
    def get_document_prompt(self) -> str: pass

    @abstractmethod
    def get_social_media_post_prompt(self) -> str: pass

    @abstractmethod
    def get_articles_prompt(self) -> str: pass

    @abstractmethod
    def get_documentation_prompt(self) -> str: pass


class OperationOptions:
    def __init__(self, content: str, model_name: str, temperature: float) -> None:
        self.content: str = content
        self.model: str = model_name
        self.temperature: float = temperature


class ITextTools(ABC):
    @abstractmethod
    def translate_text(self, source_language: str, target_language: str, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_proofread(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_rewrite(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_regenerate(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_formal(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_casual(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_friendly(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_email(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_chat(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_document(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_social_media_post(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_articles(self, oper_ops: OperationOptions) -> str: pass

    @abstractmethod
    def make_documentation(self, oper_ops: OperationOptions) -> str: pass


class ITextSanitizer(ABC):
    @abstractmethod
    def sanitize_text(self, text: str) -> str: pass
