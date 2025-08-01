import logging

from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMainWindow, QApplication

from context import AppContext
from ui.main_widget import MainWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, ctx: AppContext):
        super().__init__()

        logger.debug("__init__: Initializing main application window")

        self._is_initialized = False
        self.main_control_widget = MainWidget(ctx=ctx)
        self.setCentralWidget(self.main_control_widget)

        logger.debug(
            "__init__: Main window initialized with central widget (default size: %dx%d)",
            800,
            600
        )

        self.setWindowTitle("LLM Edit")
        self.default_width = 800
        self.default_height = 600

    def center_on_screen(self):
        """Center the window on the appropriate screen."""
        logger.debug("center_on_screen: Attempting to center window on screen")

        screen = QApplication.screenAt(QPoint(self.x(), self.y()))
        if not screen:
            logger.debug("center_on_screen: No screen at window position - using primary screen")
            screen = QApplication.primaryScreen()

        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()

            logger.debug(
                "center_on_screen: Screen dimensions - width=%d, height=%d",
                screen_geometry.width(),
                screen_geometry.height()
            )

            x = (screen_geometry.width() - window_geometry.width()) // 2
            y = (screen_geometry.height() - window_geometry.height()) // 2

            logger.debug(
                "center_on_screen: Calculated position - x=%d, y=%d",
                x,
                y
            )

            self.move(max(0, x), max(0, y))
            logger.debug(
                "center_on_screen: Window positioned at (%d, %d)",
                self.x(),
                self.y()
            )
        else:
            logger.warning("center_on_screen: No screen available for positioning")

    def showEvent(self, event):
        """Handle window show event."""
        logger.debug("showEvent: Window show event triggered")

        if not self._is_initialized:
            logger.debug(
                "showEvent: First-time initialization - resizing to %dx%d",
                self.default_width,
                self.default_height
            )
            self.resize(self.default_width, self.default_height)
            self.center_on_screen()
            self._is_initialized = True
            logger.debug("showEvent: Initialization complete")
        else:
            logger.debug("showEvent: Window re-shown (already initialized)")

        super().showEvent(event)
