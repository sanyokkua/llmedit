from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from core.models.enums.prompt import PromptCategory


@dataclass(frozen=True)
class Prompt:
    id: str
    name: str
    description: str
    category: PromptCategory
    template: str
    parameters: List[str]


@dataclass(frozen=True)
class ProcessingContext:
    user_prompt_id: str
    prompt_parameters: dict[str, str]


@dataclass(frozen=True)
class GenerationRequest:
    system_prompt: str
    user_prompt: str
    temperature: float
    top_k: int
    top_p: float
    min_p: float


@dataclass(frozen=True)
class GenerationResponse:
    text_content: str
    original_request: GenerationRequest
    metadata: dict[str, str]


@dataclass(frozen=True)
class TaskResult:
    id: str
    task_result_content: Any
    has_error: bool = False
    error_message: str = ''
    exception: Optional[Exception] = None


@dataclass(frozen=True)
class TaskInput:
    id: str
    task_func: Callable[[], Any]
    on_task_finished: Callable[[TaskResult], None]
