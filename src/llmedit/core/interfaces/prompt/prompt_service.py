from abc import ABC, abstractmethod
from typing import List

from core.models.data_types import Prompt
from core.models.enums.prompt import PromptCategory


class PromptService(ABC):
    """
    Abstract base class defining the interface for managing and processing prompts.

    Implementations provide access to prompt templates, support parameter injection,
    and validate required inputs. Used to construct dynamic prompts for LLM queries.
    """

    @abstractmethod
    def get_prompt(self, prompt_id: str) -> Prompt:
        """
        Retrieve a prompt by its unique identifier.

        Args:
            prompt_id: The ID of the prompt to retrieve.

        Returns:
            Prompt object containing the template and metadata.

        Raises:
            PromptNotFoundError: If no prompt with the given ID exists.

        Notes:
            Prompt IDs are expected to be unique across the application.
        """

    @abstractmethod
    def get_prompts_by_category(self, category: PromptCategory) -> List[Prompt]:
        """
        Retrieve all prompts belonging to a specific category.

        Args:
            category: The PromptCategory to filter by.

        Returns:
            List of Prompt objects that belong to the specified category.

        Notes:
            Returns empty list if no prompts match the category.
        """

    @abstractmethod
    def apply_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> str:
        """
        Fill a prompt template with provided parameter values.

        Args:
            prompt: The prompt template to fill.
            parameters: Dictionary mapping parameter names to their values.

        Returns:
            Fully rendered prompt string with all placeholders replaced.

        Raises:
            PromptValidationError: If required parameters are missing or invalid.

        Notes:
            Placeholder format is typically `{{key}}`. Behavior depends on implementation.
        """

    @abstractmethod
    def validate_prompt_parameters(self, prompt: Prompt, parameters: dict[str, str]) -> tuple[bool, str]:
        """
        Validate that all required parameters for a prompt are present.

        Args:
            prompt: The prompt whose required parameters are checked.
            parameters: The provided parameters to validate.

        Returns:
            Tuple where first element is True if valid, False otherwise.
            Second element is an empty string on success or an error message on failure.

        Notes:
            Only checks presence of required keys, not their values.
        """
