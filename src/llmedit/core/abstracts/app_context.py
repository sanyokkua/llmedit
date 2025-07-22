from core.abstracts.providers import PromptProvider, LLMProvider, DBClientProvider, LanguageProvider, \
    TextTransformationProvider, TextTranslationProvider
from core.abstracts.services import SettingsService, TextSanitizer, PromptValidator


class AppContext:
    def __init__(self,
                 db_provider: DBClientProvider,
                 app_settings: SettingsService,
                 llm_provider: LLMProvider,
                 prompts_provider: PromptProvider,
                 translate_prompt_validator: PromptValidator,
                 text_prompt_validator: PromptValidator,
                 text_sanitizer: TextSanitizer,
                 translation_service_provider: TextTranslationProvider,
                 transformation_service_provider: TextTransformationProvider,
                 lang_provider: LanguageProvider,
                 ):
        self._db_provider = db_provider
        self._app_settings = app_settings
        self._llm_provider = llm_provider
        self._prompts_provider = prompts_provider
        self._translate_prompt_validator = translate_prompt_validator
        self._text_prompt_validator = text_prompt_validator
        self._text_sanitizer = text_sanitizer
        self._translation_service_provider = translation_service_provider
        self._transformation_service_provider = transformation_service_provider
        self._lang_provider = lang_provider

    @property
    def db_provider(self):
        return self._db_provider

    @property
    def app_settings(self):
        return self._app_settings

    @property
    def llm_provider(self):
        return self._llm_provider

    @property
    def prompts_provider(self):
        return self._prompts_provider

    @property
    def translate_prompt_validator(self):
        return self._translate_prompt_validator

    @property
    def text_prompt_validator(self):
        return self._text_prompt_validator

    @property
    def text_sanitizer(self):
        return self._text_sanitizer

    @property
    def translation_service_provider(self):
        return self._translation_service_provider

    @property
    def transformation_service_provider(self):
        return self._transformation_service_provider

    @property
    def lang_provider(self):
        return self._lang_provider
