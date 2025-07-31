from abc import ABC, abstractmethod
from typing import List, Callable

from core.models.settings import LlmModel


class SettingsLLMProvider(ABC):

    @abstractmethod
    def get_model_list(self) -> List[LlmModel]: pass

