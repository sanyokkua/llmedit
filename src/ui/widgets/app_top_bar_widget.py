from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class AppTopBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        label = QLabel("LLM Edit", self)
        label.setStyleSheet("color: white; background-color: gray; padding: 10px;")

        layout.addWidget(label)
        self.setLayout(layout)
