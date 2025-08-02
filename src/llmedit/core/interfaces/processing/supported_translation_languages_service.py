from abc import ABC, abstractmethod


class SupportedTranslationLanguagesService(ABC):
    """
    Abstract base class defining the interface for retrieving supported translation languages.

    Implementations provide a list of language names that can be used as targets in translation workflows.
    """

    @abstractmethod
    def get_supported_translation_languages(self) -> list[str]:
        """
        Retrieve the list of supported translation languages.

        Returns:
            A list of language names as strings (e.g., 'English', 'German').

        Notes:
            The returned list should contain human-readable language names.
            The order may be significant depending on the implementation.
        """
