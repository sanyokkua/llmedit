from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMainWindow, QApplication

from context import AppContext
from ui.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, ctx: AppContext):
        super().__init__()
        self._is_initialized = False
        self.main_control_widget = MainWidget(ctx=ctx)
        self.setCentralWidget(self.main_control_widget)

        self.setWindowTitle("LLM Edit")
        self.default_width = 800
        self.default_height = 600


    def center_on_screen(self):
        screen = QApplication.screenAt(QPoint(self.x(), self.y()))
        if not screen:
            screen = QApplication.primaryScreen()

        if screen:
            screen_geometry = screen.availableGeometry()
            window_geometry = self.frameGeometry()

            x = (screen_geometry.width() - window_geometry.width()) // 2
            y = (screen_geometry.height() - window_geometry.height()) // 2

            self.move(max(0, x), max(0, y))

    def showEvent(self, event):
        if not self._is_initialized:
            self.resize(self.default_width, self.default_height)
            self.center_on_screen()
            self._is_initialized = True
        super().showEvent(event)
