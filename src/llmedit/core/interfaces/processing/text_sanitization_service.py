from abc import ABC, abstractmethod


class TextSanitizationService(ABC):
    @abstractmethod
    def sanitize_text(self, text: str) -> str: pass
