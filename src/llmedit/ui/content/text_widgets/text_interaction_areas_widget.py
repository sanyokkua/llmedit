from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QLabel, QToolButton, QTextEdit, QSizePolicy, QHBoxLayout, QFrame, QVBoxLayout, QApplication
)


class TextInteractionAreasWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._input_header = QLabel("Input")
        self._input_header.setStyleSheet("font-weight: bold;")

        self._paste_button = QToolButton()
        self._paste_button.setText("📋 Paste")
        self._paste_button.setToolTip("Paste text from clipboard")
        self._paste_button.clicked.connect(self._paste_from_clipboard)

        self._input_text = QTextEdit()
        self._input_text.setAcceptRichText(False)
        self._input_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self._output_header = QLabel("Output")
        self._output_header.setStyleSheet("font-weight: bold;")

        self._copy_button = QToolButton()
        self._copy_button.setText("📋 Copy")
        self._copy_button.setToolTip("Copy text to clipboard")
        self._copy_button.clicked.connect(self._copy_to_clipboard)

        self._output_text = QTextEdit()
        self._output_text.setReadOnly(True)
        self._output_text.setAcceptRichText(False)
        self._output_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Input area layout
        input_layout = self._create_section_layout(
            self._input_header,
            self._paste_button,
            self._input_text
        )
        layout.addLayout(input_layout)

        # Output area layout
        output_layout = self._create_section_layout(
            self._output_header,
            self._copy_button,
            self._output_text
        )
        layout.addLayout(output_layout)

    def _create_section_layout(self, header: QLabel, action_button: QToolButton, text_area: QTextEdit) -> QVBoxLayout:
        section_layout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(4)

        # Header row
        header_layout = QHBoxLayout()
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(action_button)
        section_layout.addLayout(header_layout)

        # Text area
        section_layout.addWidget(text_area)

        return section_layout

    def _paste_from_clipboard(self) -> None:
        """Paste text from system clipboard into input area."""
        clipboard = QApplication.clipboard()

        if clipboard and clipboard.text():
            text = clipboard.text()
            self.set_input_text(text)

    def _copy_to_clipboard(self) -> None:
        """Copy text from output area to system clipboard."""
        clipboard = QApplication.clipboard()
        text = self.output_text()
        if text and clipboard:
            clipboard.setText(text)

    def set_input_text(self, text: str) -> None:
        self._input_text.setPlainText(text)

    def input_text(self) -> str:
        return self._input_text.toPlainText()

    def set_output_text(self, text: str) -> None:
        self._output_text.setPlainText(text)

    def output_text(self) -> str:
        return self._output_text.toPlainText()

    def set_enabled(self, enabled: bool) -> None:
        self._input_text.setEnabled(enabled)
        self._output_text.setEnabled(enabled and not self._output_text.isReadOnly())
        self._paste_button.setEnabled(enabled)
        self._copy_button.setEnabled(enabled)
