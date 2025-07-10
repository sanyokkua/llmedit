from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QTextEdit, QPushButton, QApplication


class AppTextAreaWidget(QWidget):
    def __init__(self, header_text: str, btn_text: str, read_only: bool = False):
        super().__init__()
        self._text_edit = QTextEdit(self)
        self._text_edit.setReadOnly(read_only)
        self._functional_btn = QPushButton(btn_text, self)

        widget_layout = QVBoxLayout()
        widget_layout.addWidget(QLabel(header_text))
        widget_layout.addWidget(self._functional_btn)
        widget_layout.addWidget(self._text_edit)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(10)
        self.setLayout(widget_layout)

    @property
    def text_edit_value(self) -> str:
        return self._text_edit.toPlainText().strip()

    @text_edit_value.setter
    def text_edit_value(self, text: str):
        self._text_edit.setPlainText(text.strip())


class InputTextArea(AppTextAreaWidget):
    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__("Input", "Paste from Clipboard")
        self._functional_btn.clicked.connect(self._paste_from_clipboard)
        self._text_edit.textChanged.connect(lambda: self.text_changed.emit(self.text_edit_value))

    def _paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        if clipboard is not None and clipboard.text():
            self._text_edit.clear()
            self._text_edit.insertPlainText(clipboard.text().strip())


class OutputTextArea(AppTextAreaWidget):
    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__("Output", "Copy to Clipboard", True)
        self._functional_btn.clicked.connect(self._copy_to_clipboard)
        self._text_edit.textChanged.connect(lambda: self.text_changed.emit(self.text_edit_value))

    def _copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(self._text_edit.toPlainText())
