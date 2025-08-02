import logging
from typing import Optional

from PyQt6.QtCore import Qt
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

from llmedit.context import AppContext
from llmedit.ui.base_widget import BaseWidget

logger = logging.getLogger(__name__)


class TextInteractionAreasWidget(BaseWidget):
    """
    Widget providing side-by-side input and output text areas with clipboard controls.

    Features include:
    - Input area with paste button to import text from clipboard
    - Output area with copy button to export text to clipboard
    - Read-only output display with rich text disabled
    - Responsive layout with labeled sections
    """

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the text interaction widget.

        Args:
            ctx: Application context for shared services.
            parent: Optional parent widget.

        Raises:
            Exception: If widget initialization fails due to Qt errors or resource issues.

        Notes:
            Creates two sections (Input and Output) each with header, action button,
            and text area. Connects clipboard buttons to their respective handlers.
        """
        super().__init__(ctx, parent)

        logger.debug("__init__: Initializing text interaction areas")

        try:
            self._input_header = QLabel("Input")
            self._input_header.setStyleSheet("font-weight: bold;")

            self._clear_button = QToolButton()
            self._clear_button.setText("Clear")
            self._clear_button.setToolTip("Clear input text area")
            self._clear_button.clicked.connect(self._clear_input)
            logger.debug("__init__: Clear button initialized")

            self._paste_button = QToolButton()
            self._paste_button.setText("Paste")
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
            self._copy_button.setText("Copy")
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

            input_layout = self._create_section_layout(
                self._input_header,
                self._paste_button,
                self._input_text,
                self._clear_button,
            )
            layout.addLayout(input_layout)

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

        self.setObjectName("textInteractionAreasWidget")
        self._input_header.setObjectName("textInteractionAreaHeader")
        self._input_text.setObjectName("textInteractionAreaInputText")
        self._output_header.setObjectName("textInteractionAreaHeader")
        self._output_text.setObjectName("textInteractionAreaOutputText")
        self._clear_button.setObjectName("textInteractionAreaClearButton")
        self._paste_button.setObjectName("textInteractionAreaPasteButton")
        self._copy_button.setObjectName("textInteractionAreaCopyButton")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    @staticmethod
    def _create_section_layout(header: QLabel,
                               action_button: QToolButton,
                               text_area: QTextEdit,
                               clear_button: Optional[QToolButton] = None,
                               ) -> QVBoxLayout:
        """
        Create a labeled section with header, action button, and text area.

        Args:
            header: Label for the section (e.g., "Input", "Output").
            clear_button: Button for clearing text.
            action_button: Button for clipboard operations.
            text_area: QTextEdit for text input/output.

        Returns:
            QVBoxLayout containing the assembled section.

        Raises:
            Exception: If layout creation fails.
        """
        try:
            logger.debug("_create_section_layout: Creating text section")

            section_layout = QVBoxLayout()
            section_layout.setContentsMargins(0, 0, 0, 0)
            section_layout.setSpacing(4)

            header_layout = QHBoxLayout()
            header_layout.addWidget(header)
            header_layout.addStretch()
            if clear_button:
                header_layout.addWidget(clear_button)
            header_layout.addWidget(action_button)
            section_layout.addLayout(header_layout)

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

    def _clear_input(self) -> None:
        """
        Clear the input text area.
        """
        logger.debug("_clear_input: Clear operation started")
        self.set_input_text("")
        logger.debug("_clear_input: Cleared input text area")

    def _paste_from_clipboard(self) -> None:
        """
        Paste text from system clipboard into the input text area.

        Notes:
            Only plain text is pasted. Logs the operation and handles empty clipboard.
        """
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
        """
        Copy text from output area to system clipboard.

        Notes:
            Only plain text is copied. Logs the operation and handles empty content.
        """
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
        """
        Set the text in the input area.

        Args:
            text: The text to display in the input QTextEdit.

        Notes:
            Replaces all existing content. Logs the character count.
        """
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
        """
        Get the current text from the input area.

        Returns:
            The plain text content of the input QTextEdit.

        Notes:
            Returns empty string if retrieval fails.
        """
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
        """
        Set the text in the output area.

        Args:
            text: The text to display in the output QTextEdit.

        Notes:
            Replaces all existing content. Logs the character count.
        """
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
        """
        Get the current text from the output area.

        Returns:
            The plain text content of the output QTextEdit.

        Notes:
            Returns empty string if retrieval fails.
        """
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
        """
        Update the enabled state of all contained widgets.

        Args:
            enabled: True to enable all widgets, False to disable.

        Notes:
            Affects both text areas and clipboard buttons. Used to prevent interaction
            during processing or when context is not ready.
        """
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
