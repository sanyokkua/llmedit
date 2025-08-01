import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy, QDialog
)

from context import AppContext
from ui.base_widget import BaseWidget
from ui.content.bottom_widget import BottomBarWidget
from ui.content.central_widget import CentralWidget
from ui.content.top_widget import TopBarWidget
from ui.settings.settings_dialog import SettingsDialog

logger = logging.getLogger(__name__)


class MainWidget(BaseWidget):
    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing main application widget")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._top_widget = TopBarWidget(ctx, self)
        self._center_widget = CentralWidget(ctx)
        self._bottom_widget = BottomBarWidget(self)

        logger.debug(
            "__init__: Created %d main components",
            sum(1 for _ in [self._top_widget, self._center_widget, self._bottom_widget])
        )

        layout.addWidget(self._top_widget)
        layout.addWidget(self._center_widget)
        layout.addWidget(self._bottom_widget)

        self.setLayout(layout)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self._top_widget.settings_clicked.connect(self._on_settings_clicked)
        logger.debug("__init__: Connected settings clicked signal")

        self.on_widget_initialization_complete()
        logger.debug(
            "__init__: Main widget initialized with %d layout elements",
            layout.count()
        )

    def _on_settings_clicked(self) -> None:
        """Handle settings button click event."""
        logger.debug("_on_settings_clicked: Opening settings dialog")

        settings = SettingsDialog(self._ctx)
        result = settings.exec()

        # If OK was clicked, process the settings
        if result == QDialog.DialogCode.Accepted:
            logger.debug("_on_settings_clicked: Settings dialog accepted - applying changes")
            self._ctx.emit_settings_updated()
        else:
            logger.debug("_on_settings_clicked: Settings dialog canceled")

    def on_settings_updated(self) -> None:
        """Handle settings update events."""
        settings = self._ctx.settings_service.get_settings_state()
        logger.debug(
            "on_settings_updated: Settings updated - provider=%s, model=%s",
            settings.llm_provider.value,
            settings.llm_model_name or "None"
        )

        self._bottom_widget.set_model(settings.llm_model_name)
        self._bottom_widget.set_provider(str(settings.llm_provider.value))

    def on_system_ready_changed(self, is_ready: bool) -> None:
        """Handle system readiness state changes."""
        status = "READY" if is_ready else "NOT READY"
        logger.debug(
            "on_system_ready_changed: System state changed to %s",
            status
        )

        if not is_ready:
            self._bottom_widget.set_initialization_status("No Model Selected")
        else:
            self._bottom_widget.set_initialization_status("")

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """Handle widget enabled state changes."""
        state = "ENABLED" if enabled else "DISABLED"
        logger.debug(
            "on_widgets_enabled_changed: Main widget state changed to %s",
            state
        )

        if enabled:
            self._bottom_widget.set_background_task_status("")
        else:
            self._bottom_widget.set_background_task_status("Running tasks...")
