from abc import ABC, abstractmethod


class TextSanitizationService(ABC):
    """
    Abstract base class defining the interface for text sanitization.

    Implementations are responsible for cleaning and normalizing generated text,
    such as removing unwanted content, formatting, or security-sensitive patterns.
    """

    @abstractmethod
    def sanitize_text(self, text: str) -> str:
        """
        Clean and normalize the input text.

        Args:
            text: The raw text to sanitize.

        Returns:
            Cleaned text with unwanted content removed or replaced.

        Notes:
            Implementations may remove tags, control characters, or other
            unwanted elements. Should handle empty or None input gracefully.
        """