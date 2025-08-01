import logging
from pathlib import Path
from typing import List, override

from config.gguf_models import PREDEFINED_GGUF_MODELS
from core.interfaces.settings.settings_llm_provider import SettingsLLMProvider
from core.models.settings import LlmModel

logger = logging.getLogger(__name__)


class SettingsLlamaCppProvider(SettingsLLMProvider):
    def __init__(self, model_folder_path: Path) -> None:
        self._model_folder_path = model_folder_path
        logger.debug(
            "__init__: Model folder path set to '%s'",
            self._model_folder_path,
        )

    @override
    def get_model_list(self) -> List[LlmModel]:
        """
        Retrieve available GGUF models from configured folder.

        Returns:
            List of available LLM models sorted by name
        """
        logger.debug(
            "get_model_list: Scanning '%s' for %d predefined models",
            self._model_folder_path,
            len(PREDEFINED_GGUF_MODELS),
        )

        try:
            # Filter available models using list comprehension
            available_models = [
                LlmModel(
                    id=model.fileName,
                    name=model.name,
                    is_available=True,
                )
                for model in PREDEFINED_GGUF_MODELS
                if self._is_model_available(model.fileName)
            ]

        except Exception as e:
            logger.error("get_model_list: Error while scanning for models - %s", e, exc_info=True)
            return []

        logger.debug(
            "get_model_list: Found %d/%d available models",
            len(available_models),
            len(PREDEFINED_GGUF_MODELS),
        )

        # Sort models by name (more readable than lambda)
        return sorted(available_models, key=lambda model: model.name)

    def _is_model_available(self, file_name: str) -> bool:
        """
        Check if a model file exists and is available.

        Args:
            file_name: Name of the model file to check

        Returns:
            True if model file exists and is a regular file, False otherwise
        """
        try:
            model_path = self._model_folder_path / file_name
            logger.debug("Checking model file: '%s'", model_path)

            is_available = model_path.exists() and model_path.is_file()
            if is_available:
                logger.debug("Model file found: '%s'", model_path)
            else:
                logger.debug("Model file not found or not a regular file: '%s'", model_path)

            return is_available
        except OSError as e:
            logger.warning("Error checking model file '%s' - %s", file_name, e)
            return False
        except Exception as e:
            logger.error("Unexpected error checking model file '%s' - %s", file_name, e, exc_info=True)
            return False
