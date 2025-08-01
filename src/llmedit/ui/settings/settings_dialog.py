from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QSlider, QVBoxLayout)

from context import AppContext
from core.interfaces.settings.settings_service import SettingsService
from core.models.enums.settings import LlmProviderType
from core.models.settings import SettingsState


class SettingsDialog(QDialog):
    """
    Dialog window for configuring application settings.

    Provides UI controls for selecting LLM provider, model, and temperature settings.
    Changes are applied only when Save is clicked.
    """

    def __init__(self, app_context: AppContext, parent=None):
        """
        Initialize the settings dialog.

        Args:
            app_context: Application context providing access to settings service.
            parent: Optional parent widget.

        Notes:
            Loads current settings state and populates UI controls accordingly.
            Connects signals for dynamic updates (e.g., provider changes reload models).
        """
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self._settings_service: SettingsService = app_context.settings_service

        self._state: SettingsState = self._settings_service.get_settings_state()

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        self.provider_combo = QComboBox()
        for provider in self._settings_service.get_llm_provider_list():
            self.provider_combo.addItem(provider.value, provider)
        idx = self.provider_combo.findData(self._state.llm_provider)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)
        form_layout.addRow(QLabel("LLM Provider:"), self.provider_combo)

        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        form_layout.addRow(QLabel("LLM Model:"), self.model_combo)

        self._reload_models()
        if self._state.llm_model_name:
            idx = self.model_combo.findText(self._state.llm_model_name)
            if idx >= 0:
                self.model_combo.setCurrentIndex(idx)
            else:
                self.model_combo.setEditText(self._state.llm_model_name)

        self.provider_combo.currentIndexChanged.connect(self._on_provider_changed)

        self.temp_check = QCheckBox("Enable custom temperature")
        self.temp_check.setChecked(self._state.llm_temperature_enabled)
        form_layout.addRow(self.temp_check)

        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(100)
        self.temp_slider.setValue(int(self._state.llm_temperature * 100))
        self.temp_slider.setEnabled(self._state.llm_temperature_enabled)
        self.temp_slider.setProperty("tempSlider", True)
        form_layout.addRow(QLabel("Temperature:"), self.temp_slider)

        self.temp_check.toggled.connect(self.temp_slider.setEnabled)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._on_save)
        btn_box.rejected.connect(self.reject)
        main_layout.addWidget(btn_box)

    def _reload_models(self):
        """
        Reload available models for the currently selected provider.

        Notes:
            Clears and repopulates the model combo box.
            Includes an empty option at the top.
            Called when provider changes or dialog initializes.
        """
        self.model_combo.clear()
        models = self._settings_service.get_llm_models_for_selected_provider()
        for m in models:
            self.model_combo.addItem(m.name, m.name)
        self.model_combo.insertItem(0, "", None)

    def _on_provider_changed(self):
        """
        Handle LLM provider selection changes.

        Notes:
            Updates the settings service with the new provider.
            Reloads available models for the new provider.
        """
        new_provider: LlmProviderType = self.provider_combo.currentData()
        self._settings_service.set_llm_provider(new_provider)
        self._reload_models()

    def _on_save(self):
        """
        Apply settings changes and close the dialog.

        Notes:
            Saves model name, temperature enabled state, and temperature value.
            Only applies changes when Save button is clicked.
        """
        model_name = self.model_combo.currentText().strip() or None
        self._settings_service.set_llm_model_name(model_name)
        enabled = self.temp_check.isChecked()
        temp = self.temp_slider.value() / 100.0
        self._settings_service.set_llm_temperature_enabled(enabled)
        self._settings_service.set_llm_temperature(temp)

        self.accept()
