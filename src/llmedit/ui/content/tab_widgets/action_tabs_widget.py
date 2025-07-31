from typing import Optional

from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget,
    QSizePolicy
)

from context import AppContext
from core.models.enums.prompt import PromptCategory
from ui.content.tab_widgets.action_controls_widget import ActionControlsWidget


class ActionTabsWidget(QTabWidget):
    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self._proofreading_tab = ActionControlsWidget(
            prompts=ctx.prompt_service.get_prompts_by_category(PromptCategory.PROOFREAD)
        )
        self._format_tab = ActionControlsWidget(
            prompts=ctx.prompt_service.get_prompts_by_category(PromptCategory.FORMAT)
        )
        self._translate_tab = ActionControlsWidget(
            prompts=ctx.prompt_service.get_prompts_by_category(PromptCategory.TRANSLATE),
            input_dropdown_items=ctx.supported_languages_service.get_supported_translation_languages(),
            output_dropdown_items=ctx.supported_languages_service.get_supported_translation_languages(),
        )
        self.addTab(self._proofreading_tab, "Proofreading")
        self.addTab(self._format_tab, "Formatting")
        self.addTab(self._translate_tab, "Translating")
