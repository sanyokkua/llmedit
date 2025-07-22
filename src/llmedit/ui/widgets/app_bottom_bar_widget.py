from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class AppBottomBarWidget(QWidget):
    def __init__(self, status_text="Ready", llm_name="", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 1)
        layout.setSpacing(1)
        self.status_text = status_text
        self.llm_name = llm_name
        self.status_label = QLabel(f"Status: \"{self.status_text}\"", self)
        self.llm_label = QLabel(f"LLM loaded: {self.llm_name}", self)

        # Set styles to match the mockup
        self.status_label.setStyleSheet("padding-right: 0px;")
        layout.addWidget(self.status_label)
        layout.addStretch()
        layout.addWidget(self.llm_label)

        self.setLayout(layout)

    def update_status(self, new_status):
        self.status_text = new_status
        if self.status_label is not None:
            self.status_label.setText(f"Status: \"{new_status}\"")

    def update_llm_name(self, new_llm_name):
        self.llm_name = new_llm_name
        if self.llm_label is not None:
            self.llm_label.setText(f"LLM loaded: {new_llm_name}")
