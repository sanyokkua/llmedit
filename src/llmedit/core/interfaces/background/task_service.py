from abc import ABC, abstractmethod
from typing import Callable

from core.models.data_types import TaskInput, TaskResult


class TaskService(ABC):
    """
    Abstract base class defining the interface for task management and execution.

    Implementations handle asynchronous task processing, lifecycle management, and event broadcasting.
    Supports submitting, canceling, and monitoring tasks, as well as subscribing to global task events.
    """

    @abstractmethod
    def submit_task(self, task_input: TaskInput) -> None:
        """
        Submit a new task for asynchronous execution.

        Args:
            task_input: Input data and configuration for the task to be executed.

        Notes:
            This method returns immediately. Task execution occurs in the background.
        """

    @abstractmethod
    def cancel_task(self, task_id: str) -> bool:
        """
        Attempt to cancel a running task by its identifier.

        Args:
            task_id: Unique identifier of the task to cancel.

        Returns:
            True if the task was found and cancellation was initiated, False otherwise.

        Notes:
            Cancellation may not be immediate or guaranteed depending on task state.
        """

    @abstractmethod
    def cancel_all_tasks(self) -> None:
        """
        Cancel all currently running tasks.

        Notes:
            Iterates through active tasks and attempts to cancel each one.
            No guarantee that all tasks will stop immediately.
        """

    @abstractmethod
    def is_busy(self) -> bool:
        """
        Check if the service is currently executing one or more tasks.

        Returns:
            True if any task is running, False if the service is idle.

        Notes:
            Used to determine system load or readiness for new tasks.
        """

    @abstractmethod
    def subscribe_global_task_finished(self, listener: Callable[[TaskResult], None]) -> None:
        """
        Subscribe to notifications when any task completes.

        Args:
            listener: Callback function to invoke with the TaskResult when a task finishes.

        Notes:
            Multiple listeners can be registered. The service manages listener lifecycle.
        """

    @abstractmethod
    def subscribe_global_busy_state_changed(self, listener: Callable[[bool], None]) -> None:
        """
        Subscribe to notifications when the busy state changes.

        Args:
            listener: Callback function to invoke with the new busy state (True/False).

        Notes:
            Useful for UI components that need to reflect system activity status.
        """
