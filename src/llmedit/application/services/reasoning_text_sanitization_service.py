import logging
import re
from typing import override

from llmedit.core.interfaces.processing.text_sanitization_service import TextSanitizationService

logger = logging.getLogger(__name__)


class ReasoningTextSanitizationService(TextSanitizationService):
    # Compile a regex pattern for better performance and readability
    REASONING_TAG_PATTERN = re.compile(r"(<think>.*?</think>)", re.DOTALL)

    @override
    def sanitize_text(self, text: str) -> str:
        """
        Remove reasoning tags and sanitize text.

        Args:
            text: Input text that may contain reasoning tags.

        Returns:
            Sanitized text with reasoning tags removed and leading/trailing whitespace stripped.

        Notes:
            Uses a compiled regex pattern to remove all occurrences of <think>...</think>,
            including multiline content. Returns empty string for empty input.
            Falls back to basic stripping if an error occurs during processing.
        """
        if not text:
            logger.debug("sanitize_text: Empty input provided")
            return ""

        logger.debug(f"sanitize_text: Input length={len(text)}")
        self._log_text_sample("Input", text)

        try:
            cleaned_text = self.REASONING_TAG_PATTERN.sub("", text)
            logger.debug(f"sanitize_text: Removed reasoning tags - new length={len(cleaned_text)}")

            result = cleaned_text.strip()
            logger.debug(f"sanitize_text: Output length={len(result)}")
            self._log_text_sample("Output", result)

            return result

        except re.error as e:
            logger.error(f"sanitize_text: Regex error during sanitization - {e}")
            return text.strip()
        except Exception as e:
            logger.error(f"sanitize_text: Unexpected error during sanitization - {e}", exc_info=True)
            return text.strip()

    @staticmethod
    def _log_text_sample(label: str, text: str) -> None:
        """
        Log a sample of text for debugging purposes.

        Args:
            label: Label to prefix the log message (e.g., "Input", "Output").
            text: The text to sample and log.

        Notes:
            Truncates text to 50 characters with ellipsis if longer.
            Used internally to provide visibility into text state during sanitization.
        """
        sample = text[:50] + "..." if len(text) > 50 else text
        logger.debug(f"sanitize_text: {label} sample='{sample}'")
