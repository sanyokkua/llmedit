import logging
from pathlib import Path
from typing import List

from config.gguf_models import PREDEFINED_GGUF_MODELS
from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.models.settings import LlmModel

logger = logging.getLogger(__name__)


class SettingsLlamaCppProvider(SettingsLLMProvider):
    def __init__(self, model_folder_path: Path) -> None:
        self._model_folder_path = model_folder_path
        logger.debug(
            "__init__: Model folder path set to '%s'",
            self._model_folder_path
        )

    def get_model_list(self) -> List[LlmModel]:
        """Retrieve available GGUF models from configured folder."""
        logger.debug(
            "get_model_list: Scanning '%s' for %d predefined models",
            self._model_folder_path,
            len(PREDEFINED_GGUF_MODELS)
        )

        available_models = []
        for model in PREDEFINED_GGUF_MODELS:
            model_path = self._model_folder_path / model.fileName
            logger.debug(
                "get_model_list: Checking model '%s' (file: '%s')",
                model.name,
                model.fileName
            )

            if model_path.exists() and model_path.is_file():
                logger.debug(
                    "get_model_list: Model '%s' found at '%s'",
                    model.name,
                    model_path
                )
                model_info = LlmModel(
                    id=model.fileName,
                    name=model.name,
                    is_available=True
                )
                available_models.append(model_info)

        logger.debug(
            "get_model_list: Found %d/%d available models",
            len(available_models),
            len(PREDEFINED_GGUF_MODELS)
        )
        available_models.sort(key=lambda x: x.name)
        return available_models
