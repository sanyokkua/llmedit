import logging

from core.interfaces.processing.supported_translation_languages_service import SupportedTranslationLanguagesService

logger = logging.getLogger(__name__)


class DefaultSupportedTranslationLanguagesService(SupportedTranslationLanguagesService):
    def get_supported_translation_languages(self) -> list[str]:
        """Retrieve the list of supported translation languages."""
        logger.debug("Get supported translation languages: entering method")

        languages = ['English', 'German', 'French', 'Spanish', 'Italian', 'Croatian', 'Ukrainian']

        logger.debug(
            "Get supported translation languages: returning %d languages - %s",
            len(languages),
            ", ".join(languages)
        )
        return languages
