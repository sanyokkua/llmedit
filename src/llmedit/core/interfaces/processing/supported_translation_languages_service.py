from abc import ABC, abstractmethod


class SupportedTranslationLanguagesService(ABC):
    @abstractmethod
    def get_supported_translation_languages(self) -> list[str]: pass
