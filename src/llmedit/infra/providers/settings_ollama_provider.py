import logging
from typing import List

import ollama

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.models.settings import LlmModel

logger = logging.getLogger(__name__)


class SettingsOllamaProvider(SettingsLLMProvider):
    def get_model_list(self) -> List[LlmModel]:
        logger.debug("Getting list of models")
        response = ollama.list()
        logger.debug(f"Response: {response}")
        model_names = [model["model"] for model in response["models"]]
        models: List[LlmModel] = []
        for model_name in model_names:
            model = LlmModel(
                id=model_name,
                name=model_name,
                is_available=True
            )
            models.append(model)
        logger.debug(f"Models: {models}")
        return models
