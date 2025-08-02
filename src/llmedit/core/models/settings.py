from dataclasses import dataclass
from typing import Optional

from llmedit.core.models.enums.llm_provider_type import LlmProviderType


@dataclass(frozen=True)
class SettingsState:
    """
    Immutable data class representing the complete state of application settings.

    Captures all configurable LLM-related options at a point in time.
    """
    llm_provider: LlmProviderType
    llm_model_name: Optional[str]
    llm_temperature: float
    llm_temperature_enabled: bool
    source_language: str
    target_language: str


@dataclass(frozen=True)
class LlmModel:
    """
    Immutable data class representing a language model available in the system.

    Contains model identity and availability status. Used in UI selection components.
    """
    id: str
    name: str
    is_available: bool = False


@dataclass(frozen=True)
class ModelInformation:
    """
    Immutable data class containing configuration and metadata for a language model.

    Includes model source, generation parameters, formatting rules, and provider information.
    Serves as a blueprint for model loading and prompt formatting.
    """
    name: str
    repositoryId: str = ''
    fileName: str = ''
    output_length: int = 32768
    temperature: float = 0.5
    top_k: int = 40
    top_p: float = 0.95
    min_p: float = 0.05
    system_prompt_prefix: str = ''
    user_prompt_prefix: str = ''
    user_prompt_suffix: str = ''
    provider: LlmProviderType = LlmProviderType.LLAMA_CPP
