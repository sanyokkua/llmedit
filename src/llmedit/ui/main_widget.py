from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy, QDialog
)

from context import AppContext
from ui.content.bottom_widget import BottomBarWidget
from ui.content.central_widget import CentralWidget
from ui.content.top_widget import TopBarWidget
from ui.settings.settings_dialog import SettingsDialog


class MainWidget(QWidget):

    def __init__(self, ctx: AppContext, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._ctx = ctx
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        top_widget = TopBarWidget(self)
        center_widget = CentralWidget(ctx)
        bottom_widget = BottomBarWidget(self)

        layout.addWidget(top_widget)
        layout.addWidget(center_widget)
        layout.addWidget(bottom_widget)

        self.setLayout(layout)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        top_widget.settings_clicked.connect(self._on_settings_clicked)

    def _on_settings_clicked(self) -> None:
        settings = SettingsDialog(self._ctx)
        result = settings.exec()

        # If OK was clicked, process the settings
        if result == QDialog.DialogCode.Accepted:
            print(f"Settings updated: {settings}")
