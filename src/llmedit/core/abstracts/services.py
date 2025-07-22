from abc import ABC, abstractmethod
from concurrent.futures import Future

from core.abstracts.types import LLMRequest, LLMResponse, AppSettings, PromptType


class TaskExecutor(ABC):
    @abstractmethod
    def submit_task(self, operation: str, **kwargs) -> Future:
        pass

    @abstractmethod
    def cancel_task(self, task_id: str) -> None:
        pass


class TextSanitizer(ABC):
    @abstractmethod
    def sanitize_text(self, text: str) -> str:
        pass


class LLMModelClient(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse: pass


class SettingsService(ABC):
    @abstractmethod
    def get_settings(self) -> AppSettings: pass

    @abstractmethod
    def save_settings(self, settings: AppSettings) -> None: pass


class TextTranslation(ABC):
    @abstractmethod
    def translate_text(self, text: str, input_language: str, output_language: str) -> str: pass

    @abstractmethod
    def translate_text_dict(self, text: str, input_language: str, output_language: str) -> str: pass


class TextTransformation(ABC):
    @abstractmethod
    def process_text(self, text: str, prompt_type: PromptType) -> str: pass


class PromptValidator(ABC):
    @abstractmethod
    def validate_prompt(self, prompt: str) -> bool: pass


class DBClient(ABC):
    @abstractmethod
    def save_settings(self, settings: AppSettings): pass

    @abstractmethod
    def load_settings(self) -> AppSettings | None: pass
