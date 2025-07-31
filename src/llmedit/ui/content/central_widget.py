from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QSizePolicy, QVBoxLayout
)

from context import AppContext
from ui.content.tab_widgets.action_tabs_widget import ActionTabsWidget
from ui.content.text_widgets.text_interaction_areas_widget import TextInteractionAreasWidget


class CentralWidget(QWidget):
    tab_action_requested = pyqtSignal()

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        """Initialize the central tab widget.

        Args:
            parent: Optional parent widget
        """
        super().__init__(parent)
        self._ctx = ctx

        self._text_widget = TextInteractionAreasWidget()
        self._tabs = ActionTabsWidget(ctx)
        layout = QVBoxLayout()
        layout.addWidget(self._text_widget, 8)
        layout.addWidget(self._tabs, 2)
        self.setLayout(layout)

        self._setup_tabs()
        self._configure_appearance()
        self._connect_signals()

    def _setup_tabs(self) -> None:
        """Initialize and populate all tab widgets with specialized content."""
        # self._proofreading_tab = self._create_tab(self._config_provider.get_proofreading_config())
        # self._formatting_tab = self._create_tab(self._config_provider.get_formatting_config())
        # self._translation_tab = self._create_tab(self._config_provider.get_translation_config())

        # Add tabs to the widget
        # self.addTab(self._proofreading_tab, "Proofreading")
        # self.addTab(self._formatting_tab, "Formatting")
        # self.addTab(self._translation_tab, "Translation")
        pass

    def _connect_signals(self) -> None:
        """Connect all tab action signals to the central handler."""
        # self._proofreading_tab.action_requested.connect(self._process_tab_action)
        # self._formatting_tab.action_requested.connect(self._process_tab_action)
        # self._translation_tab.action_requested.connect(self._process_tab_action)
        pass

    def _process_tab_action(self) -> None:
        """Process a tab action request."""
        # self.tab_action_requested.emit(tab_action_ctx)
        pass

    def _create_tab(self, config):
        """Create a tab with the given configuration.

        Args:
            config: Tab configuration

        Returns:
            Configured TabContentWidget instance
        """
        # return TabContentWidget(
        #     config.buttons,
        #     tab_id=config.tab_id,
        #     input_dropdown_items=config.input_dropdown_items,
        #     output_dropdown_items=config.output_dropdown_items
        # )
        pass

    def _configure_appearance(self) -> None:
        """Configure widget appearance and sizing policies."""
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

    def set_tabs_enabled(self, enabled: bool) -> None:
        self.setEnabled(enabled)

        # Then disable all content within each tab
        # self._proofreading_tab.set_enabled(enabled)
        # self._formatting_tab.set_enabled(enabled)
        # self._translation_tab.set_enabled(enabled)

    def set_input_text(self, text: str, tab_id: str) -> None:
        """Set the text in the input area."""
        # if tab_id == "proofreading_tab":
        #     self._proofreading_tab.set_input_text(text)
        # elif tab_id == "formatting_tab":
        #     self._formatting_tab.set_input_text(text)
        # elif tab_id == "translation_tab":
        #     self._translation_tab.set_input_text(text)
        # else:
        #     raise ValueError(f"Invalid tab ID: {tab_id}")
        pass

    def set_output_text(self, text: str, tab_id: str) -> None:
        """Set the text in the output area."""
        # if tab_id == "proofreading_tab":
        #     self._proofreading_tab.set_output_text(text)
        # elif tab_id == "formatting_tab":
        #     self._formatting_tab.set_output_text(text)
        # elif tab_id == "translation_tab":
        #     self._translation_tab.set_output_text(text)
        # else:
        #     raise ValueError(f"Invalid tab ID: {tab_id}")
        pass
