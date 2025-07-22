from pathlib import Path
from threading import Lock

from core.abstracts.app_context import AppContext
from core.services.db.sq_lite import SQLiteProvider, SQLiteClient
from core.services.languages.language_provider import AppLanguageProvider
from core.services.llms.llm_provider import AppLlmProvider
from core.services.prompts.prompt_file_provider import PromptFileProvider
from core.services.prompts.prompt_validators import TranslationPromptValidator, TextGenericPromptValidator
from core.services.settings.settings_service import AppSettingsService
from core.services.text.providers import TextTranslationServiceProvider, TextTransformationServiceProvider
from core.services.text.text_sanitizer import ReasoningTextSanitizer


def _create_app_context(app_root_path: Path) -> AppContext:
    prompt_dir = app_root_path / "data" / "prompts"
    models_dir = app_root_path / "data" / "models"
    db_file = app_root_path / "data" / "app.db"

    db_client = SQLiteClient(db_file)
    db_provider = SQLiteProvider(db_client)
    app_settings = AppSettingsService(db_provider)
    llm_provider = AppLlmProvider(local_model_dir=models_dir, settings_service=app_settings)
    prompts_provider = PromptFileProvider(prompt_dir=prompt_dir)
    translate_prompt_validator = TranslationPromptValidator()
    text_prompt_validator = TextGenericPromptValidator()
    text_sanitizer = ReasoningTextSanitizer()
    translation_service_provider = TextTranslationServiceProvider(llm_provider=llm_provider,
                                                                  prompt_provider=prompts_provider,
                                                                  prompt_validator=translate_prompt_validator,
                                                                  text_sanitizer=text_sanitizer,
                                                                  )
    transformation_service_provider = TextTransformationServiceProvider(llm_provider=llm_provider,
                                                                        prompt_provider=prompts_provider,
                                                                        prompt_validator=text_prompt_validator,
                                                                        text_sanitizer=text_sanitizer,
                                                                        )
    lang_provider = AppLanguageProvider()
    return AppContext(
        db_provider=db_provider,
        app_settings=app_settings,
        llm_provider=llm_provider,
        prompts_provider=prompts_provider,
        translate_prompt_validator=translate_prompt_validator,
        text_prompt_validator=text_prompt_validator,
        text_sanitizer=text_sanitizer,
        translation_service_provider=translation_service_provider,
        transformation_service_provider=transformation_service_provider,
        lang_provider=lang_provider,
    )


_context_lock = Lock()
context: AppContext | None = None


def get_app_context(app_root_path: Path) -> AppContext:
    global context
    with _context_lock:  # Ensure only one thread initializes
        if context is None:
            context = _create_app_context(app_root_path)
    return context
