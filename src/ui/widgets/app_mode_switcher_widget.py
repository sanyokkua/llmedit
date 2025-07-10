from enum import StrEnum
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton


class ApplicationMode(StrEnum):
    TRANSLATION = "Translation Mode"
    TEXT_UTILS = "Text Utilities Mode"


class AppModeSwitcherWidget(QWidget):
    mode_changed = pyqtSignal(ApplicationMode)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.current_mode: ApplicationMode = ApplicationMode.TRANSLATION
        self.widget_layout = QHBoxLayout()

        # Create buttons
        self.translation_button = QPushButton("Translation Mode", self)
        self.text_utilities_button = QPushButton("Text Utilities Mode", self)

        # Connect button clicks to handlers
        self.translation_button.clicked.connect(self.on_translation_mode_selected)
        self.text_utilities_button.clicked.connect(self.on_text_utilities_mode_selected)

        # Add buttons to the layout
        self.widget_layout.addWidget(self.translation_button)
        self.widget_layout.addWidget(self.text_utilities_button)
        self.widget_layout.addStretch()

        # Create a label for displaying the selected mode
        self.mode_label = QLabel(f"Selected: {self.current_mode.__str__()}", self)
        self.widget_layout.addWidget(self.mode_label)

        self.setLayout(self.widget_layout)
        self.update_button_styles()

    def on_translation_mode_selected(self):
        if self.current_mode != ApplicationMode.TRANSLATION:
            self.current_mode = ApplicationMode.TRANSLATION
            self.mode_label.setText(f"Selected: {self.current_mode}")
            self.mode_changed.emit(ApplicationMode.TRANSLATION)
            self.update_button_styles()

    def on_text_utilities_mode_selected(self):
        if self.current_mode != ApplicationMode.TEXT_UTILS:
            self.current_mode = ApplicationMode.TEXT_UTILS
            self.mode_label.setText(f"Selected: {self.current_mode}")
            self.mode_changed.emit(ApplicationMode.TEXT_UTILS)
            self.update_button_styles()

    def update_button_styles(self):
        # Update button styles based on the selected mode
        bold_style = "padding: 10px; margin-right: 10px; font-weight: bold;"
        normal_style = "padding: 10px; margin-right: 10px;"
        if self.current_mode == ApplicationMode.TRANSLATION:
            self.translation_button.setStyleSheet(bold_style)
            self.text_utilities_button.setStyleSheet(normal_style)
        else:  # Text Utilities Mode
            self.translation_button.setStyleSheet(normal_style)
            self.text_utilities_button.setStyleSheet(bold_style)
