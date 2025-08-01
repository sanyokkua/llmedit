import logging
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy
)

from context import AppContext
from ui.base_widget import BaseWidget

logger = logging.getLogger(__name__)


class TopBarWidget(BaseWidget):
    settings_clicked = pyqtSignal()

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing top bar widget")

        self._app_label = QLabel("LLM Edit")
        self._settings_button = QPushButton("Settings")
        self._settings_button.clicked.connect(self.settings_clicked)

        logger.debug("__init__: Settings button initialized")

        self._configure_layout()
        logger.debug(
            "__init__: Top bar initialized with %d elements",
            self.layout().count() if self.layout() else 0
        )

    def _configure_layout(self) -> None:
        """Configure the layout for the top bar."""
        logger.debug("_configure_layout: Setting up top bar layout")

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

        logger.debug(
            "_configure_layout: Layout configured with %d elements",
            layout.count()
        )

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """Update settings button state based on system readiness."""
        system_ready = self._ctx.is_system_ready()
        button_state = "ENABLED" if (system_ready and enabled) else "DISABLED"

        logger.debug(
            "on_widgets_enabled_changed: Settings button set to %s (system_ready=%s, enabled=%s)",
            button_state,
            system_ready,
            enabled
        )

        if not system_ready:
            self._settings_button.setEnabled(True)
        else:
            self._settings_button.setEnabled(enabled)
