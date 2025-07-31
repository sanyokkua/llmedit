import logging
from pathlib import Path

from PyQt6.QtCore import QThreadPool

from application.services.default_supported_translation_languages_service import \
    DefaultSupportedTranslationLanguagesService
from application.services.prompt_service import AppPromptService
from application.services.text_processing_service_base import TextProcessingServiceBase
from application.services.text_sanitization_service import ReasoningTextSanitizationService
from config.in_memory_settings_service import InMemorySettingsService
from core.interfaces.background.task_service import TaskService
from core.interfaces.processing.supported_translation_languages_service import SupportedTranslationLanguagesService
from core.interfaces.processing.text_processing_service import TextProcessingService
from core.interfaces.prompt.prompt_service import PromptService
from core.interfaces.settings.settings_service import SettingsService
from infra.providers.settings_llamacpp_provider import SettingsLlamaCppProvider
from infra.providers.settings_ollama_provider import SettingsOllamaProvider
from infra.providers.standard_model_service_provider import StandardModelServiceProvider
from qt_based.task_service import TaskServiceImpl

logger = logging.getLogger(__name__)

DATA_DIR = "data"
DATA_MODELS_SUBDIR = "models"


class AppContext:
    def __init__(self, *,
                 settings_service: SettingsService,
                 prompt_service: PromptService,
                 text_processing_service: TextProcessingService,
                 supported_languages_service: SupportedTranslationLanguagesService,
                 task_service: TaskService,
                 ):
        self._settings_service = settings_service
        self._prompt_service = prompt_service
        self._text_processing_service = text_processing_service
        self._supported_languages_service = supported_languages_service
        self._task_service = task_service

    @property
    def settings_service(self) -> SettingsService:
        return self._settings_service

    @property
    def prompt_service(self) -> PromptService:
        return self._prompt_service

    @property
    def text_processing_service(self) -> TextProcessingService:
        return self._text_processing_service

    @property
    def supported_languages_service(self) -> SupportedTranslationLanguagesService:
        return self._supported_languages_service

    @property
    def task_service(self) -> TaskService:
        return self._task_service


def create_settings_service(root_path: Path) -> SettingsService:
    models_path = root_path / DATA_DIR / DATA_MODELS_SUBDIR
    models_path.mkdir(parents=True, exist_ok=True)

    ollama_settings_provider = SettingsOllamaProvider()
    llamacpp_settings_provider = SettingsLlamaCppProvider(model_folder_path=models_path)

    return InMemorySettingsService(
        ollama_provider=ollama_settings_provider,
        llama_provider=llamacpp_settings_provider
    )


def create_context(root_path: Path) -> AppContext:
    logger.debug(f"Creating context for root path: {root_path}")

    try:
        prompt_service = AppPromptService()
        text_sanitization_service = ReasoningTextSanitizationService()
        supported_languages_service = DefaultSupportedTranslationLanguagesService()
        models_path = root_path / DATA_DIR / DATA_MODELS_SUBDIR

        settings_service = create_settings_service(root_path)
        model_service_provider = StandardModelServiceProvider(
            settings_service=settings_service,
            model_folder_path=models_path
        )

        text_processing_service = TextProcessingServiceBase(
            settings_service=settings_service,
            sanitizer_service=text_sanitization_service,
            model_service_provider=model_service_provider,
            prompt_service=prompt_service,
        )

        thread_pool = QThreadPool()
        thread_pool.setMaxThreadCount(1)  # Limit to 1 thread
        task_service: TaskService = TaskServiceImpl(thread_pool=thread_pool)

        context = AppContext(
            settings_service=settings_service,
            prompt_service=prompt_service,
            text_processing_service=text_processing_service,
            supported_languages_service=supported_languages_service,
            task_service=task_service,
        )

        logger.debug("Application context created successfully")
        return context

    except Exception as e:
        logger.error(f"Failed to create application context: {e}")
        raise
