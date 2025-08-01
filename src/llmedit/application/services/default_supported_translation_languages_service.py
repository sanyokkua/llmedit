import logging
from typing import Sequence

from core.interfaces.processing.supported_translation_languages_service import (
    SupportedTranslationLanguagesService,
)

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES: tuple[str, ...] = (
    'English',
    'German',
    'French',
    'Spanish',
    'Italian',
    'Croatian',
    'Ukrainian',
)


class DefaultSupportedTranslationLanguagesService(
    SupportedTranslationLanguagesService,
):
    """
    Default implementation of SupportedTranslationLanguagesService
    that returns a fixed set of languages.
    """

    def get_supported_translation_languages(self) -> Sequence[str]:
        """
        Return a fresh list of all supported translation languages.

        By returning a new list each time, we prevent external
        callers from mutating the module‐level tuple.
        """
        # Build a new list from the immutable tuple
        langs = list(SUPPORTED_LANGUAGES)

        # Single debug log with lazy formatting
        logger.debug("Supported translation languages → %s", langs)

        return langs
