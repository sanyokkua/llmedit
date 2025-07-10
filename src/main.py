import sys

from PyQt6.QtWidgets import QApplication

from src.app_context import AppContext, get_app_context
from ui.main_window import MainWindow


def start_application(app_context: AppContext):
    app = QApplication(sys.argv)
    window = MainWindow(app_context)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    app_context = get_app_context()
    start_application(app_context)
