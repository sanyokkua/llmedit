import logging
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from context import create_context
from theme.loader import load_stylesheet
from ui.main_window import MainWindow


def configure_logger(log_level: int = logging.INFO) -> None:
    """
    Configure the application's logging system.

    Args:
        log_level: The logging level to set (default: INFO).

    Raises:
        Exception: If logger configuration fails.

    Notes:
            Sets up a stream handler with a standardized format including timestamp,
            log level, logger name, and message. Disables propagation to prevent
            duplicate logs.
    """
    try:
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)-8s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.addHandler(handler)
        root_logger.propagate = False
        logging.info("Logger configured successfully")
        logging.debug("Debug logging is enabled")
    except Exception as e:
        print(f"Failed to configure logger: {e}", file=sys.stderr)
        raise


logger = logging.getLogger(__name__)

APP_ROOT_PATH = Path(__file__).resolve().parents[2]
"""
Base path for the application, pointing to the project root directory.
Derived from the location of this script file.
"""


def start_application() -> None:
    """
    Initialize and launch the application.

    Notes:
        Configures logging, creates the application context, sets up the UI with
        stylesheet, and starts the Qt event loop. Handles startup exceptions and
        performs proper shutdown.
    """
    try:
        configure_logger(log_level=logging.DEBUG)
        logger.info("Starting application")
        logger.debug(f"Application root path: {APP_ROOT_PATH}")

        ctx = create_context(APP_ROOT_PATH)
        app = QApplication(sys.argv)

        style = load_stylesheet(APP_ROOT_PATH)
        if style:
            app.setStyle("Fusion")
            app.setStyleSheet(style)

        window = MainWindow(ctx=ctx)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    """
    Entry point of the application.

    Handles startup, interruption, and unhandled exceptions.
    """
    try:
        start_application()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}", exc_info=True)
        sys.exit(1)
