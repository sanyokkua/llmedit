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


class DefaultSupportedTranslationLanguagesService(SupportedTranslationLanguagesService):
    """
    Default implementation of SupportedTranslationLanguagesService that returns a fixed set of supported languages.

    This service provides a static list of translation languages. A new list instance is returned on each call
    to prevent external modification of the internal immutable tuple.
    """

    def get_supported_translation_languages(self) -> Sequence[str]:
        """
        Return a fresh list of all supported translation languages.

        Returns:
            Sequence[str]: A new list containing the names of all supported translation languages.
                The list is built from a module-level immutable tuple to ensure consistency and thread safety.

        Notes:
            The returned list is a copy to prevent external callers from mutating the internal state.
            Debug-level logging is performed with the list contents.
        """
        langs = list(SUPPORTED_LANGUAGES)
        logger.debug("Supported translation languages → %s", langs)
        return langs
