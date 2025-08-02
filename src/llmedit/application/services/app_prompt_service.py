import logging
from typing import Dict, Mapping, Sequence, Tuple

from typing_extensions import override

from config.application_prompts import APPLICATION_PROMPTS
from core.interfaces.prompt.prompt_service import PromptService
from core.models.data_types import Prompt
from core.models.enums.prompt_category import PromptCategory

logger = logging.getLogger(__name__)


class PromptNotFoundError(ValueError):
    """Raised when a requested prompt ID does not exist."""


class PromptValidationError(ValueError):
    """Raised when parameters for a prompt fail validation."""


class AppPromptService(PromptService):
    """
    Concrete PromptService using a fixed, in-memory list of application prompts.

    Public methods override PromptService to provide app-specific behavior.
    This implementation retrieves prompts from a static collection and supports parameterized template rendering.
    """

    @override
    def get_prompt(self, prompt_id: str) -> Prompt:
        """
        Return the Prompt whose `id` matches the given prompt_id.

        Args:
            prompt_id: The unique identifier of the prompt to retrieve.

        Returns:
            Prompt: The prompt object with the matching ID.

        Raises:
            PromptNotFoundError: If no prompt with the given ID exists.

        Notes:
            Performs a linear search through the APPLICATION_PROMPTS collection.
            Logs debug and warning messages for lookup results.
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
        Return all prompts whose category matches the given PromptCategory.

        Args:
            category: The category to filter prompts by.

        Returns:
            Sequence[Prompt]: A list of prompts belonging to the specified category.

        Notes:
            Returns an empty sequence if no prompts match.
            Logs the number of results at info level.
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
        Substitute placeholders in the prompt's template with corresponding parameter values.

        Args:
            prompt: The prompt object containing the template to fill.
            parameters: A dictionary mapping parameter names to their values.

        Returns:
            str: The fully rendered prompt string with all placeholders replaced.

        Raises:
            PromptValidationError: If required parameters are missing or validation fails.

        Notes:
            Uses validate_prompt_parameters to check input validity before substitution.
            Logs the result snippet (truncated if longer than 100 characters).
        """
        logger.debug(
            "apply_prompt_parameters: id=%r, params=%s",
            prompt.id,
            list(parameters.keys()),
        )

        is_valid, error = self.validate_prompt_parameters(prompt, parameters)
        if not is_valid:
            logger.error(
                "apply_prompt_parameters: validation failed for id=%r: %s",
                prompt.id,
                error,
            )
            raise PromptValidationError(error)

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
        Validate that all required parameters for the prompt are present in the input.

        Args:
            prompt: The prompt whose required parameters are checked.
            parameters: The provided parameters to validate.

        Returns:
            Tuple[bool, str]: A tuple where the first element is True if validation
                passes, otherwise False. The second element is an empty string on
                success or an error message on failure.

        Notes:
            Only checks presence of required keys; does not validate their values.
            Logs missing parameters as warnings.
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
        Replace all occurrences of `{{key}}` in the template with corresponding values from parameters.

        Args:
            template: The string containing placeholders to replace.
            parameters: A mapping of placeholder names to their replacement values.

        Returns:
            str: The template string with all placeholders substituted.

        Notes:
            Placeholder format is double-braced: `{{key}}`.
            No escaping or nested substitution is performed.
        """
        result = template
        for key, val in parameters.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, val)
        return result
