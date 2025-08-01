import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget

from context import AppContext

logger = logging.getLogger(__name__)


class BaseWidget(QWidget):
    """
    Base widget class providing common functionality for all UI components.

    Automatically subscribes to application context events including settings updates
    and task service busy state changes. Provides hooks for subclasses to respond
    to system state changes.
    """

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None):
        """
        Initialize the base widget.

        Args:
            ctx: Application context for accessing services and state.
            parent: Optional parent widget.

        Notes:
            Subscribes to settings updates and task service busy state changes.
            Stores context reference for use by derived classes.
        """
        super().__init__(parent)

        logger.debug(
            "__init__: Initializing BaseWidget (context type: %s)",
            type(ctx).__name__,
        )

        self._ctx = ctx
        self._ctx.subscribe_settings_updated(self._on_settings_updated)
        self._ctx.task_service.subscribe_global_busy_state_changed(self._set_widget_enabled)

        logger.debug(
            "__init__: Subscribed to settings updates and task service (busy state tracking)",
        )

    def on_widget_initialization_complete(self) -> None:
        """
        Called when widget initialization is complete.

        Notes:
            Triggers an immediate settings update to synchronize with current state.
            Should be called by subclasses after their initialization is complete.
        """
        logger.debug("on_widget_initialization_complete: Initialization complete - updating settings")
        try:
            self._on_settings_updated()
        except Exception as e:
            logger.error(
                "on_widget_initialization_complete: Failed to update settings: %s",
                str(e),
                exc_info=True,
            )

    def _set_widget_enabled(self, running: bool) -> None:
        """
        Update widget enabled state based on task execution status.

        Args:
            running: True if any task is currently running, False otherwise.

        Notes:
            Called automatically when task service busy state changes.
            Delegates to on_widgets_enabled_changed hook.
        """
        enabled = not running
        logger.debug(
            "_set_widget_enabled: Setting widget state to %s (running=%s)",
            "ENABLED" if enabled else "DISABLED",
            running,
        )
        try:
            self.on_widgets_enabled_changed(enabled)
        except Exception as e:
            logger.error(
                "_set_widget_enabled: Failed to handle widget state change: %s",
                str(e),
                exc_info=True,
            )

    def _on_settings_updated(self) -> None:
        """
        Handle settings update events from the application context.

        Notes:
            Called when any setting changes. Updates system readiness state
            and notifies subclasses through hooks.
        """
        try:
            is_ready = self._ctx.is_system_ready()
            logger.debug(
                "_on_settings_updated: System readiness status: %s",
                "READY" if is_ready else "NOT READY",
            )
            self.on_system_ready_changed(is_ready)
            self.on_settings_updated()
        except Exception as e:
            logger.error(
                "_on_settings_updated: Failed to handle settings update: %s",
                str(e),
                exc_info=True,
            )

    def on_settings_updated(self) -> None:
        """
        Hook for subclasses to handle settings updates.

        Notes:
            Called when settings change. Base implementation does nothing.
            Subclasses should override to update their UI or behavior.
        """
        logger.debug("on_settings_updated: Base implementation (no action)")

    def on_system_ready_changed(self, is_ready: bool) -> None:
        """
        Hook for subclasses to handle changes in system readiness.

        Args:
            is_ready: True if system is ready for processing, False otherwise.

        Notes:
            Called when the system transitions between ready and not-ready states.
            Base implementation does nothing.
        """
        logger.debug(
            "on_system_ready_changed: System state changed to %s",
            "READY" if is_ready else "NOT READY",
        )

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        """
        Hook for subclasses to handle changes in widget enabled state.

        Args:
            enabled: True to enable widgets, False to disable.

        Notes:
            Called when the widget should be enabled/disabled (e.g., during processing).
            Base implementation does nothing.
        """
        logger.debug(
            "on_widgets_enabled_changed: Widgets state changed to %s",
            "ENABLED" if enabled else "DISABLED",
        )
