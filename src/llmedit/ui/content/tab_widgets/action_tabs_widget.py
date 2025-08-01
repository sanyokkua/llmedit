import logging
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QSizePolicy, QTabWidget, QWidget)

from context import AppContext
from core.models.enums.prompt import PromptCategory
from ui.content.tab_widgets.action_controls_widget import ActionControlsWidget, ActionEvent

logger = logging.getLogger(__name__)


class ActionTabsWidget(QTabWidget):
    action_button_clicked = pyqtSignal(ActionEvent)

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        try:
            # Log initialization with key metrics
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

    def _set_widget_enabled(self, running: bool) -> None:
        """Update widget state based on task service busy status."""
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
        """Handle action button click events."""
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
