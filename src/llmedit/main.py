import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from core.abstracts.app_context import AppContext
from core.app_di_context import get_app_context
from ui.main_window import MainWindow

APP_ROOT_PATH = Path(__file__).resolve().parents[2]


def start_application(context: AppContext):
    app = QApplication(sys.argv)
    window = MainWindow(context)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    app_context = get_app_context(APP_ROOT_PATH)
    start_application(app_context)
