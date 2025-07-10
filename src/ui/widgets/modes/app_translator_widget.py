from enum import StrEnum

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.app_context import AppContext
from src.business_logic.interface import OperationOptions
from src.ui.widgets.customs.app_io_mode_widgets import TranslatorIOWidget
from src.ui.widgets.customs.app_tools_line_widgets import AppButtonsLineWidget, AppLMPropsWidget


class AppTranslatorWidgetEvents(StrEnum):
    TRANSLATE = "Translate"
    REGENERATE = "Regenerate"


class AppTranslatorWidget(QWidget):
    source_language_changed = pyqtSignal(str)
    target_language_changed = pyqtSignal(str)
    functional_btn_clicked = pyqtSignal(str)
    temperature_changed = pyqtSignal(float)
    model_changed = pyqtSignal(str)

    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context = app_context

        self._translator_widget = TranslatorIOWidget(app_context.language_provider.get_supported_languages())
        self._control_buttons = AppButtonsLineWidget({
            AppTranslatorWidgetEvents.TRANSLATE: QPushButton("Translate", self),
            AppTranslatorWidgetEvents.REGENERATE: QPushButton("Regenerate", self),
        })
        self._lm_control_widget = AppLMPropsWidget(app_context.llm_provider.get_available_models())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._translator_widget)
        main_layout.addWidget(self._control_buttons)
        main_layout.addWidget(self._lm_control_widget)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setSpacing(0)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self._translator_widget.source_language_changed.connect(self.on_source_language_change)
        self._translator_widget.target_language_changed.connect(self.on_target_language_change)
        self._control_buttons.button_clicked.connect(self.on_functional_button_click)
        self._lm_control_widget.model_changed.connect(self.on_model_change)
        self._lm_control_widget.temperature_changed.connect(self.on_temperature_change)

    @property
    def input_text(self) -> str:
        return self._translator_widget.input_text

    @property
    def output_text(self) -> str:
        return self._translator_widget.output_text

    @property
    def source_language(self) -> str:
        return self._translator_widget.source_language

    @property
    def target_language(self) -> str:
        return self._translator_widget.target_language

    @property
    def model(self) -> str:
        return self._lm_control_widget.model

    @property
    def temperature(self) -> float:
        return self._lm_control_widget.temperature

    def on_source_language_change(self, lang: str):
        self.source_language_changed.emit(lang)

    def on_target_language_change(self, lang: str):
        self.target_language_changed.emit(lang)

    def on_functional_button_click(self, btn_name: str):
        self.functional_btn_clicked.emit(btn_name)
        src_lang = self.source_language
        tgt_lang = self.target_language
        content = self.input_text
        model = self.model
        temperature = self.temperature
        ops: OperationOptions = OperationOptions(content=content, model_name=model, temperature=temperature)

        if btn_name == AppTranslatorWidgetEvents.TRANSLATE:
            text = self._app_context.text_tools.translate_text(source_language=src_lang, target_language=tgt_lang,
                                                               oper_ops=ops)
            self._translator_widget._output_app_text_area.text_edit_value = text
        elif btn_name == AppTranslatorWidgetEvents.REGENERATE:
            ops.content = self.output_text
            text = self._app_context.text_tools.make_regenerate(ops)
            self._translator_widget._output_app_text_area.text_edit_value = text

    def on_model_change(self, model_name: str):
        self.model_changed.emit(model_name)

    def on_temperature_change(self, value: float):
        self.temperature_changed.emit(value)
