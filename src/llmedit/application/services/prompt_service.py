import logging
from typing import Dict, Mapping, Sequence, Tuple

from typing_extensions import override

from config.prompts_objects import APPLICATION_PROMPTS
from core.interfaces.prompt.prompt_service import PromptService
from core.models.data_types import Prompt
from core.models.enums.prompt import PromptCategory

logger = logging.getLogger(__name__)


class PromptNotFoundError(ValueError):
    """Raised when a requested prompt ID does not exist."""


class PromptValidationError(ValueError):
    """Raised when parameters for a prompt fail validation."""


class AppPromptService(PromptService):
    """
    Concrete PromptService using a fixed, in-memory list of application prompts.
    Public methods override PromptService to provide app-specific behavior.
    """

    @override
    def get_prompt(self, prompt_id: str) -> Prompt:
        """
        Override: Return the Prompt whose `id` matches `prompt_id`.
        Raises PromptNotFoundError if no match.
        """
        logger.debug("get_prompt: looking up id=%r", prompt_id)

        prompt = next((p for p in APPLICATION_PROMPTS if p.id == prompt_id), None)
        if prompt is None:
            logger.warning("get_prompt: no prompt for id=%r", prompt_id)
            raise PromptNotFoundError(f"No prompt with id={prompt_id!r}")

        logger.debug(
            "get_prompt: found id=%r (category=%s)",
            prompt.id,
            prompt.category.value,
        )
        return prompt

    @override
    def get_prompts_by_category(self, category: PromptCategory) -> Sequence[Prompt]:
        """
        Override: Return all prompts whose `.category` equals the given category.
        """
        logger.debug(
            "get_prompts_by_category: filtering category=%s", category.value,
        )

        results = [p for p in APPLICATION_PROMPTS if p.category == category]

        logger.info(
            "get_prompts_by_category: %d found for category=%s",
            len(results),
            category.value,
        )
        return results

    @override
    def apply_prompt_parameters(
        self,
        prompt: Prompt,
        parameters: Dict[str, str],
    ) -> str:
        """
        Override: Substitute placeholders in `prompt.template` with values from `parameters`.
        Raises PromptValidationError if validation fails.
        """
        logger.debug(
            "apply_prompt_parameters: id=%r, params=%s",
            prompt.id,
            list(parameters.keys()),
        )

        # Validate; uses public validate_prompt_parameters
        is_valid, error = self.validate_prompt_parameters(prompt, parameters)
        if not is_valid:
            logger.error(
                "apply_prompt_parameters: validation failed for id=%r: %s",
                prompt.id,
                error,
            )
            raise PromptValidationError(error)

        # Perform all replacements
        filled = self._substitute_placeholders(prompt.template, parameters)

        snippet = filled if len(filled) <= 100 else filled[:100] + "…"
        logger.debug("apply_prompt_parameters: result=%r", snippet)
        return filled

    @override
    def validate_prompt_parameters(
        self,
        prompt: Prompt,
        parameters: Dict[str, str],
    ) -> Tuple[bool, str]:
        """
        Override: Validate required parameters are present.
        Returns (True, "") if valid, otherwise (False, error_message).
        """
        missing = [p for p in prompt.parameters if p not in parameters]
        if missing:
            message = f"Missing required parameters: {', '.join(missing)}"
            logger.warning(
                "validate_prompt_parameters: %s", message,
            )
            return False, message

        logger.debug(
            "validate_prompt_parameters: all %d parameters present for id=%r",
            len(prompt.parameters),
            prompt.id,
        )
        return True, ""

    @staticmethod
    def _substitute_placeholders(
        template: str,
        parameters: Mapping[str, str],
    ) -> str:
        """
        Internal: Replace all occurrences of `{{key}}` in `template` with
        `parameters[key]`.
        """
        result = template
        for key, val in parameters.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, val)
        return result
