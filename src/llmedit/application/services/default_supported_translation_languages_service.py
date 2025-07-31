from core.interfaces.processing.supported_translation_languages_service import SupportedTranslationLanguagesService


class DefaultSupportedTranslationLanguagesService(SupportedTranslationLanguagesService):

    def get_supported_translation_languages(self) -> list[str]:
        return ['English', 'German', 'French', 'Spanish', 'Italian', 'Croatian', 'Ukrainian']
