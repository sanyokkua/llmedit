from enum import StrEnum

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton

from core.abstracts.app_context import AppContext
from core.abstracts.types import PromptType
from llmedit.ui.widgets.customs.app_io_mode_widgets import TextUtilsIOWidget
from llmedit.ui.widgets.customs.app_tools_line_widgets import AppButtonsLineWidget, AppLMPropsWidget


class AppTextUtilitiesWidgetEvents(StrEnum):
    PROOFREAD = "Proofread"
    REWRITE = "Rewrite"
    REGENERATE = "Regenerate"
    FORMAL = "Formal"
    CASUAL = "Casual"
    FRIENDLY = "Friendly"
    EMAIL = "Email"
    CHAT = "Chat"
    DOCUMENT = "Document"
    SOCIAL_MEDIA_POST = "SocialMediaPost"
    ARTICLES = "Articles"
    DOCUMENTATION = "Documentation"


class AppTextUtilitiesWidget(QWidget):
    functional_btn_clicked = pyqtSignal(str)
    temperature_changed = pyqtSignal(float)
    model_changed = pyqtSignal(str)

    def __init__(self, app_context: AppContext):
        super().__init__()
        self._app_context: AppContext = app_context

        self._text_utility_io = TextUtilsIOWidget()
        self._controls_widget = AppButtonsLineWidget(buttons={
            AppTextUtilitiesWidgetEvents.PROOFREAD: QPushButton("Proofread", self),
            AppTextUtilitiesWidgetEvents.REWRITE: QPushButton("Rewrite", self),
            AppTextUtilitiesWidgetEvents.REGENERATE: QPushButton("Regenerate", self),
        })
        self._tone_widget = AppButtonsLineWidget(buttons={
            AppTextUtilitiesWidgetEvents.FORMAL: QPushButton("Formal", self),
            AppTextUtilitiesWidgetEvents.CASUAL: QPushButton("Casual", self),
            AppTextUtilitiesWidgetEvents.FRIENDLY: QPushButton("Friendly", self),
        }, group_label="Tone: ")
        self._format_widget = AppButtonsLineWidget(buttons={
            AppTextUtilitiesWidgetEvents.EMAIL: QPushButton("Email", self),
            AppTextUtilitiesWidgetEvents.CHAT: QPushButton("Chat", self),
            AppTextUtilitiesWidgetEvents.DOCUMENT: QPushButton("Document", self),
        }, group_label="Format: ")
        self._structure_widget = AppButtonsLineWidget(buttons={
            AppTextUtilitiesWidgetEvents.SOCIAL_MEDIA_POST: QPushButton("Social Media Post", self),
            AppTextUtilitiesWidgetEvents.ARTICLES: QPushButton("Articles", self),
            AppTextUtilitiesWidgetEvents.DOCUMENTATION: QPushButton("Documentation", self),
        }, group_label="Structure: ")
        self._lm_control_widget = AppLMPropsWidget(app_context.llm_provider.get_llm_provider().get_available_models())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self._text_utility_io)
        main_layout.addWidget(self._controls_widget)
        main_layout.addWidget(self._tone_widget)
        main_layout.addWidget(self._format_widget)
        main_layout.addWidget(self._structure_widget)
        main_layout.addWidget(self._lm_control_widget)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setSpacing(0)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self._controls_widget.button_clicked.connect(self.handle_functional_btn_click)
        self._tone_widget.button_clicked.connect(self.handle_functional_btn_click)
        self._format_widget.button_clicked.connect(self.handle_functional_btn_click)
        self._structure_widget.button_clicked.connect(self.handle_functional_btn_click)
        self._lm_control_widget.model_changed.connect(self.on_model_change)
        self._lm_control_widget.temperature_changed.connect(self.on_temperature_change)

    @property
    def input_text(self) -> str:
        return self._text_utility_io.input_text

    @property
    def output_text(self) -> str:
        return self._text_utility_io.output_text

    @property
    def model(self) -> str:
        return self._lm_control_widget.model

    @property
    def temperature(self) -> float:
        return self._lm_control_widget.temperature

    def handle_functional_btn_click(self, btn_name: str):
        self.functional_btn_clicked.emit(btn_name)

        content = self.input_text if btn_name != AppTextUtilitiesWidgetEvents.REGENERATE else self.output_text
        model = self.model
        temperature = self.temperature

        ops_lib: dict[str, PromptType] = {
            AppTextUtilitiesWidgetEvents.PROOFREAD: PromptType.PROOFREADING_BASE,
            AppTextUtilitiesWidgetEvents.REWRITE: PromptType.PROOFREADING_REWRITING,
            AppTextUtilitiesWidgetEvents.REGENERATE: PromptType.PROOFREADING_REWRITING,
            AppTextUtilitiesWidgetEvents.FORMAL: PromptType.PROOFREADING_FORMAL,
            AppTextUtilitiesWidgetEvents.CASUAL: PromptType.PROOFREADING_CASUAL,
            AppTextUtilitiesWidgetEvents.FRIENDLY: PromptType.PROOFREADING_FRIENDLY,
            AppTextUtilitiesWidgetEvents.EMAIL: PromptType.TRANSFORMING_EMAIL,
            AppTextUtilitiesWidgetEvents.CHAT: PromptType.TRANSFORMING_CHAT,
            AppTextUtilitiesWidgetEvents.DOCUMENT: PromptType.TRANSFORMING_PLAIN_DOCUMENTATION,
            AppTextUtilitiesWidgetEvents.SOCIAL_MEDIA_POST: PromptType.TRANSFORMING_SOCIAL_MEDIA_POST,
            AppTextUtilitiesWidgetEvents.ARTICLES: PromptType.TRANSFORMING_WIKI_DOCUMENTATION,
            AppTextUtilitiesWidgetEvents.DOCUMENTATION: PromptType.TRANSFORMING_WIKI_DOCUMENTATION,
        }
        func = self._app_context.transformation_service_provider.get_text_transformation_service().process_text
        operation = ops_lib[btn_name]
        text = func(content, operation)
        self._text_utility_io.output_text = text

    def on_model_change(self, model_name: str):
        self.model_changed.emit(model_name)

    def on_temperature_change(self, value: float):
        self.temperature_changed.emit(value)
