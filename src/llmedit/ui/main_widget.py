import logging
from typing import Optional

from PyQt6.QtWidgets import (QDialog, QSizePolicy, QVBoxLayout, QWidget)
from PyQt6.QtCore import Qt
from llmedit.context import AppContext
from llmedit.ui.base_widget import BaseWidget
from llmedit.ui.content.bottom_widget import BottomBarWidget
from llmedit.ui.content.central_widget import CentralWidget
from llmedit.ui.content.top_widget import TopBarWidget
from llmedit.ui.settings.settings_dialog import SettingsDialog

logger = logging.getLogger(__name__)


class MainWidget(BaseWidget):
    """
    Main application widget composing the complete UI layout.

    Orchestrates the top, central, and bottom UI components. Handles settings
    dialog interaction and updates status displays based on system state changes.
    """

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the main widget.

        Args:
            ctx: Application context providing access to services and state.
            parent: Optional parent widget.

        Notes:
            Creates and arranges the three main UI components (top, center, bottom).
            Connects the settings button to dialog opening.
            Calls initialization complete to trigger initial state updates.
        """
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
            sum(1 for _ in [self._top_widget, self._center_widget, self._bottom_widget]),
        )

        layout.addWidget(self._top_widget)
        layout.addWidget(self._center_widget)
        layout.addWidget(self._bottom_widget)

        self.setLayout(layout)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self._top_widget.settings_clicked.connect(self._on_settings_clicked)
        logger.debug("__init__: Connected settings clicked signal")

        self.on_widget_initialization_complete()
        logger.debug(
            "__init__: Main widget initialized with %d layout elements",
            layout.count(),
        )
        self.setObjectName("mainWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def _on_settings_clicked(self) -> None:
        """
        Handle settings button click by opening the settings dialog.

        Notes:
            Creates a SettingsDialog, executes it modally, and emits settings
            updated signal if changes were accepted. Uses context manager pattern
            for proper cleanup.
        """
        logger.debug("_on_settings_clicked: Opening settings dialog")

        settings_dialog = None
        try:
            settings_dialog = SettingsDialog(self._ctx)
            result = settings_dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                logger.debug("_on_settings_clicked: Settings dialog accepted - applying changes")
                self._ctx.emit_settings_updated()
            else:
                logger.debug("_on_settings_clicked: Settings dialog canceled")
        except Exception as e:
            logger.error(
                "_on_settings_clicked: Failed to open settings dialog: %s",
                str(e),
                exc_info=True,
            )
        finally:
            if settings_dialog:
                settings_dialog.deleteLater()

    def on_settings_updated(self) -> None:
        """
        Handle settings update events from the application context.

        Notes:
            Updates the bottom bar with current provider and model information.
            Called when any setting changes.
        """
        try:
            settings = self._ctx.settings_service.get_settings_state()
            logger.debug(
                "on_settings_updated: Settings updated - provider=%s, model=%s",
                settings.llm_provider.value,
                settings.llm_model_name or "None",
            )

            self._bottom_widget.set_model(settings.llm_model_name)
            self._bottom_widget.set_provider(str(settings.llm_provider.value))
        except Exception as e:
            logger.error(
                "on_settings_updated: Failed to update settings display: %s",
                str(e),
                exc_info=True,
            )

    def on_system_ready_changed(self, is_ready: bool) -> None:
        """
        Handle changes in system readiness state.

        Args:
            is_ready: True if system is ready for processing, False otherwise.

        Notes:
            Updates the bottom bar initialization status message accordingly.
        """
        try:
            status = "READY" if is_ready else "NOT READY"
            logger.debug(
                "on_system_ready_changed: System state changed to %s",
                status,
            )

            if not is_ready:
                self._bottom_widget.set_initialization_status("No Model Selected")
            else:
                self._bottom_widget.set_initialization_status("")
        except Exception as e:
            logger.error(
                "on_system_ready_changed: Failed to update system readiness display: %s",
                str(e),
                exc_info=True,
            )

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """
        Handle changes in widget enabled state.

        Args:
            enabled: True to enable widgets, False to disable.

        Notes:
            Updates the bottom bar task status message to reflect processing state.
        """
        try:
            state = "ENABLED" if enabled else "DISABLED"
            logger.debug(
                "on_widgets_enabled_changed: Main widget state changed to %s",
                state,
            )

            if enabled:
                self._bottom_widget.set_background_task_status("")
            else:
                self._bottom_widget.set_background_task_status("Running tasks...")
        except Exception as e:
            logger.error(
                "on_widgets_enabled_changed: Failed to update widget enabled state display: %s",
                str(e),
                exc_info=True,
            )
