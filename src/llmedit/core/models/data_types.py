from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from core.models.enums.prompt import PromptCategory


@dataclass(frozen=True)
class Prompt:
    """
    Immutable data class representing a prompt template.

    Contains all information needed to render a prompt for LLM use, including
    parameters and categorization.
    """
    id: str
    name: str
    description: str
    category: PromptCategory
    template: str
    parameters: List[str]


@dataclass(frozen=True)
class ProcessingContext:
    """
    Immutable data class containing input data for text processing.

    Bundles prompt selection and parameter values needed to generate a response.
    """
    user_prompt_id: str
    prompt_parameters: dict[str, str]


@dataclass(frozen=True)
class GenerationRequest:
    """
    Immutable data class representing a request for text generation.

    Contains prompts, sampling parameters, and other settings for model inference.
    """
    system_prompt: str
    user_prompt: str
    temperature: float
    top_k: int
    top_p: float
    min_p: float


@dataclass(frozen=True)
class GenerationResponse:
    """
    Immutable data class representing a model's response to a generation request.

    Contains the generated text and metadata about the request and response.
    """
    text_content: str
    original_request: GenerationRequest
    metadata: dict[str, str]


@dataclass(frozen=True)
class TaskResult:
    """
    Immutable data class representing the result of an asynchronous task.

    Contains the output, error status, and optional error details.
    """
    id: str
    task_result_content: Any
    has_error: bool = False
    error_message: str = ''
    exception: Optional[Exception] = None


@dataclass(frozen=True)
class TaskInput:
    """
    Immutable data class representing an asynchronous task to be executed.

    Contains the task function, completion callback, and identifier.
    """
    id: str
    task_func: Callable[[], Any]
    on_task_finished: Callable[[TaskResult], None]
