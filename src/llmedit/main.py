import logging
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from context import create_context
from ui.main_window import MainWindow


def configure_logger(log_level: int = logging.INFO) -> None:
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)-8s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    root_logger.propagate = False
    logging.info("Logger configured successfully")
    logging.debug("Debug logging is enabled")


logger = logging.getLogger(__name__)

APP_ROOT_PATH = Path(__file__).resolve().parents[2]


def start_application():
    configure_logger(log_level=logging.DEBUG)
    logger.info("Starting application")
    logger.debug(f"Application root path: {APP_ROOT_PATH}")
    ctx = create_context(APP_ROOT_PATH)
    # testing(ctx)
    app = QApplication(sys.argv)
    window = MainWindow(ctx=ctx)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    start_application()
