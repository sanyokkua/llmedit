import logging
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from context import AppContext
from ui.base_widget import BaseWidget

logger = logging.getLogger(__name__)


class TextInteractionAreasWidget(BaseWidget):
    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing text interaction areas")

        try:
            self._input_header = QLabel("Input")
            self._input_header.setStyleSheet("font-weight: bold;")

            self._paste_button = QToolButton()
            self._paste_button.setText("📋 Paste")
            self._paste_button.setToolTip("Paste text from clipboard")
            self._paste_button.clicked.connect(self._paste_from_clipboard)
            logger.debug("__init__: Paste button initialized")

            self._input_text = QTextEdit()
            self._input_text.setAcceptRichText(False)
            self._input_text.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            logger.debug("__init__: Input text area initialized")

            self._output_header = QLabel("Output")
            self._output_header.setStyleSheet("font-weight: bold;")

            self._copy_button = QToolButton()
            self._copy_button.setText("📋 Copy")
            self._copy_button.setToolTip("Copy text to clipboard")
            self._copy_button.clicked.connect(self._copy_to_clipboard)
            logger.debug("__init__: Copy button initialized")

            self._output_text = QTextEdit()
            self._output_text.setReadOnly(True)
            self._output_text.setAcceptRichText(False)
            self._output_text.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
            logger.debug("__init__: Output text area initialized (read-only)")

            layout = QHBoxLayout(self)
            layout.setContentsMargins(8, 8, 8, 8)
            layout.setSpacing(8)

            # Input area layout
            input_layout = self._create_section_layout(
                self._input_header,
                self._paste_button,
                self._input_text,
            )
            layout.addLayout(input_layout)

            # Output area layout
            output_layout = self._create_section_layout(
                self._output_header,
                self._copy_button,
                self._output_text,
            )
            layout.addLayout(output_layout)

            logger.debug(
                "__init__: Text interaction areas initialized with %d sections",
                layout.count(),
            )
        except Exception as e:
            logger.error(
                "__init__: Failed to initialize text interaction areas: %s",
                str(e),
                exc_info=True,
            )
            raise

    @staticmethod
    def _create_section_layout(header: QLabel, action_button: QToolButton, text_area: QTextEdit) -> QVBoxLayout:
        try:
            logger.debug("_create_section_layout: Creating text section")

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

            logger.debug(
                "_create_section_layout: Section created with %s header",
                header.text(),
            )
            return section_layout
        except Exception as e:
            logger.error(
                "_create_section_layout: Failed to create section layout: %s",
                str(e),
                exc_info=True,
            )
            raise

    def _paste_from_clipboard(self) -> None:
        """Paste text from system clipboard into input area."""
        try:
            logger.debug("_paste_from_clipboard: Paste operation started")

            clipboard = QApplication.clipboard()
            if clipboard and clipboard.text():
                text = clipboard.text()
                logger.debug(
                    "_paste_from_clipboard: Pasting %d characters from clipboard",
                    len(text),
                )
                self.set_input_text(text)
            else:
                logger.debug("_paste_from_clipboard: Clipboard is empty")
        except Exception as e:
            logger.error(
                "_paste_from_clipboard: Failed to paste from clipboard: %s",
                str(e),
                exc_info=True,
            )

    def _copy_to_clipboard(self) -> None:
        """Copy text from output area to system clipboard."""
        try:
            logger.debug("_copy_to_clipboard: Copy operation started")

            clipboard = QApplication.clipboard()
            text = self.output_text()
            if text and clipboard:
                logger.debug(
                    "_copy_to_clipboard: Copying %d characters to clipboard",
                    len(text),
                )
                clipboard.setText(text)
            else:
                logger.debug("_copy_to_clipboard: No text to copy")
        except Exception as e:
            logger.error(
                "_copy_to_clipboard: Failed to copy to clipboard: %s",
                str(e),
                exc_info=True,
            )

    def set_input_text(self, text: str) -> None:
        try:
            logger.debug(
                "set_input_text: Setting %d characters in input area",
                len(text),
            )
            self._input_text.setPlainText(text)
        except Exception as e:
            logger.error(
                "set_input_text: Failed to set input text: %s",
                str(e),
                exc_info=True,
            )

    def input_text(self) -> str:
        try:
            text = self._input_text.toPlainText()
            logger.debug(
                "input_text: Returning %d characters from input area",
                len(text),
            )
            return text
        except Exception as e:
            logger.error(
                "input_text: Failed to get input text: %s",
                str(e),
                exc_info=True,
            )
            return ""

    def set_output_text(self, text: str) -> None:
        try:
            logger.debug(
                "set_output_text: Setting %d characters in output area",
                len(text),
            )
            self._output_text.setPlainText(text)
        except Exception as e:
            logger.error(
                "set_output_text: Failed to set output text: %s",
                str(e),
                exc_info=True,
            )

    def output_text(self) -> str:
        try:
            text = self._output_text.toPlainText()
            logger.debug(
                "output_text: Returning %d characters from output area",
                len(text),
            )
            return text
        except Exception as e:
            logger.error(
                "output_text: Failed to get output text: %s",
                str(e),
                exc_info=True,
            )
            return ""

    def on_widgets_enabled_changed(self, enabled: bool) -> None:
        try:
            state = "ENABLED" if enabled else "DISABLED"
            logger.debug(
                "on_widgets_enabled_changed: Setting text areas to %s",
                state,
            )

            self._input_text.setEnabled(enabled)
            self._output_text.setEnabled(enabled)
            self._paste_button.setEnabled(enabled)
            self._copy_button.setEnabled(enabled)
        except Exception as e:
            logger.error(
                "on_widgets_enabled_changed: Failed to change widget enabled state: %s",
                str(e),
                exc_info=True,
            )
