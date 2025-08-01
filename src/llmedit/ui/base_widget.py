import logging

from PyQt6.QtWidgets import QWidget

from context import AppContext

logger = logging.getLogger(__name__)


class BaseWidget(QWidget):
    def __init__(self, ctx: AppContext, parent=None):
        super().__init__(parent)

        # Log initialization with context
        logger.debug(
            "__init__: Initializing BaseWidget (context type: %s)",
            type(ctx).__name__
        )

        self._ctx = ctx
        self._ctx.subscribe_settings_updated(self._on_settings_updated)
        self._ctx.task_service.subscribe_global_busy_state_changed(self._set_widget_enabled)

        # Log subscription setup
        logger.debug(
            "__init__: Subscribed to settings updates and task service (busy state tracking)"
        )

    def on_widget_initialization_complete(self) -> None:
        """Called when widget initialization is complete."""
        logger.debug("on_widget_initialization_complete: Initialization complete - updating settings")
        self._on_settings_updated()

    def _set_widget_enabled(self, running: bool) -> None:
        """Update widget enabled state based on task service status."""
        enabled = not running
        logger.debug(
            "_set_widget_enabled: Setting widget state to %s (running=%s)",
            "ENABLED" if enabled else "DISABLED",
            running
        )
        self.on_widgets_enabled_changed(enabled)

    def _on_settings_updated(self) -> None:
        """Handle settings update events from context."""
        is_ready = self._ctx.is_system_ready()
        logger.debug(
            "_on_settings_updated: System readiness status: %s",
            "READY" if is_ready else "NOT READY"
        )
        self.on_system_ready_changed(is_ready)
        self.on_settings_updated()

    def on_settings_updated(self) -> None:
        """Hook for subclasses to handle settings updates."""
        logger.debug("on_settings_updated: Base implementation (no action)")

    def on_system_ready_changed(self, is_ready: bool) -> None:
        """Hook for subclasses to handle system readiness changes."""
        logger.debug(
            "on_system_ready_changed: System state changed to %s",
            "READY" if is_ready else "NOT READY"
        )

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """Hook for subclasses to handle widget enabled state changes."""
        logger.debug(
            "on_widgets_enabled_changed: Widgets state changed to %s",
            "ENABLED" if enabled else "DISABLED"
        )
