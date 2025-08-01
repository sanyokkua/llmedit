import logging
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QSizePolicy, QTabWidget, QWidget)

from context import AppContext
from core.models.enums.prompt import PromptCategory
from ui.content.tab_widgets.action_controls_widget import ActionControlsWidget, ActionEvent

logger = logging.getLogger(__name__)


class ActionTabsWidget(QTabWidget):
    """
    Tabbed widget organizing action buttons by category (Proofreading, Formatting, Translating).

    Each tab contains an ActionControlsWidget with prompts from a specific category.
    Emits signals when action buttons are clicked and disables itself during active tasks.
    """

    action_button_clicked = pyqtSignal(ActionEvent)

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the tab widget with categorized action controls.

        Args:
            ctx: Application context providing access to services and state.
            parent: Optional parent widget.

        Raises:
            Exception: If initialization fails due to service errors or invalid data.

        Notes:
            Creates three tabs: Proofreading, Formatting, and Translating.
            Translation tab includes input/output language dropdowns.
            Automatically subscribes to task service busy state to disable during processing.
        """
        super().__init__(parent)

        try:
            proofreading_prompts = ctx.prompt_service.get_prompts_by_category(PromptCategory.PROOFREAD)
            formatting_prompts = ctx.prompt_service.get_prompts_by_category(PromptCategory.FORMAT)
            translation_prompts = ctx.prompt_service.get_prompts_by_category(PromptCategory.TRANSLATE)

            logger.debug(
                "__init__: Initializing with %d proofreading, %d formatting, and %d translation prompts",
                len(proofreading_prompts),
                len(formatting_prompts),
                len(translation_prompts),
            )

            self.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )

            self._proofreading_tab = ActionControlsWidget(
                ctx=ctx,
                prompts=proofreading_prompts,
            )
            self._format_tab = ActionControlsWidget(
                ctx=ctx,
                prompts=formatting_prompts,
            )
            self._translate_tab = ActionControlsWidget(
                ctx=ctx,
                prompts=translation_prompts,
                input_dropdown_items=ctx.supported_languages_service.get_supported_translation_languages(),
                output_dropdown_items=ctx.supported_languages_service.get_supported_translation_languages(),
            )

            self.addTab(self._proofreading_tab, "Proofreading")
            self.addTab(self._format_tab, "Formatting")
            self.addTab(self._translate_tab, "Translating")

            self._proofreading_tab.button_clicked.connect(self._on_action_btn_clicked)
            self._format_tab.button_clicked.connect(self._on_action_btn_clicked)
            self._translate_tab.button_clicked.connect(self._on_action_btn_clicked)

            ctx.task_service.subscribe_global_busy_state_changed(self._set_widget_enabled)
            logger.debug(
                "__init__: Action tabs initialized - %d tabs created",
                self.count(),
            )
        except Exception as e:
            logger.error(
                "__init__: Failed to initialize ActionTabsWidget: %s",
                str(e),
                exc_info=True,
            )
            raise
        self.setObjectName("action-tabs-widget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def _set_widget_enabled(self, running: bool) -> None:
        """
        Update widget enabled state based on task execution status.

        Args:
            running: True if any task is currently running, False otherwise.

        Notes:
            Disables the entire widget when tasks are running to prevent concurrent actions.
            Called automatically via subscription to task service busy state changes.
        """
        try:
            enabled = not running
            self.setEnabled(enabled)
            logger.debug(
                "_set_widget_enabled: Widget state set to %s (running=%s)",
                "ENABLED" if enabled else "DISABLED",
                running,
            )
        except Exception as e:
            logger.error(
                "_set_widget_enabled: Failed to set widget enabled state: %s",
                str(e),
                exc_info=True,
            )

    def _on_action_btn_clicked(self, action: ActionEvent) -> None:
        """
        Handle action button click events from any tab.

        Args:
            action: The action event containing prompt and dropdown information.

        Notes:
            Forwards the event to the action_button_clicked signal.
            Logs the action ID and prompt name for debugging.
        """
        try:
            logger.debug(
                "_on_action_btn_clicked: Button '%s' clicked (prompt: '%s')",
                action.action_id,
                action.prompt.name,
            )
            self.action_button_clicked.emit(action)
        except Exception as e:
            logger.error(
                "_on_action_btn_clicked: Failed to handle button click: %s",
                str(e),
                exc_info=True,
            )
