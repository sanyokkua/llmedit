from abc import ABC, abstractmethod

from core.interfaces.llm_model.model_service import ModelService
from core.interfaces.settings.settings_service import SettingsService


class ModelServiceProvider(ABC):
    def __init__(self, settings_service: SettingsService):
        self._settings_service = settings_service

    @abstractmethod
    def get_model_service(self) -> ModelService: pass
