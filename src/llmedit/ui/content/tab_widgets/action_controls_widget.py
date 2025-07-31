from dataclasses import dataclass
from typing import List, Optional, Dict

from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QSizePolicy, QComboBox
)
from black.lines import Callable  # (you may need to replace this import)

from core.models.data_types import Prompt


@dataclass(frozen=True)
class ActionEvent:
    action_id: str
    prompt: Prompt
    input_dropdown_item: Optional[Callable[[], str]] = None
    output_dropdown_item: Optional[Callable[[], str]] = None


class ActionControlsWidget(QWidget):
    button_clicked = pyqtSignal(ActionEvent)

    def __init__(self,
                 prompts: List[Prompt],
                 input_dropdown_items: Optional[List[str]] = None,
                 output_dropdown_items: Optional[List[str]] = None,
                 parent=None):
        super().__init__(parent)

        self._prompts = prompts
        self._buttons: Dict[str, QPushButton] = {}

        # Top-level layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(6)

        # ─── DROPDOWNS (conditionally shown) ─────────────────────────
        show_dropdowns = bool(input_dropdown_items) and bool(output_dropdown_items)
        if show_dropdowns:
            dropdown_layout = QHBoxLayout()
            dropdown_layout.setSpacing(8)

            self._input_dropdown = QComboBox()
            self._input_dropdown.setEditable(True)
            self._input_dropdown.setPlaceholderText("Input")
            self._input_dropdown.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )
            for item in input_dropdown_items:
                self._input_dropdown.addItem(item)
            dropdown_layout.addWidget(self._input_dropdown)

            self._output_dropdown = QComboBox()
            self._output_dropdown.setEditable(True)
            self._output_dropdown.setPlaceholderText("Output")
            self._output_dropdown.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )
            for item in output_dropdown_items:
                self._output_dropdown.addItem(item)
            dropdown_layout.addWidget(self._output_dropdown)

            main_layout.addLayout(dropdown_layout)
        else:
            self._input_dropdown = None  # type: ignore
            self._output_dropdown = None  # type: ignore

        # ─── SCROLL AREA CONTAINER ───────────────────────────────────
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        main_layout.addWidget(self._scroll_area, stretch=1)

        # Container inside a scroll area, with a grid layout
        self._container = QWidget()
        self._grid = QGridLayout(self._container)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setSpacing(1)
        self._scroll_area.setWidget(self._container)

        # Create and register all buttons
        for prompt in self._prompts:
            btn = QPushButton(prompt.name)
            btn.setToolTip(prompt.description)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )
            btn.setProperty("action_id", prompt.id)
            event = ActionEvent(
                action_id=prompt.id,
                prompt=prompt,
                input_dropdown_item=self.input_dropdown_value,
                output_dropdown_item=self.output_dropdown_value,
            )
            btn.clicked.connect(lambda _, e=event: self.button_clicked.emit(e))
            self._buttons[prompt.id] = btn

        # Initial layout
        self._relayout_buttons()

    def input_dropdown_value(self) -> str:
        return self._input_dropdown.currentText() if self._input_dropdown else ""

    def output_dropdown_value(self) -> str:
        return self._output_dropdown.currentText() if self._output_dropdown else ""

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._relayout_buttons()

    def _relayout_buttons(self):
        # Clear existing widgets
        while self._grid.count() > 0:
            item = self._grid.takeAt(0)
            if item and item.widget():
                self._grid.removeWidget(item.widget())

        # Fixed number of columns
        cols = 4

        # Place buttons in grid, stretched to column width
        for idx, btn in enumerate(self._buttons.values()):
            row = idx // cols
            col = idx % cols
            self._grid.addWidget(btn, row, col)
            # Make sure each button expands to fill its column
            self._grid.setColumnStretch(col, 1)
