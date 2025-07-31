from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSizePolicy
)


class BottomBarWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._configure_layout()

    def _setup_ui(self) -> None:
        """Initialize all UI components with default states."""
        # Status labels
        self._provider_label = QLabel("Provider: ")
        self._model_label = QLabel("Model: ")
        self._task_status_label = QLabel("Tasks: ")
        self._initialization_status_label = QLabel("")

    def _configure_layout(self) -> None:
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(16)

        # Add status labels
        layout.addWidget(self._provider_label)
        layout.addWidget(self._model_label)
        layout.addWidget(self._task_status_label)
        layout.addWidget(self._initialization_status_label)
        layout.addStretch()

        self.setLayout(layout)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

    def set_provider(self, provider: str) -> None:
        self._provider_label.setText(f"Provider: {provider}")

    def set_model(self, model: str) -> None:
        self._model_label.setText(f"Model: {model}")

    def set_background_task_status(self, status: str) -> None:
        self._task_status_label.setText(f"Tasks: {status}")

    def set_initialization_status(self, status: str) -> None:
        self._initialization_status_label.setText(status)
