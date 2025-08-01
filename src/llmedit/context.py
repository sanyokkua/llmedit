import logging
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal

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


class AppContext(QObject):
    """
    Central application context providing access to all core services.

    Serves as a dependency container and event hub for the application.
    Manages service instances and propagates settings update notifications.
    """

    settings_updated_signal = pyqtSignal()

    def __init__(self, *,
                 settings_service: SettingsService,
                 prompt_service: PromptService,
                 text_processing_service: TextProcessingService,
                 supported_languages_service: SupportedTranslationLanguagesService,
                 task_service: TaskService,
                 ):
        """
        Initialize the application context with required services.

        Args:
            settings_service: Service for managing application settings.
            prompt_service: Service for retrieving and processing prompts.
            text_processing_service: Service for generating and processing text.
            supported_languages_service: Service providing available translation languages.
            task_service: Service for managing background task execution.

        Notes:
            Stores references to all core services for easy access by UI components.
        """
        super().__init__()

        logger.debug(
            "__init__: Initializing application context with %s settings service",
            type(settings_service).__name__,
        )

        self._settings_service = settings_service
        self._prompt_service = prompt_service
        self._text_processing_service = text_processing_service
        self._supported_languages_service = supported_languages_service
        self._task_service = task_service

    @property
    def settings_service(self) -> SettingsService:
        """
        Get the settings service instance.

        Returns:
            The configured SettingsService for accessing and modifying settings.
        """
        logger.debug("settings_service: Accessing settings service")
        return self._settings_service

    @property
    def prompt_service(self) -> PromptService:
        """
        Get the prompt service instance.

        Returns:
            The configured PromptService for retrieving and parameterizing prompts.
        """
        logger.debug("prompt_service: Accessing prompt service")
        return self._prompt_service

    @property
    def text_processing_service(self) -> TextProcessingService:
        """
        Get the text processing service instance.

        Returns:
            The configured TextProcessingService for generating and sanitizing text.
        """
        logger.debug("text_processing_service: Accessing text processing service")
        return self._text_processing_service

    @property
    def supported_languages_service(self) -> SupportedTranslationLanguagesService:
        """
        Get the supported languages service instance.

        Returns:
            The configured service providing available translation languages.
        """
        logger.debug("supported_languages_service: Accessing languages service")
        return self._supported_languages_service

    @property
    def task_service(self) -> TaskService:
        """
        Get the task service instance.

        Returns:
            The configured TaskService for managing background operations.
        """
        logger.debug("task_service: Accessing task service")
        return self._task_service

    def subscribe_settings_updated(self, listener: Callable[[], None]):
        """
        Subscribe to settings update events.

        Args:
            listener: Function to call when settings are updated.

        Notes:
            Multiple listeners can be registered. The signal is emitted after
            any setting change is applied.
        """
        logger.debug(
            "subscribe_settings_updated: New listener registered (%s)",
            getattr(listener, '__qualname__', str(listener)),
        )
        self.settings_updated_signal.connect(listener)

    def emit_settings_updated(self):
        """
        Notify all subscribers that settings have been updated.

        Notes:
            Called by components that modify settings to trigger UI updates
            and service reconfiguration.
        """
        logger.debug("emit_settings_updated: Emitting settings updated signal")
        self.settings_updated_signal.emit()

    def is_system_ready(self) -> bool:
        """
        Check if the system is ready for operations.

        Returns:
            True if a valid model is selected, False otherwise.

        Notes:
            Considers the system ready only when a non-empty model ID is selected.
        """
        model = self.settings_service.get_llm_model()
        is_ready = model is not None and model.id is not None and len(model.id.strip()) > 0

        logger.debug(
            "is_system_ready: System readiness status: %s",
            "READY" if is_ready else "NOT READY",
        )
        return is_ready


def create_settings_service(root_path: Path) -> SettingsService:
    """
    Create and configure the settings service with model providers.

    Args:
        root_path: Base directory for application data.

    Returns:
        Configured SettingsService instance.

    Raises:
        Exception: If models directory creation fails.

    Notes:
            Creates directory structure for models and initializes both Ollama
            and llama.cpp providers.
    """
    logger.debug(
        "create_settings_service: Creating settings service for root path '%s'",
        root_path,
    )

    models_path = root_path / DATA_DIR / DATA_MODELS_SUBDIR
    logger.debug(
        "create_settings_service: Models will be stored at '%s'",
        models_path,
    )

    try:
        models_path.mkdir(parents=True, exist_ok=True)
        logger.debug(
            "create_settings_service: Models directory created (exists=%s)",
            models_path.exists(),
        )
    except Exception as e:
        logger.error(
            "create_settings_service: Failed to create models directory: %s",
            str(e),
            exc_info=True,
        )
        raise

    ollama_settings_provider = SettingsOllamaProvider()
    llamacpp_settings_provider = SettingsLlamaCppProvider(model_folder_path=models_path)

    logger.debug(
        "create_settings_service: Settings providers initialized (%s, %s)",
        type(ollama_settings_provider).__name__,
        type(llamacpp_settings_provider).__name__,
    )

    settings_service = InMemorySettingsService(
        ollama_provider=ollama_settings_provider,
        llama_provider=llamacpp_settings_provider,
    )

    logger.debug(
        "create_settings_service: Settings service created with provider count: %d",
        len(settings_service.get_llm_provider_list()),
    )
    return settings_service


def create_context(root_path: Path) -> AppContext:
    """
    Create and configure the complete application context.

    Args:
        root_path: Base directory for application data.

    Returns:
        Fully configured AppContext with all services wired together.

    Raises:
        Exception: If context creation fails at any stage.

    Notes:
            Sets up the dependency graph: services depend on each other in a
            specific order, with the AppContext as the central coordinator.
    """
    logger.debug(
        "create_context: Creating application context for root path '%s'",
        root_path,
    )

    try:
        prompt_service = AppPromptService()
        logger.debug(
            "create_context: Prompt service initialized (%s)",
            type(prompt_service).__name__,
        )

        text_sanitization_service = ReasoningTextSanitizationService()
        logger.debug(
            "create_context: Text sanitization service initialized (%s)",
            type(text_sanitization_service).__name__,
        )

        supported_languages_service = DefaultSupportedTranslationLanguagesService()
        logger.debug(
            "create_context: Languages service initialized with %d supported languages",
            len(supported_languages_service.get_supported_translation_languages()),
        )

        models_path = root_path / DATA_DIR / DATA_MODELS_SUBDIR
        logger.debug(
            "create_context: Using models path '%s'",
            models_path,
        )

        settings_service = create_settings_service(root_path)
        logger.debug(
            "create_context: Settings service created with provider: %s",
            settings_service.get_llm_provider().value,
        )

        model_service_provider = StandardModelServiceProvider(
            settings_service=settings_service,
            model_folder_path=models_path,
        )
        logger.debug(
            "create_context: Model service provider initialized (%s)",
            type(model_service_provider).__name__,
        )

        text_processing_service = TextProcessingServiceBase(
            settings_service=settings_service,
            sanitizer_service=text_sanitization_service,
            model_service_provider=model_service_provider,
            prompt_service=prompt_service,
        )
        logger.debug(
            "create_context: Text processing service initialized (%s)",
            type(text_processing_service).__name__,
        )

        thread_pool = QThreadPool()
        thread_pool.setMaxThreadCount(1)
        task_service: TaskService = TaskServiceImpl(thread_pool=thread_pool)
        logger.debug(
            "create_context: Task service initialized with max threads=%d",
            thread_pool.maxThreadCount(),
        )

        context = AppContext(
            settings_service=settings_service,
            prompt_service=prompt_service,
            text_processing_service=text_processing_service,
            supported_languages_service=supported_languages_service,
            task_service=task_service,
        )

        logger.info(
            "create_context: Application context created successfully with %d services",
            5,
        )
        return context

    except Exception as e:
        logger.error(
            "create_context: Failed to create application context: %s",
            str(e),
            exc_info=True,
        )
        raise
