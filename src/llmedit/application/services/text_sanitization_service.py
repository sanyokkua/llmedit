import logging
import re

from core.interfaces.processing.text_sanitization_service import TextSanitizationService

logger = logging.getLogger(__name__)


class ReasoningTextSanitizationService(TextSanitizationService):
    def sanitize_text(self, text: str) -> str:
        """Remove reasoning tags and sanitize text."""
        logger.debug("sanitize_text: Input length=%d", len(text))
        if len(text) > 50:
            logger.debug("sanitize_text: Input sample='%s...'", text[:50])
        else:
            logger.debug("sanitize_text: Input sample='%s'", text)

        # Remove <think>...</think> (non-greedy, across lines)
        cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        logger.debug("sanitize_text: Removed reasoning tags - new length=%d", len(cleaned))

        # Strip leading/trailing whitespace
        result = cleaned.strip()
        logger.debug("sanitize_text: Output length=%d", len(result))
        if len(result) > 50:
            logger.debug("sanitize_text: Output sample='%s...'", result[:50])
        else:
            logger.debug("sanitize_text: Output sample='%s'", result)

        return result
