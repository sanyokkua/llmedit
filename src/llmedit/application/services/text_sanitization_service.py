import logging
import re
from typing import override

from core.interfaces.processing.text_sanitization_service import TextSanitizationService

logger = logging.getLogger(__name__)


class ReasoningTextSanitizationService(TextSanitizationService):
    # Compile a regex pattern for better performance and readability
    REASONING_TAG_PATTERN = re.compile(r"<think>.*?</think>", re.DOTALL)

    @override
    def sanitize_text(self, text: str) -> str:
        """
        Remove reasoning tags and sanitize text.

        Args:
            text: Input text that may contain reasoning tags

        Returns:
            Sanitized text with reasoning tags removed and whitespace stripped
        """
        # Guard clause for empty input
        if not text:
            logger.debug("sanitize_text: Empty input provided")
            return ""

        logger.debug(f"sanitize_text: Input length={len(text)}")
        self._log_text_sample("Input", text)

        try:
            # Remove <think>...</think> tags (non-greedy, across lines)
            cleaned_text = self.REASONING_TAG_PATTERN.sub("", text)
            logger.debug(f"sanitize_text: Removed reasoning tags - new length={len(cleaned_text)}")

            # Strip leading/trailing whitespace
            result = cleaned_text.strip()
            logger.debug(f"sanitize_text: Output length={len(result)}")
            self._log_text_sample("Output", result)

            return result

        except re.error as e:
            logger.error(f"sanitize_text: Regex error during sanitization - {e}")
            return text.strip()  # Fallback to basic sanitization
        except Exception as e:
            logger.error(f"sanitize_text: Unexpected error during sanitization - {e}", exc_info=True)
            return text.strip()  # Fallback to basic sanitization

    @staticmethod
    def _log_text_sample(label: str, text: str) -> None:
        """
        Log a sample of text for debugging purposes.

        Args:
            label: Label for the log message
            text: Text to log sample of
        """
        sample = text[:50] + "..." if len(text) > 50 else text
        logger.debug(f"sanitize_text: {label} sample='{sample}'")
