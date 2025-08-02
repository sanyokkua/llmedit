from abc import ABC, abstractmethod

from llmedit.core.interfaces.llm_model.model_service import ModelService
from llmedit.core.interfaces.settings.settings_service import SettingsService


class ModelServiceProvider(ABC):
    """
    Abstract base class for providing model services based on current settings.

    Manages the lifecycle and selection of ModelService instances according to the active
    LLM provider and model configuration. Ensures the correct model backend is used.
    """

    def __init__(self, settings_service: SettingsService):
        """
        Initialize the provider with access to application settings.

        Args:
            settings_service: Service providing current LLM configuration including provider and model.
        """
        self._settings_service = settings_service

    @abstractmethod
    def get_model_service(self) -> ModelService:
        """
        Retrieve the appropriate model service instance based on current settings.

        Returns:
            ModelService implementation configured for the currently selected LLM provider.

        Notes:
            The returned service may be newly created or reused from a pool, depending on implementation.
            Must reflect the current provider setting from SettingsService.
        """
