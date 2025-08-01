import logging
from typing import Optional

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QApplication, QMainWindow

from context import AppContext
from ui.main_widget import MainWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window managing the top-level UI and window lifecycle.

    Handles window initialization, centering on screen, and first-time setup.
    Contains the main widget as its central widget.
    """

    def __init__(self, ctx: AppContext):
        """
        Initialize the main window.

        Args:
            ctx: Application context for shared services and state.

        Notes:
            Sets up the main widget as central content and configures default window size.
            Initialization is deferred until showEvent to ensure proper display setup.
        """
        super().__init__()

        logger.debug("__init__: Initializing main application window")

        self._is_initialized = False
        self.main_control_widget = MainWidget(ctx=ctx)
        self.setCentralWidget(self.main_control_widget)

        logger.debug(
            "__init__: Main window initialized with central widget (default size: %dx%d)",
            800,
            600,
        )

        self.setWindowTitle("LLM Edit")
        self.default_width = 800
        self.default_height = 600

    def center_on_screen(self) -> None:
        """
        Center the window on the appropriate screen.

        Notes:
            Uses the screen at the current window position, falling back to primary screen.
            Calculates center position based on available screen geometry.
            Logs positioning calculations and handles errors gracefully.
        """
        logger.debug("center_on_screen: Attempting to center window on screen")

        try:
            screen: Optional[QScreen] = QApplication.screenAt(QPoint(self.x(), self.y()))
            if not screen:
                logger.debug("center_on_screen: No screen at window position - using primary screen")
                screen = QApplication.primaryScreen()

            if screen:
                screen_geometry = screen.availableGeometry()
                window_geometry = self.frameGeometry()

                logger.debug(
                    "center_on_screen: Screen dimensions - width=%d, height=%d",
                    screen_geometry.width(),
                    screen_geometry.height(),
                )

                x = (screen_geometry.width() - window_geometry.width()) // 2
                y = (screen_geometry.height() - window_geometry.height()) // 2

                logger.debug(
                    "center_on_screen: Calculated position - x=%d, y=%d",
                    x,
                    y,
                )

                self.move(max(0, x), max(0, y))
                logger.debug(
                    "center_on_screen: Window positioned at (%d, %d)",
                    self.x(),
                    self.y(),
                )
            else:
                logger.warning("center_on_screen: No screen available for positioning")
        except Exception as e:
            logger.error(
                "center_on_screen: Failed to center window on screen: %s",
                str(e),
                exc_info=True,
            )

    def showEvent(self, event) -> None:
        """
        Handle window show event for initialization.

        Args:
            event: The show event.

        Notes:
            On first show, resizes window to default dimensions and centers it.
            Sets initialization flag to prevent reinitialization on subsequent shows.
        """
        logger.debug("showEvent: Window show event triggered")

        try:
            if not self._is_initialized:
                logger.debug(
                    "showEvent: First-time initialization - resizing to %dx%d",
                    self.default_width,
                    self.default_height,
                )
                self.resize(self.default_width, self.default_height)
                self.center_on_screen()
                self._is_initialized = True
                logger.debug("showEvent: Initialization complete")
            else:
                logger.debug("showEvent: Window re-shown (already initialized)")
        except Exception as e:
            logger.error(
                "showEvent: Failed during window show event handling: %s",
                str(e),
                exc_info=True,
            )

        super().showEvent(event)
