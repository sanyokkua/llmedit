import logging
from typing import List

from config.prompts_objects import APPLICATION_PROMPTS
from core.models.enums.prompt import PromptCategory
from core.interfaces.prompt.prompt_service import PromptService
from core.models.data_types import Prompt

logger = logging.getLogger(__name__)

class AppPromptService(PromptService):
    def get_prompt(self, prompt_id: str) -> Prompt:
        logger.debug(f"Getting prompt with id: {prompt_id}")
        for APPLICATION_PROMPT in APPLICATION_PROMPTS:
            if APPLICATION_PROMPT.id == prompt_id:
                logger.debug(f"Prompt found: {APPLICATION_PROMPT}")
                return APPLICATION_PROMPT
        raise ValueError(f"Prompt with id {prompt_id} not found.")

    def get_prompts_by_category(self, category: PromptCategory) -> List[Prompt]:
        logger.debug(f"Getting prompts by category: {category}")
        prompts = [prompt for prompt in APPLICATION_PROMPTS if prompt.category == category]
        logger.debug(f"Prompts found: {prompts}")
        return prompts

    def apply_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> str:
        logger.debug(f"Applying prompt parameters to prompt: {prompt}")
        is_valid, err = self.validate_prompt_parameters(prompt, parameters)
        if not is_valid:
            raise ValueError(err)

        prompt_template = prompt.template
        for parameter in parameters:
            replace_value = f"{{{parameter}}}"
            prompt_template = prompt_template.replace(replace_value, parameters[parameter])

        logger.debug(f"Prompt template after replacement: {prompt_template}")
        return prompt_template

    def validate_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> tuple[bool, str]:
        logger.debug(f"Validating prompt parameters for prompt: {prompt}")
        is_valid = True
        errors: List[str] = []
        for parameter in parameters:
            parameter_value = f"{{{parameter}}}"
            if not parameter_value in prompt.template:
                logger.debug(f"Parameter {parameter} not found in prompt template.")
                is_valid = False
                errors.append(f"Parameter {parameter} not found in prompt template.")
        logger.debug(f"Prompt parameters validation result: {is_valid}")
        return is_valid, "; ".join(errors)
