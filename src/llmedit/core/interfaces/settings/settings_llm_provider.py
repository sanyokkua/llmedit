from abc import ABC, abstractmethod
from typing import List

from core.models.settings import LlmModel


class SettingsLLMProvider(ABC):
    """
    Abstract base class defining the interface for LLM model providers in settings.

    Implementations provide access to available language models for a specific backend
    (e.g., llama.cpp, Ollama). Used by settings service to populate model selection options.
    """

    @abstractmethod
    def get_model_list(self) -> List[LlmModel]:
        """
        Retrieve the list of available LLM models from this provider.

        Returns:
            List of LlmModel objects representing available models.

        Notes:
            Each model includes ID, name, and availability status.
            Implementations may retrieve models from local filesystem, remote API, or other sources.
        """
