import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSizePolicy
)

logger = logging.getLogger(__name__)


class BottomBarWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        logger.debug("__init__: Initializing bottom status bar")
        self._setup_ui()
        self._configure_layout()
        logger.debug("__init__: Bottom status bar initialized with %d status elements", self.layout().count())

    def _setup_ui(self) -> None:
        """Initialize all UI components with default states."""
        logger.debug("_setup_ui: Creating status labels")

        # Status labels
        self._provider_label = QLabel("Provider: ")
        self._model_label = QLabel("Model: ")
        self._task_status_label = QLabel("Tasks: ")
        self._initialization_status_label = QLabel("")

        logger.debug(
            "_setup_ui: Created %d status labels",
            sum(1 for _ in
                [self._provider_label, self._model_label, self._task_status_label, self._initialization_status_label])
        )

    def _configure_layout(self) -> None:
        logger.debug("_configure_layout: Setting up layout")

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

        logger.debug(
            "_configure_layout: Layout configured with %d elements",
            layout.count()
        )

    def set_provider(self, provider: str) -> None:
        """Update provider status display."""
        logger.debug("set_provider: Setting provider to '%s'", provider)
        self._provider_label.setText(f"Provider: {provider}")

    def set_model(self, model: str) -> None:
        """Update model status display."""
        logger.debug("set_model: Setting model to '%s'", model)
        self._model_label.setText(f"Model: {model}")

    def set_background_task_status(self, status: str) -> None:
        """Update background task status display."""
        logger.debug("set_background_task_status: Setting task status to '%s'", status)
        self._task_status_label.setText(f"Tasks: {status}")

    def set_initialization_status(self, status: str) -> None:
        """Update initialization status display."""
        logger.debug("set_initialization_status: Setting initialization status to '%s'", status)
        self._initialization_status_label.setText(status)
