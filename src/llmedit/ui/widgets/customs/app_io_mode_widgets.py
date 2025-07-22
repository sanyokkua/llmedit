from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QComboBox

from llmedit.ui.widgets.customs.app_io_text_area_widgets import InputTextArea, OutputTextArea


class TranslatorIOWidget(QWidget):
    source_language_changed = pyqtSignal(str)
    target_language_changed = pyqtSignal(str)

    def __init__(self, languages: list[str]):
        super().__init__()
        self._input_app_text_area = InputTextArea()
        self._output_app_text_area = OutputTextArea()

        self._source_lang_combo = QComboBox(self)
        self._source_lang_combo.addItems(languages)

        self._target_lang_combo = QComboBox(self)
        self._target_lang_combo.addItems(languages)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self._input_app_text_area)
        input_layout.addWidget(self._source_lang_combo)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(0)
        input_container = QWidget()
        input_container.setLayout(input_layout)

        output_layout = QVBoxLayout()
        output_layout.addWidget(self._output_app_text_area)
        output_layout.addWidget(self._target_lang_combo)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(0)
        output_container = QWidget()
        output_container.setLayout(output_layout)

        widget_layout = QHBoxLayout()
        widget_layout.addWidget(input_container)
        widget_layout.addWidget(output_container)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setSpacing(0)
        self.setLayout(widget_layout)

    @property
    def input_text(self) -> str:
        return self._input_app_text_area.text_edit_value

    @property
    def output_text(self) -> str:
        return self._output_app_text_area.text_edit_value

    @property
    def source_language(self) -> str:
        return self._source_lang_combo.currentText().strip()

    @property
    def target_language(self) -> str:
        return self._target_lang_combo.currentText().strip()


class TextUtilsIOWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._input_app_text_area = InputTextArea()
        self._output_app_text_area = OutputTextArea()

        layout = QHBoxLayout()
        layout.addWidget(self._input_app_text_area)
        layout.addWidget(self._output_app_text_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    @property
    def input_text(self) -> str:
        return self._input_app_text_area.text_edit_value

    @property
    def output_text(self) -> str:
        return self._output_app_text_area.text_edit_value

    @output_text.setter
    def output_text(self, text: str) -> None:
        self._output_app_text_area.text_edit_value = text
