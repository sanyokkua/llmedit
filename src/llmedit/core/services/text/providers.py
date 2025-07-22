from core.abstracts.providers import TextTranslationProvider, TextTransformationProvider, LLMProvider, PromptProvider
from core.abstracts.services import TextTranslation, TextTransformation, TextSanitizer, PromptValidator
from core.services.text.transformation_service import TransformationService
from core.services.text.translation_service import TranslationService


class TextTranslationServiceProvider(TextTranslationProvider):
    def __init__(self,
                 llm_provider: LLMProvider,
                 prompt_provider: PromptProvider,
                 prompt_validator: PromptValidator,
                 text_sanitizer: TextSanitizer,
                 ):
        self.llm_provider = llm_provider
        self.prompt_provider = prompt_provider
        self.sanitizer = text_sanitizer
        self.prompt_validator = prompt_validator

    def get_translation_service(self) -> TextTranslation:
        provider = self.llm_provider.get_llm_provider()

        return TranslationService(
            llm_model_client=provider.get_model_client(),
            prompt_provider=self.prompt_provider,
            text_sanitizer=self.sanitizer,
            prompt_validator=self.prompt_validator,
        )


class TextTransformationServiceProvider(TextTransformationProvider):
    def __init__(self,
                 llm_provider: LLMProvider,
                 prompt_provider: PromptProvider,
                 prompt_validator: PromptValidator,
                 text_sanitizer: TextSanitizer,
                 ):
        self.llm_provider = llm_provider
        self.prompt_provider = prompt_provider
        self.sanitizer = text_sanitizer
        self.prompt_validator = prompt_validator

    def get_text_transformation_service(self) -> TextTransformation:
        provider = self.llm_provider.get_llm_provider()

        return TransformationService(
            llm_model_client=provider.get_model_client(),
            prompt_provider=self.prompt_provider,
            text_sanitizer=self.sanitizer,
            prompt_validator=self.prompt_validator,
        )
