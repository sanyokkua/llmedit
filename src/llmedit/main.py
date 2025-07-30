import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication


APP_ROOT_PATH = Path(__file__).resolve().parents[2]


def start_application():
    app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    start_application()
