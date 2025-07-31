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
        logger.debug(f"Model folder path: {self._model_folder_path}")

    def get_model_list(self) -> List[LlmModel]:
        list_of_models: List[LlmModel] = []
        logger.debug("Getting list of models")
        for model in PREDEFINED_GGUF_MODELS:
            model_path = self._model_folder_path / model.fileName
            logger.debug(f"Checking if model {model.name} exists at path {model_path}")
            if model_path.exists() and model_path.is_file():
                logger.debug(f"Model {model.name} exists at path {model_path}")
                model_info = LlmModel(
                    id=model.fileName,
                    name=model.name,
                    is_available=True
                )
                logger.debug(f"Model info: {model_info}")
                list_of_models.append(model_info)
        logger.debug(f"List of models: {list_of_models}")
        return list_of_models
