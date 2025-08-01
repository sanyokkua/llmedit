import logging
from typing import List, override

import ollama

from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.models.settings import LlmModel

logger = logging.getLogger(__name__)


class SettingsOllamaProvider(SettingsLLMProvider):
    """
    Implementation of SettingsLLMProvider for Ollama backend.

    Retrieves available models by querying the Ollama service API.
    Converts the response into LlmModel instances with availability status.
    """

    @override
    def get_model_list(self) -> List[LlmModel]:
        """
        Retrieve available models from Ollama service.

        Returns:
            List of LlmModel instances representing models available in Ollama,
            sorted alphabetically by name.

        Raises:
            Exception: If connection to Ollama service fails or API request errors.

        Notes:
            Uses ollama.list() to fetch model information. Logs detailed debugging
            information about the response and model count.
        """
        logger.debug("get_model_list: Starting model list retrieval from Ollama")

        try:
            response = ollama.list()
            logger.debug("get_model_list: Ollama API responded with %d models", len(response["models"]))
        except Exception as e:
            logger.error("get_model_list: Failed to connect to Ollama service", exc_info=True)
            raise e

        model_names = [model["model"] for model in response["models"]]

        if model_names:
            sample = ", ".join(model_names[:5])
            suffix = f" ... ({len(model_names) - 5} more)" if len(model_names) > 5 else ""
            logger.debug("get_model_list: Found models: %s%s", sample, suffix)
        else:
            logger.debug("get_model_list: No models found in Ollama")

        models = [
            LlmModel(
                id=model_name,
                name=model_name,
                is_available=True,
            ) for model_name in model_names
        ]

        models.sort(key=lambda x: x.name)

        logger.debug("get_model_list: Prepared %d model objects for return", len(models))
        return models
