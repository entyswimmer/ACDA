from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
)


class DevicePanel(QWidget):

    device_changed = Signal(str)

    def __init__(
        self,
        device,
        device_resolver
    ):
        super().__init__()

        self.device = device
        self.device_resolver = device_resolver

        self._build_ui()

        self.set_models(
            ["razavi_level1"]
        )

        self._refresh_parameters()

    def _build_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox("Device")
        group.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        layout.addWidget(group)

        group_layout = QVBoxLayout(group)

        # -------------------------
        # Device Type
        # -------------------------

        group_layout.addWidget(
            QLabel("Device Type")
        )

        device_type_row = QHBoxLayout()

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

        device_type_row.addWidget(
            self.nmos_radio
        )

        device_type_row.addWidget(
            self.pmos_radio
        )

        device_type_row.addStretch()

        group_layout.addLayout(
            device_type_row
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
        self.model_combo.setMinimumHeight(36)

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

        self.param_table.setMinimumHeight(
            280
        )
        self.param_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.param_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.param_table.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.param_table.verticalHeader().setVisible(
            False
        )

        self.param_table.setHorizontalHeaderLabels(
            ["Parameter", "Value"]
        )

        self.param_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        group_layout.addWidget(
            self.param_table,
            stretch=1,
        )

    def _emit_device_changed(self):

        self._refresh_parameters()

        self.device_changed.emit(
            self.selected_device()
        )

    def _refresh_parameters(self):

        params = self.device_resolver.get_all(
            self.device,
            self.selected_device()
        )

        self.update_parameters(
            params
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