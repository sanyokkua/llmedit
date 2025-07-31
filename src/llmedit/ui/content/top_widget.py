from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy
)


class TopBarWidget(QWidget):
    settings_clicked = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._configure_layout()

    def _setup_ui(self) -> None:
        self._app_label = QLabel("LLM Edit")
        self._settings_button = QPushButton("Settings")
        self._settings_button.clicked.connect(self.settings_clicked)

    def _configure_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(16)

        layout.addWidget(self._app_label)
        layout.addStretch()  # Push settings button to right

        layout.addWidget(self._settings_button)

        self.setLayout(layout)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

    def set_settings_enabled(self, enabled: bool) -> None:
        self._settings_button.setEnabled(enabled)
