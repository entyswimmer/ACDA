from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class DevicePanel(QWidget):

    device_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        group = QGroupBox("Device")
        layout.addWidget(group)

        group_layout = QVBoxLayout(group)

        # -------------------------
        # Device Type
        # -------------------------

        group_layout.addWidget(
            QLabel("Device Type")
        )

        self.nmos_radio = QRadioButton(
            "NMOS"
        )

        self.pmos_radio = QRadioButton(
            "PMOS"
        )

        self.nmos_radio.setChecked(
            True
        )

        self.device_group = (
            QButtonGroup(self)
        )

        self.device_group.addButton(
            self.nmos_radio
        )

        self.device_group.addButton(
            self.pmos_radio
        )

        group_layout.addWidget(
            self.nmos_radio
        )

        group_layout.addWidget(
            self.pmos_radio
        )

        self.nmos_radio.toggled.connect(
            self._emit_device_changed
        )

        self.pmos_radio.toggled.connect(
            self._emit_device_changed
        )

        # -------------------------
        # Model
        # -------------------------

        group_layout.addWidget(
            QLabel("Model")
        )

        self.model_combo = QComboBox()

        group_layout.addWidget(
            self.model_combo
        )

        # -------------------------
        # Parameters
        # -------------------------

        group_layout.addWidget(
            QLabel("Parameters")
        )

        self.param_table = (
            QTableWidget(0, 2)
        )

        self.param_table.setHorizontalHeaderLabels(
            ["Parameter", "Value"]
        )

        self.param_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        group_layout.addWidget(
            self.param_table
        )

    def _emit_device_changed(self):

        self.device_changed.emit(
            self.selected_device()
        )

    def selected_device(self) -> str:

        if self.pmos_radio.isChecked():

            return "pmos"

        return "nmos"

    def set_models(
        self,
        model_names: list[str]
    ):

        self.model_combo.clear()

        self.model_combo.addItems(
            model_names
        )

    def selected_model(self) -> str:

        return self.model_combo.currentText()

    def update_parameters(
        self,
        params: dict
    ):

        self.param_table.setRowCount(
            len(params)
        )

        for row, (key, value) in enumerate(
            params.items()
        ):

            self.param_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(key)
                )
            )

            self.param_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(value)
                )
            )