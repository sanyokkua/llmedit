import logging
from typing import Optional

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QWidget,
    QSizePolicy, QVBoxLayout, QMessageBox
)

from config.prompts_objects import PROMPT_PARAM_USER_TEXT, PROMPT_PARAM_INPUT_LANGUAGE, PROMPT_PARAM_OUTPUT_LANGUAGE
from context import AppContext
from core.models.data_types import TaskInput, TaskResult, ProcessingContext
from ui.base_widget import BaseWidget
from ui.content.tab_widgets.action_controls_widget import ActionEvent
from ui.content.tab_widgets.action_tabs_widget import ActionTabsWidget
from ui.content.text_widgets.text_interaction_areas_widget import TextInteractionAreasWidget

logger = logging.getLogger(__name__)


class CentralWidget(BaseWidget):
    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing central widget")

        self._text_widget = TextInteractionAreasWidget(ctx)
        self._tabs = ActionTabsWidget(ctx)

        layout = QVBoxLayout()
        layout.addWidget(self._text_widget, 8)
        layout.addWidget(self._tabs, 2)
        self.setLayout(layout)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self._tabs.action_button_clicked.connect(self._on_action_btn_clicked)

        logger.debug(
            "__init__: Central widget initialized with %d text areas and %d tabs",
            2,  # Input and output text areas
            self._tabs.count()
        )

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """Update widget state based on system readiness."""
        state = "ENABLED" if enabled else "DISABLED"
        logger.debug(
            "on_widgets_enabled_changed: Setting central widget to %s",
            state
        )
        self.setEnabled(enabled)

    def _on_action_btn_clicked(self, action: ActionEvent) -> None:
        """Handle action button click events."""
        logger.debug(
            "_on_action_btn_clicked: Button '%s' clicked (prompt: '%s')",
            action.action_id,
            action.prompt.name
        )

        # Check system readiness
        system_ready = self._ctx.is_system_ready()
        task_busy = self._ctx.task_service.is_busy()

        if not system_ready or task_busy:
            status = "NOT READY" if not system_ready else "BUSY"
            reason = "model not selected" if not system_ready else "task in progress"

            logger.debug(
                "_on_action_btn_clicked: Action skipped - system %s (%s)",
                status,
                reason
            )

            msg_box = QMessageBox()
            msg_box.setWindowTitle("System not ready")
            msg_box.setText(f"System is {status.lower()}. {reason.capitalize()}.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.exec()
            return

        # Prepare task execution
        logger.debug(
            "_on_action_btn_clicked: Preparing task '%s' execution",
            action.action_id
        )

        def closure() -> str:
            logger.debug(
                "_on_action_btn_clicked.closure: Executing task '%s'",
                action.action_id
            )

            # Build prompt parameters
            prompt_parameters = {
                PROMPT_PARAM_USER_TEXT: self._text_widget.input_text(),
            }

            if action.input_dropdown_item:
                input_lang = action.input_dropdown_item()
                logger.debug(
                    "_on_action_btn_clicked.closure: Using input language '%s'",
                    input_lang
                )
                prompt_parameters[PROMPT_PARAM_INPUT_LANGUAGE] = input_lang

            if action.output_dropdown_item:
                output_lang = action.output_dropdown_item()
                logger.debug(
                    "_on_action_btn_clicked.closure: Using output language '%s'",
                    output_lang
                )
                prompt_parameters[PROMPT_PARAM_OUTPUT_LANGUAGE] = output_lang

            # Create processing context
            process_ctx = ProcessingContext(
                user_prompt_id=action.prompt.id,
                prompt_parameters=prompt_parameters
            )

            logger.debug(
                "_on_action_btn_clicked.closure: Processing context created - prompt_id=%s, params_count=%d",
                process_ctx.user_prompt_id,
                len(process_ctx.prompt_parameters)
            )

            return self._ctx.text_processing_service.process(process_ctx)

        # Submit task
        task = TaskInput(
            id=action.action_id,
            task_func=closure,
            on_task_finished=self._on_task_finished
        )

        logger.debug(
            "_on_action_btn_clicked: Submitting task '%s' to task service",
            action.action_id
        )
        self._ctx.task_service.submit_task(task)

    def _on_task_finished(self, task_result: TaskResult) -> None:
        """Handle task completion events."""
        if task_result.has_error:
            logger.error(
                "_on_task_finished: Task '%s' failed with error: %s",
                task_result.id,
                task_result.error_message,
                exc_info=task_result.exception
            )

            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(f"Failed to execute task: {task_result.error_message}")
            error_dialog.setWindowTitle("Task Execution Failed")
            error_dialog.exec()
        else:
            logger.debug(
                "_on_task_finished: Task '%s' completed successfully",
                task_result.id
            )
            logger.debug(
                "_on_task_finished: Setting output with %d characters",
                len(task_result.task_result_content or "")
            )
            self.set_output_text(str(task_result.task_result_content))

    def set_output_text(self, text: str) -> None:
        """Set output text in the text interaction area."""
        logger.debug(
            "set_output_text: Displaying %d characters in output area",
            len(text)
        )
        self._text_widget.set_output_text(text)
