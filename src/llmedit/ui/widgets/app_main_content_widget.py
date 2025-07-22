from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget
)

from core.abstracts.app_context import AppContext
from llmedit.ui.widgets.app_bottom_bar_widget import AppBottomBarWidget
from llmedit.ui.widgets.app_mode_switcher_widget import ApplicationMode, AppModeSwitcherWidget
from llmedit.ui.widgets.app_top_bar_widget import AppTopBarWidget
from llmedit.ui.widgets.modes.app_text_utilities_widget import AppTextUtilitiesWidget
from llmedit.ui.widgets.modes.app_translator_widget import AppTranslatorWidget


class AppMainContentWidget(QWidget):

    def __init__(self, app_context: AppContext, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        model = app_context.app_settings.get_settings().model_name
        app_context.llm_provider.get_llm_provider().load_model(model)

        # Top Bar Widget
        top_bar = AppTopBarWidget()
        main_layout.addWidget(top_bar)

        # Mode Switcher Widget
        mode_switcher = AppModeSwitcherWidget()
        main_layout.addWidget(mode_switcher)

        # Content Area (Stacked Widget for different modes)
        self.translator_widget = AppTranslatorWidget(app_context)
        self.text_utilities_widget = AppTextUtilitiesWidget(app_context)
        self.content_area = QStackedWidget()
        self.content_area.addWidget(self.translator_widget)
        self.content_area.addWidget(self.text_utilities_widget)
        main_layout.addWidget(self.content_area)

        # Bottom Bar Widget
        self.bottom_bar = AppBottomBarWidget()
        main_layout.addWidget(self.bottom_bar)

        # Connect Mode Switcher signal to switch content area widgets
        mode_switcher.mode_changed.connect(self.switch_content_mode)

        self.setLayout(main_layout)
        self.show()

        self.translator_widget.model_changed.connect(self.on_model_changed)
        self.text_utilities_widget.model_changed.connect(self.on_model_changed)

    def switch_content_mode(self, mode: ApplicationMode):
        if mode == ApplicationMode.TRANSLATION:
            self.content_area.setCurrentIndex(0)  # Translation Widget index
        elif mode == ApplicationMode.TEXT_UTILS:
            self.content_area.setCurrentIndex(1)  # Text Utilities Widget index

    def on_model_changed(self, model_name: str):
        self.bottom_bar.update_llm_name(model_name)
