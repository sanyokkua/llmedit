import logging
from typing import Optional

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QMessageBox, QSizePolicy, QVBoxLayout, QWidget)

from config.prompts_objects import PROMPT_PARAM_INPUT_LANGUAGE, PROMPT_PARAM_OUTPUT_LANGUAGE, PROMPT_PARAM_USER_TEXT
from context import AppContext
from core.models.data_types import ProcessingContext, TaskInput, TaskResult
from ui.base_widget import BaseWidget
from ui.content.tab_widgets.action_controls_widget import ActionEvent
from ui.content.tab_widgets.action_tabs_widget import ActionTabsWidget
from ui.content.text_widgets.text_interaction_areas_widget import TextInteractionAreasWidget

logger = logging.getLogger(__name__)


class CentralWidget(BaseWidget):
    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing central widget")

        try:
            self._text_widget = TextInteractionAreasWidget(ctx)
            self._tabs = ActionTabsWidget(ctx)

            layout = QVBoxLayout()
            layout.addWidget(self._text_widget, 8)
            layout.addWidget(self._tabs, 2)
            self.setLayout(layout)

            self.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            self._tabs.action_button_clicked.connect(self._on_action_btn_clicked)

            logger.debug(
                "__init__: Central widget initialized with %d text areas and %d tabs",
                2,  # Input and output text areas
                self._tabs.count(),
            )
        except Exception as e:
            logger.error(
                "__init__: Failed to initialize central widget: %s",
                str(e),
                exc_info=True,
            )
            raise

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """Update widget state based on system readiness."""
        try:
            state = "ENABLED" if enabled else "DISABLED"
            logger.debug(
                "on_widgets_enabled_changed: Setting central widget to %s",
                state,
            )
            self.setEnabled(enabled)
        except Exception as e:
            logger.error(
                "on_widgets_enabled_changed: Failed to change widget enabled state: %s",
                str(e),
                exc_info=True,
            )

    def _on_action_btn_clicked(self, action: ActionEvent) -> None:
        """Handle action button click events."""
        try:
            logger.debug(
                "_on_action_btn_clicked: Button '%s' clicked (prompt: '%s')",
                action.action_id,
                action.prompt.name,
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
                    reason,
                )

                self._show_warning_message(
                    "System not ready",
                    f"System is {status.lower()}. {reason.capitalize()}.",
                )
                return

            if not self._text_widget.input_text().strip():
                logger.debug(
                    "_on_action_btn_clicked: Action skipped - no input text",
                )
                self._show_warning_message(
                    "Nothing to process",
                    "The input text is empty. Please enter some text to process.",
                )
                return

            # Prepare task execution
            logger.debug(
                "_on_action_btn_clicked: Preparing task '%s' execution",
                action.action_id,
            )

            def closure() -> str:
                try:
                    logger.debug(
                        "_on_action_btn_clicked.closure: Executing task '%s'",
                        action.action_id,
                    )

                    # Build prompt parameters
                    prompt_parameters = {
                        PROMPT_PARAM_USER_TEXT: self._text_widget.input_text(),
                    }

                    if action.input_dropdown_item:
                        input_lang = action.input_dropdown_item()
                        logger.debug(
                            "_on_action_btn_clicked.closure: Using input language '%s'",
                            input_lang,
                        )
                        prompt_parameters[PROMPT_PARAM_INPUT_LANGUAGE] = input_lang

                    if action.output_dropdown_item:
                        output_lang = action.output_dropdown_item()
                        logger.debug(
                            "_on_action_btn_clicked.closure: Using output language '%s'",
                            output_lang,
                        )
                        prompt_parameters[PROMPT_PARAM_OUTPUT_LANGUAGE] = output_lang

                    # Create processing context
                    process_ctx = ProcessingContext(
                        user_prompt_id=action.prompt.id,
                        prompt_parameters=prompt_parameters,
                    )

                    logger.debug(
                        "_on_action_btn_clicked.closure: Processing context created - prompt_id=%s, params_count=%d",
                        process_ctx.user_prompt_id,
                        len(process_ctx.prompt_parameters),
                    )

                    return self._ctx.text_processing_service.process(process_ctx)
                except Exception as e:
                    logger.error(
                        "_on_action_btn_clicked.closure: Task execution failed: %s",
                        str(e),
                        exc_info=True,
                    )
                    raise

            # Submit task
            task = TaskInput(
                id=action.action_id,
                task_func=closure,
                on_task_finished=self._on_task_finished,
            )

            logger.debug(
                "_on_action_btn_clicked: Submitting task '%s' to task service",
                action.action_id,
            )
            self._ctx.task_service.submit_task(task)
        except Exception as e:
            logger.error(
                "_on_action_btn_clicked: Failed to handle action button click: %s",
                str(e),
                exc_info=True,
            )

    @staticmethod
    def _show_warning_message(title: str, message: str) -> None:
        """Show a warning message dialog."""
        try:
            msg_box = QMessageBox()
            msg_box.setWindowTitle(title)
            msg_box.setText(message)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.exec()
        except Exception as e:
            logger.error(
                "_show_warning_message: Failed to show warning message: %s",
                str(e),
                exc_info=True,
            )

    def _on_task_finished(self, task_result: TaskResult) -> None:
        """Handle task completion events."""
        try:
            if task_result.has_error:
                logger.error(
                    "_on_task_finished: Task '%s' failed with error: %s",
                    task_result.id,
                    task_result.error_message,
                    exc_info=task_result.exception,
                )

                self._show_error_message(
                    "Task Execution Failed",
                    f"Failed to execute task: {task_result.error_message}",
                )
            else:
                logger.debug(
                    "_on_task_finished: Task '%s' completed successfully",
                    task_result.id,
                )
                logger.debug(
                    "_on_task_finished: Setting output with %d characters",
                    len(task_result.task_result_content or ""),
                )
                self.set_output_text(str(task_result.task_result_content))
        except Exception as e:
            logger.error(
                "_on_task_finished: Failed to handle task completion: %s",
                str(e),
                exc_info=True,
            )

    @staticmethod
    def _show_error_message(title: str, message: str) -> None:
        """Show an error message dialog."""
        try:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(message)
            error_dialog.setWindowTitle(title)
            error_dialog.exec()
        except Exception as e:
            logger.error(
                "_show_error_message: Failed to show error message: %s",
                str(e),
                exc_info=True,
            )

    def set_output_text(self, text: str) -> None:
        """Set the output text in the text interaction area."""
        try:
            logger.debug(
                "set_output_text: Displaying %d characters in output area",
                len(text),
            )
            self._text_widget.set_output_text(text)
        except Exception as e:
            logger.error(
                "set_output_text: Failed to set output text: %s",
                str(e),
                exc_info=True,
            )
