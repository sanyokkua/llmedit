import logging
from abc import ABCMeta
from typing import Callable, Dict, Set, override

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

from core.interfaces.background.task_service import TaskService
from core.models.data_types import TaskInput, TaskResult

logger = logging.getLogger(__name__)


class TaskRunnable(QRunnable):
    def __init__(self, task_input: TaskInput, callback: Callable[[TaskResult], None]):
        super().__init__()
        self.task_input = task_input
        self.callback = callback
        self.setAutoDelete(True)
        logger.debug(
            "TaskRunnable: Initialized task '%s'",
            self.task_input.id,
        )

    def run(self):
        logger.debug(
            "TaskRunnable.run: Executing task '%s'",
            self.task_input.id,
        )
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
    pass


class TaskServiceImpl(TaskService, QObject, metaclass=_MetaQObjectABC):
    task_result_ready = pyqtSignal(TaskResult)
    _global_task_finished = pyqtSignal(object)
    _global_busy_state_changed = pyqtSignal(bool)

    def __init__(self, thread_pool: QThreadPool):
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

        # Track and start
        self._running[task_id] = runnable
        if len(self._running) == 1:  # Transition from idle to busy
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
        Logically cancel a task: its callbacks (global and per-task) will be suppressed.
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
            # Remove from callbacks but not running (not yet started)
            del self._per_task_callbacks[task_id]
            return True
        return False

    @override
    def cancel_all_tasks(self) -> None:
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
        busy = bool(self._running)
        logger.debug(
            "is_busy: System is %s",
            "BUSY" if busy else "IDLE",
        )
        return busy

    @override
    def subscribe_global_task_finished(self, listener: Callable[[TaskResult], None]) -> None:
        logger.debug(
            "subscribe_global_task_finished: New global listener registered (%s)",
            listener.__qualname__ if hasattr(listener, '__qualname__') else str(listener),
        )
        self._global_task_finished.connect(listener)

    @override
    def subscribe_global_busy_state_changed(self, listener: Callable[[bool], None]) -> None:
        logger.debug(
            "subscribe_global_busy_state_changed: New busy state listener registered (%s)",
            listener.__qualname__ if hasattr(listener, '__qualname__') else str(listener),
        )
        self._global_busy_state_changed.connect(listener)

    def _on_task_result_ready(self, result: TaskResult):
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
        task_id = result.id
        logger.debug(
            "_on_task_finished: Finalizing task '%s'",
            task_id,
        )

        # Remove from running
        self._running.pop(task_id, None)

        # Busy→idle transition
        if not self._running:
            logger.debug("_on_task_finished: System transitioned to IDLE state")
            self._global_busy_state_changed.emit(False)

        # Only emit if not canceled
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

        # Clean up cancel flag
        self._canceled.discard(task_id)
        logger.debug(
            "_on_task_finished: Cleanup complete for task '%s'",
            task_id,
        )
