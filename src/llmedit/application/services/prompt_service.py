import logging
from typing import List

from config.prompts_objects import APPLICATION_PROMPTS
from core.interfaces.prompt.prompt_service import PromptService
from core.models.data_types import Prompt
from core.models.enums.prompt import PromptCategory

logger = logging.getLogger(__name__)


class AppPromptService(PromptService):
    def get_prompt(self, prompt_id: str) -> Prompt:
        """Retrieve a specific prompt by ID."""
        logger.debug("get_prompt: Requesting prompt with id '%s'", prompt_id)

        for app_prompt in APPLICATION_PROMPTS:
            if app_prompt.id == prompt_id:
                logger.debug(
                    "get_prompt: Found prompt '%s' (category: %s)",
                    app_prompt.id,
                    app_prompt.category.value
                )
                return app_prompt

        logger.warning("get_prompt: Prompt not found for id '%s'", prompt_id)
        raise ValueError(f"Prompt with id '{prompt_id}' not found.")

    def get_prompts_by_category(self, category: PromptCategory) -> List[Prompt]:
        """Retrieve prompts filtered by category."""
        logger.debug("[%s] get_prompts_by_category: Requesting category '%s'", __name__, category.value)

        prompts = [p for p in APPLICATION_PROMPTS if p.category == category]
        logger.info(
            "get_prompts_by_category: Found %d prompts for category '%s'",
            len(prompts),
            category.value
        )
        return prompts

    def apply_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> str:
        """Apply parameters to a prompt template."""
        logger.debug(
            "apply_prompt_parameters: Processing prompt '%s' with %d parameters",
            prompt.id,
            len(parameters)
        )

        is_valid, err = self.validate_prompt_parameters(prompt, parameters)
        if not is_valid:
            logger.error(
                "apply_prompt_parameters: Validation failed for prompt '%s' - %s",
                prompt.id,
                err
            )
            raise ValueError(err)

        prompt_template = prompt.template
        for param, value in parameters.items():
            placeholder = "{{" + param + "}}"
            prompt_template = prompt_template.replace(placeholder, value)
            logger.debug(
                "apply_prompt_parameters: Replaced '%s' with '%s'",
                placeholder,
                value
            )

        logger.debug(
            "apply_prompt_parameters: Final template: '%s'",
            prompt_template[:100] + "..." if len(prompt_template) > 100 else prompt_template
        )
        return prompt_template

    def validate_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> tuple[bool, str]:
        """Validate required parameters are present."""
        logger.debug(
            "validate_prompt_parameters: Validating %d required parameters for prompt '%s'",
            len(prompt.parameters),
            prompt.id
        )

        missing = [p for p in prompt.parameters if p not in parameters]
        if missing:
            logger.warning(
                "validate_prompt_parameters: Missing %d parameters: %s",
                len(missing),
                ", ".join(missing)
            )
            return False, f"Missing required parameters: {', '.join(missing)}"

        logger.debug(
            "validate_prompt_parameters: All %d parameters present",
            len(prompt.parameters)
        )
        return True, ""
