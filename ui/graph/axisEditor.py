from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QComboBox,
)


class AxisEditor(QWidget):

    settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.xmin_edit = QLineEdit()
        self.xmin_edit.setPlaceholderText("auto")
        self.xmin_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("X Min", self.xmin_edit)

        self.xmax_edit = QLineEdit()
        self.xmax_edit.setPlaceholderText("auto")
        self.xmax_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("X Max", self.xmax_edit)

        self.ymin_edit = QLineEdit()
        self.ymin_edit.setPlaceholderText("auto")
        self.ymin_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("Y Min", self.ymin_edit)

        self.ymax_edit = QLineEdit()
        self.ymax_edit.setPlaceholderText("auto")
        self.ymax_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("Y Max", self.ymax_edit)

        self.x_scale = QComboBox()
        self.x_scale.setMinimumHeight(36)
        self.x_scale.addItems(["Linear", "Log"])
        self.x_scale.currentTextChanged.connect(
            self._emit_changed
        )
        layout.addRow("X Scale", self.x_scale)

        self.y_scale = QComboBox()
        self.y_scale.setMinimumHeight(36)
        self.y_scale.addItems(["Linear", "Log"])
        self.y_scale.currentTextChanged.connect(
            self._emit_changed
        )
        layout.addRow("Y Scale", self.y_scale)

        self.grid_x = QCheckBox("Grid X")
        self.grid_x.toggled.connect(self._emit_changed)
        layout.addRow(self.grid_x)

        self.grid_y = QCheckBox("Grid Y")
        self.grid_y.toggled.connect(self._emit_changed)
        layout.addRow(self.grid_y)

    def load_settings(
        self,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        x_scale: str = "linear",
        y_scale: str = "linear",
        grid_x: bool = False,
        grid_y: bool = False,
    ):
        self.blockSignals(True)

        self.xmin_edit.setText("" if xmin is None else str(xmin))
        self.xmax_edit.setText("" if xmax is None else str(xmax))
        self.ymin_edit.setText("" if ymin is None else str(ymin))
        self.ymax_edit.setText("" if ymax is None else str(ymax))

        self.x_scale.setCurrentText(
            "Log" if x_scale == "log" else "Linear"
        )
        self.y_scale.setCurrentText(
            "Log" if y_scale == "log" else "Linear"
        )

        self.grid_x.setChecked(grid_x)
        self.grid_y.setChecked(grid_y)

        self.blockSignals(False)

    def _parse_float(self, text: str):
        text = text.strip()

        if not text:
            return None

        return float(text)

    def xmin(self):
        return self._parse_float(self.xmin_edit.text())

    def xmax(self):
        return self._parse_float(self.xmax_edit.text())

    def ymin(self):
        return self._parse_float(self.ymin_edit.text())

    def ymax(self):
        return self._parse_float(self.ymax_edit.text())

    def x_scale_value(self) -> str:
        return (
            "log"
            if self.x_scale.currentText() == "Log"
            else "linear"
        )

    def y_scale_value(self) -> str:
        return (
            "log"
            if self.y_scale.currentText() == "Log"
            else "linear"
        )

    def grid_x_enabled(self) -> bool:
        return self.grid_x.isChecked()

    def grid_y_enabled(self) -> bool:
        return self.grid_y.isChecked()

    def _emit_changed(self):
        self.settings_changed.emit()
