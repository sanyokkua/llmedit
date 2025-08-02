import logging
from abc import ABCMeta
from typing import Callable, Dict, Set, override

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

from llmedit.core.interfaces.background.task_service import TaskService
from llmedit.core.models.data_types import TaskInput, TaskResult

logger = logging.getLogger(__name__)


class TaskRunnable(QRunnable):
    """
    Runnable task wrapper that executes a TaskInput and delivers results via callback.

    Executes in a thread pool and handles both successful completion and exceptions,
    wrapping the result in a TaskResult object for consistent delivery.
    """

    def __init__(self, task_input: TaskInput, callback: Callable[[TaskResult], None]):
        """
        Initialize the runnable with task input and completion callback.

        Args:
            task_input: Contains the function to execute and task metadata.
            callback: Function to call with the TaskResult when execution completes.

        Notes:
            Auto-deletion is enabled to clean up after execution.
        """
        super().__init__()
        self.task_input = task_input
        self.callback = callback
        self.setAutoDelete(True)
        logger.debug(
            "TaskRunnable: Initialized task '%s'",
            self.task_input.id,
        )

    def run(self):
        """
        Execute the task function and deliver the result.

        Notes:
            Catches all exceptions and wraps them in a failed TaskResult.
            Always calls the callback exactly once, even on error.
        """
        result = None
        try:
            value = self.task_input.task_func()
            result = TaskResult(
                id=self.task_input.id,
                task_result_content=value,
            )
            logger.debug(
                "TaskRunnable.run: Task '%s' completed successfully",
                self.task_input.id,
            )
        except Exception as exc:
            logger.warning(
                "TaskRunnable.run: Task '%s' failed with error: %s",
                self.task_input.id,
                str(exc),
                exc_info=True,
            )
            result = TaskResult(
                id=self.task_input.id,
                task_result_content=None,
                has_error=True,
                error_message=str(exc),
                exception=exc,
            )
        finally:
            self.callback(result)
            logger.debug(
                "TaskRunnable.run: Result for task '%s' delivered to callback",
                self.task_input.id,
            )


class _MetaQObjectABC(type(QObject), ABCMeta):
    """
    Metaclass combining QObject and ABCMeta.

    Allows TaskServiceImpl to inherit from both QObject (for Qt signals)
    and ABC (for abstract base class functionality).
    """
    pass


class TaskServiceImpl(TaskService, QObject, metaclass=_MetaQObjectABC):
    """
    Concrete implementation of TaskService using Qt's threading system.

    Manages asynchronous task execution through a QThreadPool. Provides global
    and per-task completion notifications, cancellation support, and busy state tracking.
    """

    task_result_ready = pyqtSignal(TaskResult)
    _global_task_finished = pyqtSignal(object)
    _global_busy_state_changed = pyqtSignal(bool)

    def __init__(self, thread_pool: QThreadPool):
        """
        Initialize service with a thread pool for task execution.

        Args:
            thread_pool: Shared QThreadPool for running tasks.

        Notes:
            Connects internal signals and initializes tracking structures for
            active tasks, callbacks, and cancellation state.
        """
        super().__init__()
        QObject.__init__(self)

        self._pool = thread_pool
        self._running: Dict[str, TaskRunnable] = { }
        self._canceled: Set[str] = set()
        self._per_task_callbacks: Dict[str, Callable[[TaskResult], None]] = { }

        self.task_result_ready.connect(self._on_task_result_ready)
        logger.debug(
            "TaskServiceImpl: Initialized with thread pool (max threads=%d)",
            self._pool.maxThreadCount(),
        )

    @override
    def submit_task(self, task_input: TaskInput) -> None:
        """
        Submit a new task for asynchronous execution.

        Args:
            task_input: Task to execute, including function and completion callback.

        Notes:
            Emits busy state change when transitioning from idle to busy.
            Tracks task for potential cancellation.
        """
        task_id = task_input.id
        logger.debug(
            "submit_task: Submitting task '%s'",
            task_id,
        )

        self._per_task_callbacks[task_id] = task_input.on_task_finished
        runnable = TaskRunnable(
            task_input,
            callback=lambda result: self.task_result_ready.emit(result),
        )

        self._running[task_id] = runnable
        if len(self._running) == 1:
            logger.debug("submit_task: System transitioned to BUSY state")
            self._global_busy_state_changed.emit(True)

        self._pool.start(runnable)
        logger.debug(
            "submit_task: Task '%s' started (active tasks=%d)",
            task_id,
            len(self._running),
        )

    @override
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a running or queued task.

        Args:
            task_id: Identifier of the task to cancel.

        Returns:
            True if the task was found and canceled, False otherwise.

        Notes:
            Running tasks are marked for cancellation (but may complete anyway).
            Queued tasks are removed from the callback registry.
        """
        if task_id in self._running:
            logger.warning(
                "cancel_task: Canceling task '%s' (was running)",
                task_id,
            )
            self._canceled.add(task_id)
            return True
        elif task_id in self._per_task_callbacks:
            logger.warning(
                "cancel_task: Canceling task '%s' (queued)",
                task_id,
            )
            del self._per_task_callbacks[task_id]
            return True
        return False

    @override
    def cancel_all_tasks(self) -> None:
        """
        Cancel all currently running and queued tasks.

        Notes:
            Marks all running tasks as canceled and clears the callback registry.
            No individual task completion signals will be emitted for canceled tasks.
        """
        count = len(self._running) + len(self._per_task_callbacks)
        if count > 0:
            logger.warning(
                "cancel_all_tasks: Canceling %d active and queued tasks",
                count,
            )
        for tid in list(self._running.keys()):
            self._canceled.add(tid)
        self._per_task_callbacks.clear()

    @override
    def is_busy(self) -> bool:
        """
        Check if the system is currently executing any tasks.

        Returns:
            True if one or more tasks are running, False if idle.

        Notes:
            Based solely on the number of running tasks (not queued ones).
        """
        busy = bool(self._running)
        logger.debug(
            "is_busy: System is %s",
            "BUSY" if busy else "IDLE",
        )
        return busy

    @override
    def subscribe_global_task_finished(self, listener: Callable[[TaskResult], None]) -> None:
        """
        Subscribe to notifications when any task completes (and is not canceled).

        Args:
            listener: Callback function to invoke with the TaskResult.

        Notes:
            Listener will not be called for canceled tasks.
            Multiple listeners can be registered.
        """
        logger.debug(
            "subscribe_global_task_finished: New global listener registered (%s)",
            listener.__qualname__ if hasattr(listener, '__qualname__') else str(listener),
        )
        self._global_task_finished.connect(listener)

    @override
    def subscribe_global_busy_state_changed(self, listener: Callable[[bool], None]) -> None:
        """
        Subscribe to notifications when the system busy state changes.

        Args:
            listener: Callback function to invoke with the new busy state (True/False).

        Notes:
            Useful for UI components that need to show loading indicators.
        """
        logger.debug(
            "subscribe_global_busy_state_changed: New busy state listener registered (%s)",
            listener.__qualname__ if hasattr(listener, '__qualname__') else str(listener),
        )
        self._global_busy_state_changed.connect(listener)

    def _on_task_result_ready(self, result: TaskResult):
        """
        Handle completion of a task and deliver to per-task callback.

        Args:
            result: The completed task result.

        Notes:
            Internal slot connected to task_result_ready signal.
            Always calls the per-task callback if registered.
        """
        task_id = result.id
        logger.debug(
            "_on_task_result_ready: Result received for task '%s' (success=%s)",
            task_id,
            not result.has_error,
        )

        callback = self._per_task_callbacks.pop(task_id, None)
        try:
            if callback:
                logger.debug(
                    "_on_task_result_ready: Executing per-task callback for '%s'",
                    task_id,
                )
                callback(result)
        except Exception as e:
            logger.error(
                "_on_task_result_ready: Per-task callback for '%s' failed: %s",
                task_id,
                str(e),
                exc_info=True,
            )
        finally:
            self._on_task_finished(result)

    def _on_task_finished(self, result: TaskResult):
        """
        Finalize task completion and emit global signals.

        Args:
            result: The completed task result.

        Notes:
            Removes task from tracking, updates busy state, and emits global
            completion signal only if the task was not canceled.
        """
        task_id = result.id
        logger.debug(
            "_on_task_finished: Finalizing task '%s'",
            task_id,
        )

        self._running.pop(task_id, None)

        if not self._running:
            logger.debug("_on_task_finished: System transitioned to IDLE state")
            self._global_busy_state_changed.emit(False)

        if task_id not in self._canceled:
            logger.debug(
                "_on_task_finished: Emitting global completion for task '%s'",
                task_id,
            )
            self._global_task_finished.emit(result)
        else:
            logger.debug(
                "_on_task_finished: Skipping global emit for canceled task '%s'",
                task_id,
            )

        self._canceled.discard(task_id)
        logger.debug(
            "_on_task_finished: Cleanup complete for task '%s'",
            task_id,
        )
