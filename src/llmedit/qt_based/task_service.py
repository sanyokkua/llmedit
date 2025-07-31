from abc import ABCMeta
from typing import Callable, Dict, Set

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

from core.interfaces.background.task_service import TaskService
from core.models.data_types import TaskInput, TaskResult


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    finished = pyqtSignal(object)  # emits TaskResult


class TaskRunnable(QRunnable):
    def __init__(self, task_input: TaskInput):
        super().__init__()
        self.task_input = task_input
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    def run(self):
        result = None
        try:
            value = self.task_input.task_func()
            result = TaskResult(
                id=self.task_input.id,
                task_result=value,
            )
        except Exception as exc:
            result = TaskResult(
                id=self.task_input.id,
                task_result=None,
                has_error=True,
                error_message=str(exc),
                exception=exc
            )
        finally:
            self.signals.finished.emit(result)


class _MetaQObjectABC(type(QObject), ABCMeta):
    pass


class TaskServiceImpl(TaskService, QObject, metaclass=_MetaQObjectABC):
    _global_task_finished = pyqtSignal(object)
    _global_busy_state_changed = pyqtSignal(bool)

    def __init__(self, thread_pool: QThreadPool):
        super().__init__()
        QObject.__init__(self)

        self._pool = thread_pool
        self._running: Dict[str, TaskRunnable] = {}
        self._canceled: Set[str] = set()

    def submit_task(self, task_input: TaskInput) -> None:
        runnable = TaskRunnable(task_input)
        task_id = task_input.id

        # connect per-task callback
        runnable.signals.finished.connect(lambda result: task_input.on_task_finished(result))
        # connect global handler
        runnable.signals.finished.connect(self._on_task_finished)

        # track and start
        self._running[task_id] = runnable
        if len(self._running) > 0:
            self._global_busy_state_changed.emit(True)

        self._pool.start(runnable)

    def cancel_task(self, task_id: str) -> bool:
        """
        Logically cancel a task: its callbacks (global and per-task) will be suppressed.
        """
        if task_id in self._running:
            self._canceled.add(task_id)
            return True
        return False

    def cancel_all_tasks(self) -> None:
        for tid in list(self._running.keys()):
            self._canceled.add(tid)

    def is_busy(self) -> bool:
        return bool(self._running)

    def subscribe_global_task_finished(self, listener: Callable[[TaskResult], None]) -> None:
        self._global_task_finished.connect(listener)

    def subscribe_global_busy_state_changed(self, listener: Callable[[bool], None]) -> None:
        self._global_busy_state_changed.connect(listener)

    def _on_task_finished(self, result: TaskResult):
        task_id = result.id

        # remove from running
        self._running.pop(task_id, None)
        # busy→idle transition
        if not len(self._running):
            self._global_busy_state_changed.emit(False)

        # only emit if not canceled
        if task_id not in self._canceled:
            self._global_task_finished.emit(result)

        # clean up a cancel flag
        self._canceled.discard(task_id)
