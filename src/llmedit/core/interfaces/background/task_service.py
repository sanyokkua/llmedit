from abc import ABC, abstractmethod
from typing import Callable

from core.models.data_types import TaskInput, TaskResult


class TaskService(ABC):

    @abstractmethod
    def submit_task(self, task_input: TaskInput) -> None:
        pass

    @abstractmethod
    def cancel_task(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def cancel_all_tasks(self) -> None:
        pass

    @abstractmethod
    def is_busy(self) -> bool:
        pass

    @abstractmethod
    def subscribe_global_task_finished(self, listener: Callable[[TaskResult], None]) -> None:
        pass

    @abstractmethod
    def subscribe_global_busy_state_changed(self, listener: Callable[[bool], None]) -> None:
        pass
