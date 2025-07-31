from dataclasses import dataclass
from typing import Optional

from core.models.enums.settings import LlmProviderType


@dataclass(frozen=True)
class SettingsState:
    llm_provider: LlmProviderType
    llm_model_name: Optional[str]
    llm_temperature: float
    llm_temperature_enabled: bool


@dataclass(frozen=True)
class LlmModel:
    id: str
    name: str
    is_available: bool = False


@dataclass(frozen=True)
class ModelInformation:
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
