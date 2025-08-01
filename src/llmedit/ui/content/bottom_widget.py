import logging
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy, QWidget)

logger = logging.getLogger(__name__)


class BottomBarWidget(QWidget):
    """
    Status bar widget displaying application state information at the bottom of the window.

    Shows current provider, model, task status, and initialization status in a horizontal layout.
    Designed to provide real-time feedback about the application's operational state.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the bottom status bar widget.

        Args:
            parent: Optional parent widget.

        Raises:
            Exception: If widget initialization fails due to layout or UI setup errors.

        Notes:
            Creates four status labels and arranges them in a horizontal layout with stretching.
        """
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
        self.setObjectName("bottom-bar")
        self._initialization_status_label.setObjectName("bottom-bar-initialization-status")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def _setup_ui(self) -> None:
        """
        Initialize all UI components with default states.

        Notes:
            Creates four QLabel instances for provider, model, task status, and initialization status.
            Labels are created with initial placeholder text.
        """
        try:
            logger.debug("_setup_ui: Creating status labels")

            self._provider_label = QLabel("Provider: ")
            self._model_label = QLabel("Model: ")
            self._task_status_label = QLabel("Tasks: ")
            self._initialization_status_label = QLabel("")

            label_count = 4
            logger.debug("_setup_ui: Created %d status labels", label_count)
        except Exception as e:
            logger.error(
                "_setup_ui: Failed to setup UI components: %s",
                str(e),
                exc_info=True,
            )
            raise

    def _configure_layout(self) -> None:
        """
        Configure the widget's layout and sizing policy.

        Notes:
            Uses QHBoxLayout with fixed spacing and margins.
            Adds a stretch spacer at the end to push labels to the left.
            Sets horizontal expansion with fixed height.
        """
        try:
            logger.debug("_configure_layout: Setting up layout")

            layout = QHBoxLayout()
            layout.setContentsMargins(8, 4, 8, 4)
            layout.setSpacing(16)

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
        """
        Update the displayed provider status.

        Args:
            provider: Name of the current LLM provider to display.

        Notes:
            Updates the provider label text in the format "Provider: {provider}".
        """
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
        """
        Update the displayed model status.

        Args:
            model: Name of the current model to display.

        Notes:
            Updates the model label text in the format "Model: {model}".
        """
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
        """
        Update the background task status display.

        Args:
            status: Text describing current task state (e.g., "Idle", "Processing").

        Notes:
            Updates the task status label in the format "Tasks: {status}".
        """
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
        """
        Update the initialization status display.

        Args:
            status: Text describing initialization state.

        Notes:
            Updates the initialization status label with the provided text.
            Can be used to show startup progress or errors.
        """
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
