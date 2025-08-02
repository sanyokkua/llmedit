import logging
from dataclasses import dataclass
from typing import Callable as CallableType, Dict, List, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from llmedit.context import AppContext
from llmedit.core.models.data_types import Prompt
from llmedit.ui.base_widget import BaseWidget

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ActionEvent:
    """
    Immutable data class representing a button click event in the action controls.

    Carries the action ID, associated prompt, and optional callbacks for retrieving
    dropdown values at event time.
    """
    action_id: str
    prompt: Prompt
    input_dropdown_item: Optional[CallableType[[], str]] = None
    output_dropdown_item: Optional[CallableType[[], str]] = None


class ActionControlsWidget(BaseWidget):
    """
    Widget displaying a grid of action buttons with optional input/output dropdowns.

    Dynamically arranges prompt-based action buttons in a responsive grid layout.
    Emits signals when buttons are clicked, including dropdown values if present.
    """

    button_clicked = pyqtSignal(ActionEvent)

    def __init__(
        self,
        ctx: AppContext,
        prompts: List[Prompt],
        input_dropdown_items: Optional[List[str]] = None,
        output_dropdown_items: Optional[List[str]] = None,
        parent=None,
    ):
        """
        Initialize the action controls widget.

        Args:
            ctx: Application context for shared services and state.
            prompts: List of prompts to create action buttons for.
            input_dropdown_items: Optional list of items for input dropdown.
            output_dropdown_items: Optional list of items for output dropdown.
            parent: Optional parent widget.

        Notes:
            Dropdowns are only shown if both input and output items are provided.
            Buttons are arranged in a 4-column grid that relayouts on resize.
        """
        super().__init__(ctx, parent)

        logger.debug(
            "__init__: Initializing with %d prompts, dropdowns=%s",
            len(prompts),
            "enabled" if (input_dropdown_items and output_dropdown_items) else "disabled",
        )

        self._prompts = prompts
        self._buttons: Dict[str, QPushButton] = { }

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(6)

        show_dropdowns = bool(input_dropdown_items) and bool(output_dropdown_items)
        if show_dropdowns:
            logger.debug(
                "__init__: Adding dropdowns with %d input and %d output items",
                len(input_dropdown_items or []),
                len(output_dropdown_items or []),
            )

            dropdown_layout = QHBoxLayout()
            dropdown_layout.setSpacing(8)

            self._input_dropdown = QComboBox()
            self._input_dropdown.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )
            for item in input_dropdown_items or []:
                self._input_dropdown.addItem(item)
            self._input_dropdown.setCurrentText(ctx.settings_service.get_source_language())
            dropdown_layout.addWidget(self._input_dropdown)

            self._output_dropdown = QComboBox()
            self._output_dropdown.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )
            for item in output_dropdown_items or []:
                self._output_dropdown.addItem(item)
            self._output_dropdown.setCurrentText(ctx.settings_service.get_target_language())
            dropdown_layout.addWidget(self._output_dropdown)

            main_layout.addLayout(dropdown_layout)
        else:
            logger.debug("__init__: Dropdowns not needed (missing items)")
            self._input_dropdown = None  # type: ignore
            self._output_dropdown = None  # type: ignore

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        main_layout.addWidget(self._scroll_area, stretch=1)

        self._container = QWidget()
        self._grid = QGridLayout(self._container)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setWidget(self._container)

        logger.debug("__init__: Creating %d action buttons", len(prompts))
        for prompt in self._prompts:
            btn = QPushButton(prompt.name)
            btn.setToolTip(prompt.description)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )
            btn.setProperty("action_id", prompt.id)
            event = ActionEvent(
                action_id=prompt.id,
                prompt=prompt,
                input_dropdown_item=self.input_dropdown_value,
                output_dropdown_item=self.output_dropdown_value,
            )
            btn.clicked.connect(lambda checked, e=event: self.button_clicked.emit(e))
            self._buttons[prompt.id] = btn
        self.setObjectName("actionControlsWidget")
        self._scroll_area.setObjectName("actionControlsWidgetScrollArea")
        if self._input_dropdown:
            self._input_dropdown.setObjectName("actionControlsWidgetDropdownInput")
        if self._output_dropdown:
            self._output_dropdown.setObjectName("actionControlsWidgetDropdownOutput")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._relayout_buttons()

    def input_dropdown_value(self) -> str:
        """
        Get the current text from the input dropdown.

        Returns:
            Current text of input dropdown, or empty string if not available.

        Notes:
            Used by ActionEvent to capture dropdown state at button click time.
        """
        try:
            value = self._input_dropdown.currentText() if self._input_dropdown else ""
            logger.debug("input_dropdown_value: Returning '%s'", value)
            return value
        except Exception as e:
            logger.error(
                "input_dropdown_value: Failed to get input dropdown value: %s",
                str(e),
                exc_info=True,
            )
            return ""

    def output_dropdown_value(self) -> str:
        """
        Get the current text from the output dropdown.

        Returns:
            Current text of output dropdown, or empty string if not available.

        Notes:
            Used by ActionEvent to capture dropdown state at button click time.
        """
        try:
            value = self._output_dropdown.currentText() if self._output_dropdown else ""
            logger.debug("output_dropdown_value: Returning '%s'", value)
            return value
        except Exception as e:
            logger.error(
                "output_dropdown_value: Failed to get output dropdown value: %s",
                str(e),
                exc_info=True,
            )
            return ""

    def resizeEvent(self, event):
        """
        Handle widget resize events by relayouting buttons.

        Args:
            event: The resize event.

        Notes:
            Calls parent implementation and triggers grid rearrangement.
        """
        try:
            super().resizeEvent(event)
            logger.debug("resizeEvent: Widget resized to %dx%d", self.width(), self.height())
            self._relayout_buttons()
        except Exception as e:
            logger.error(
                "resizeEvent: Failed to handle resize event: %s",
                str(e),
                exc_info=True,
            )

    def _relayout_buttons(self):
        """
        Rearrange buttons in the grid layout.

        Notes:
            Clears existing layout and arranges buttons in a 4-column grid.
            Each column is stretched equally. Logs the final grid dimensions.
        """
        try:
            logger.debug("_relayout_buttons: Rearranging %d buttons", len(self._buttons))

            while self._grid.count() > 0:
                item = self._grid.takeAt(0)
                if item and item.widget():
                    self._grid.removeWidget(item.widget())

            cols = 3 if len(self._buttons) % 3 == 0 else 2

            for idx, btn in enumerate(self._buttons.values()):
                row = idx // cols
                col = idx % cols
                self._grid.addWidget(btn, row, col)
                self._grid.setColumnStretch(col, 1)

            logger.debug(
                "_relayout_buttons: Arranged into %d rows (%d columns)",
                (len(self._buttons) + cols - 1) // cols,
                cols,
            )
        except Exception as e:
            logger.error(
                "_relayout_buttons: Failed to relayout buttons: %s",
                str(e),
                exc_info=True,
            )

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """
        Update the enabled state of all contained widgets.

        Args:
            enabled: True to enable all widgets, False to disable.

        Notes:
            Affects buttons and dropdowns (if present). Used to prevent interaction
            during processing or when context is not ready.
        """
        try:
            state = "ENABLED" if enabled else "DISABLED"
            logger.debug("on_widgets_enabled_changed: Setting widget state to %s", state)

            buttons = self._buttons.values()
            for btn in buttons:
                btn.setEnabled(enabled)
            if self._input_dropdown:
                self._input_dropdown.setEnabled(enabled)
            if self._output_dropdown:
                self._output_dropdown.setEnabled(enabled)
        except Exception as e:
            logger.error(
                "on_widgets_enabled_changed: Failed to change widget enabled state: %s",
                str(e),
                exc_info=True,
            )
