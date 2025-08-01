from abc import ABC, abstractmethod
from typing import List

from core.models.settings import LlmModel


class SettingsLLMProvider(ABC):

    @abstractmethod
    def get_model_list(self) -> List[LlmModel]: pass
