from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QGridLayout


class AppButtonsLineWidget(QWidget):
    button_clicked = pyqtSignal(str)

    def __init__(self, buttons: dict[str, QPushButton], group_label: str = ''):
        super().__init__()

        # Create GridLayout with 1 row and columns based on buttons count
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)

        # Add label if provided
        index_inc = 0
        if group_label:
            grid_layout.addWidget(QLabel(group_label), 0, index_inc)
            index_inc = 1

        for index, (key, button) in enumerate(buttons.items()):
            # Add buttons to the grid
            grid_layout.addWidget(button, 0, index + index_inc)

            # Connect signal handler
            handler = lambda _, k=key: self.button_clicked.emit(k)
            button.clicked.connect(handler)

        main_layout.addLayout(grid_layout)
        main_layout.setSpacing(5)


class AppLMPropsWidget(QWidget):
    temperature_changed = pyqtSignal(float)
    model_changed = pyqtSignal(str)

    def __init__(self, models: list[str]):
        super().__init__()
        self._temperature_label = QLabel("LM Creativeness: ", self)
        self._temperature_slider = QSlider(Qt.Orientation.Horizontal, self)
        self._temperature_slider.setMinimum(0)
        self._temperature_slider.setMaximum(100)
        self._temperature_slider.setValue(50)  # Default to 0.5
        self._temperature_slider.setTickInterval(10)
        self._temperature_slider_lbl = QLabel(f"{self._temperature_slider.value()}", self)
        self._model_combo = QComboBox(self)
        self._model_combo.addItems(models)
        self._model_label = QLabel(f"Model: {self._model_combo.currentText().strip()}", self)

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self._temperature_label, 0, 0)
        grid_layout.addWidget(self._temperature_slider, 0, 1)
        grid_layout.addWidget(self._temperature_slider_lbl, 0, 2)
        grid_layout.addWidget(self._model_combo, 0, 3)
        grid_layout.addWidget(self._model_label, 0, 4)
        grid_layout.setSpacing(5)
        self.setLayout(grid_layout)

        self._model_combo.currentTextChanged.connect(self._on_model_changed)
        self._temperature_slider.valueChanged.connect(self._on_temperature_changed)

    @property
    def temperature(self) -> float:
        return self._temperature_slider.value() / 100.0

    @property
    def model(self) -> str:
        return self._model_combo.currentText()

    def _on_model_changed(self, model_name: str):
        print(f"Model changed to: {model_name}")
        self.model_changed.emit(model_name)
        self._model_label.setText(f"Model: {model_name}")

    def _on_temperature_changed(self, value: int):
        temperature = value / 100.0
        print(f"Temperature changed to: {temperature}")
        self.temperature_changed.emit(temperature)
        self._temperature_slider_lbl.setText(f"{temperature}")
