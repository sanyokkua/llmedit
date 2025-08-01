import logging
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget)

from context import AppContext
from ui.base_widget import BaseWidget

logger = logging.getLogger(__name__)


class TopBarWidget(BaseWidget):
    """
    Top application bar widget containing the app title and settings button.

    Provides a consistent header with branding and access to application settings.
    Responds to system state changes by updating button availability.
    """

    settings_clicked = pyqtSignal()

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the top bar widget.

        Args:
            ctx: Application context for state management.
            parent: Optional parent widget.

        Raises:
            Exception: If widget initialization fails due to layout or connection errors.

        Notes:
            Creates a horizontal layout with app label on the left and settings button on the right.
            Connects settings button to the settings_clicked signal.
        """
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing top bar widget")

        try:
            self._app_label = QLabel("LLM Edit")
            self._settings_button = QPushButton("Settings")
            self._settings_button.clicked.connect(self.settings_clicked)

            logger.debug("__init__: Settings button initialized")

            self._configure_layout()
            logger.debug(
                "__init__: Top bar initialized with %d elements",
                self.layout().count() if self.layout() else 0,
            )
        except Exception as e:
            logger.error(
                "__init__: Failed to initialize top bar widget: %s",
                str(e),
                exc_info=True,
            )
            raise

        self.setObjectName("app-bar")
        self._app_label.setObjectName("app-bar-title-link")
        self._settings_button.setObjectName("app-bar-settings-button")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def _configure_layout(self) -> None:
        """
        Configure the widget's layout and sizing policy.

        Notes:
            Uses QHBoxLayout with fixed margins and spacing.
            Adds stretch between label and button to push button to the right.
            Sets horizontal expansion with fixed height.
        """
        try:
            logger.debug("_configure_layout: Setting up top bar layout")

            layout = QHBoxLayout()
            layout.setContentsMargins(12, 6, 12, 6)
            layout.setSpacing(16)

            layout.addWidget(self._app_label)
            layout.addStretch()
            layout.addWidget(self._settings_button)

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

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """
        Update settings button state based on system readiness and enabled flag.

        Args:
            enabled: The general widget enabled state from the context.

        Notes:
            Settings button remains enabled when system is not ready (to allow configuration).
            Only disabled when system is ready but explicitly told to disable.
        """
        try:
            system_ready = self._ctx.is_system_ready()
            button_state = "ENABLED" if (system_ready and enabled) else "DISABLED"

            logger.debug(
                "on_widgets_enabled_changed: Settings button set to %s (system_ready=%s, enabled=%s)",
                button_state,
                system_ready,
                enabled,
            )

            if not system_ready:
                self._settings_button.setEnabled(True)
            else:
                self._settings_button.setEnabled(enabled)
        except Exception as e:
            logger.error(
                "on_widgets_enabled_changed: Failed to change widget enabled state: %s",
                str(e),
                exc_info=True,
            )
