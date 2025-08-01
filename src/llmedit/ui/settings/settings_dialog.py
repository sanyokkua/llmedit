from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QComboBox, QSlider, QCheckBox, QDialogButtonBox
)

from context import AppContext
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.settings import LlmProviderType
from core.models.settings import SettingsState


class SettingsDialog(QDialog):
    def __init__(self, app_context: AppContext, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self._settings_service: SettingsService = app_context.settings_service

        # Load state
        self._state: SettingsState = self._settings_service.get_settings_state()

        # Layouts
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        # 1. LLM Provider dropdown
        self.provider_combo = QComboBox()
        for provider in self._settings_service.get_llm_provider_list():
            self.provider_combo.addItem(provider.value, provider)
        # set current
        idx = self.provider_combo.findData(self._state.llm_provider)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)
        form_layout.addRow(QLabel("LLM Provider:"), self.provider_combo)

        # 2. LLM Model dropdown (editable for empty)
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        form_layout.addRow(QLabel("LLM Model:"), self.model_combo)

        # Populate models for initial provider
        self._reload_models()
        # set current model name
        if self._state.llm_model_name:
            idx = self.model_combo.findText(self._state.llm_model_name)
            if idx >= 0:
                self.model_combo.setCurrentIndex(idx)
            else:
                self.model_combo.setEditText(self._state.llm_model_name)

        # Provider change handler
        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)

        # 3. Temperature enabled checkbox
        self.temp_check = QCheckBox("Enable custom temperature")
        self.temp_check.setChecked(self._state.llm_temperature_enabled)
        form_layout.addRow(self.temp_check)

        # 4. Temperature slider
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(100)
        self.temp_slider.setValue(int(self._state.llm_temperature * 100))
        self.temp_slider.setEnabled(self._state.llm_temperature_enabled)
        form_layout.addRow(QLabel("Temperature:"), self.temp_slider)

        # Toggle slider enabled
        self.temp_check.toggled.connect(self.temp_slider.setEnabled)

        # Button box
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._on_save)
        btn_box.rejected.connect(self.reject)
        main_layout.addWidget(btn_box)

    def _reload_models(self):
        # clear
        self.model_combo.clear()
        provider = self.provider_combo.currentData()
        models = self._settings_service.get_llm_models_for_selected_provider()
        for m in models:
            self.model_combo.addItem(m.name, m.name)
        # allow empty
        self.model_combo.insertItem(0, "", None)

    def _on_provider_changed(self, index: int):
        new_provider: LlmProviderType = self.provider_combo.currentData()
        self._settings_service.set_llm_provider(new_provider)
        # reload models
        self._reload_models()

    def _on_save(self):
        # provider is already set on change
        # model name
        model_name = self.model_combo.currentText().strip() or None
        self._settings_service.set_llm_model_name(model_name)
        # temperature
        enabled = self.temp_check.isChecked()
        temp = self.temp_slider.value() / 100.0
        self._settings_service.set_llm_temperature_enabled(enabled)
        self._settings_service.set_llm_temperature(temp)

        self.accept()
