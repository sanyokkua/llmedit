from abc import ABC, abstractmethod
from typing import List

from core.models.enums.prompt import PromptCategory
from core.models.data_types import Prompt


class PromptService(ABC):

    @abstractmethod
    def get_prompt(self, prompt_id: str) -> Prompt:
        pass

    @abstractmethod
    def get_prompts_by_category(self, category: PromptCategory) -> List[Prompt]:
        pass

    @abstractmethod
    def apply_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> str:
        pass

    @abstractmethod
    def validate_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> tuple[bool, str]: pass
