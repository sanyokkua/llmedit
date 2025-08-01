import logging
from typing import Optional

from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy, QWidget)

logger = logging.getLogger(__name__)


class BottomBarWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        logger.debug("__init__: Initializing bottom status bar")

        try:
            self._setup_ui()
            self._configure_layout()
            logger.debug("__init__: Bottom status bar initialized with %d status elements", self.layout().count())
        except Exception as e:
            logger.error(
                "__init__: Failed to initialize bottom status bar: %s",
                str(e),
                exc_info=True,
            )
            raise

    def _setup_ui(self) -> None:
        """Initialize all UI components with default states."""
        try:
            logger.debug("_setup_ui: Creating status labels")

            # Status labels
            self._provider_label = QLabel("Provider: ")
            self._model_label = QLabel("Model: ")
            self._task_status_label = QLabel("Tasks: ")
            self._initialization_status_label = QLabel("")

            label_list = [
                self._provider_label,
                self._model_label,
                self._task_status_label,
                self._initialization_status_label
            ]
            label_count = sum(1 for _ in label_list)
            logger.debug("_setup_ui: Created %d status labels", label_count)
        except Exception as e:
            logger.error(
                "_setup_ui: Failed to setup UI components: %s",
                str(e),
                exc_info=True,
            )
            raise

    def _configure_layout(self) -> None:
        try:
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
                QSizePolicy.Policy.Fixed,
            )

            logger.debug(
                "_configure_layout: Layout configured with %d elements",
                layout.count(),
            )
        except Exception as e:
            logger.error(
                "_configure_layout: Failed to configure layout: %s",
                str(e),
                exc_info=True,
            )
            raise

    def set_provider(self, provider: str) -> None:
        """Update provider status display."""
        try:
            logger.debug("set_provider: Setting provider to '%s'", provider)
            self._provider_label.setText(f"Provider: {provider}")
        except Exception as e:
            logger.error(
                "set_provider: Failed to set provider to '%s': %s",
                provider,
                str(e),
                exc_info=True,
            )

    def set_model(self, model: str) -> None:
        """Update model status display."""
        try:
            logger.debug("set_model: Setting model to '%s'", model)
            self._model_label.setText(f"Model: {model}")
        except Exception as e:
            logger.error(
                "set_model: Failed to set model to '%s': %s",
                model,
                str(e),
                exc_info=True,
            )

    def set_background_task_status(self, status: str) -> None:
        """Update the background task status display."""
        try:
            logger.debug("set_background_task_status: Setting task status to '%s'", status)
            self._task_status_label.setText(f"Tasks: {status}")
        except Exception as e:
            logger.error(
                "set_background_task_status: Failed to set task status to '%s': %s",
                status,
                str(e),
                exc_info=True,
            )

    def set_initialization_status(self, status: str) -> None:
        """Update initialization status display."""
        try:
            logger.debug("set_initialization_status: Setting initialization status to '%s'", status)
            self._initialization_status_label.setText(status)
        except Exception as e:
            logger.error(
                "set_initialization_status: Failed to set initialization status to '%s': %s",
                status,
                str(e),
                exc_info=True,
            )
