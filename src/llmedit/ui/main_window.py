from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QMainWindow, QApplication

from core.abstracts.app_context import AppContext
from llmedit.ui.widgets.app_main_content_widget import AppMainContentWidget


class MainWindow(QMainWindow):
    def __init__(self, app_context: AppContext):
        super().__init__()
        self.main_control_widget = AppMainContentWidget(app_context)
        self.setCentralWidget(self.main_control_widget)

        layout = self.layout()
        if layout is not None:
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

        self.setWindowTitle("LLM Edit")
        self.default_width = 800
        self.default_height = 600

    def center_on_screen(self):
        primary_screen = QApplication.primaryScreen()
        if primary_screen is not None:
            screen_geometry = primary_screen.availableGeometry()
            window_size = self.frameSize()

            x = (screen_geometry.width() - window_size.width()) // 2
            y = (screen_geometry.height() - window_size.height()) // 2

            self.move(QPoint(x, y))

    def show(self):
        # Set the default size first
        self.resize(self.default_width, self.default_height)
        # Then center the window
        self.center_on_screen()
        super().show()
