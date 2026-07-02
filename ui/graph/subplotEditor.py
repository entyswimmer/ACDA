from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QCheckBox,
)

from ui.widgets.unitSelector import (
    TIME_UNITS,
    UnitSelector,
)


class SubplotEditor(QWidget):

    settings_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Graph title")
        self.title_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("Title", self.title_edit)

        self.x_label_edit = QLineEdit()
        self.x_label_edit.setPlaceholderText("X axis label")
        self.x_label_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("X Label", self.x_label_edit)

        self.y_label_edit = QLineEdit()
        self.y_label_edit.setPlaceholderText("Y axis label")
        self.y_label_edit.textChanged.connect(
            self._emit_changed
        )
        layout.addRow("Y Label", self.y_label_edit)

        self.x_unit = UnitSelector(TIME_UNITS)
        self.x_unit.prefix_changed.connect(
            self._emit_changed
        )
        layout.addRow("X Unit", self.x_unit)

        self.y_unit = UnitSelector()
        self.y_unit.prefix_changed.connect(
            self._emit_changed
        )
        layout.addRow("Y Unit", self.y_unit)

        self.legend_check = QCheckBox("Show legend")
        self.legend_check.setChecked(True)
        self.legend_check.toggled.connect(
            self._emit_changed
        )
        layout.addRow(self.legend_check)

    def load_settings(
        self,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        x_unit: str = "",
        y_unit: str = "",
        legend: bool = True,
    ):
        self.blockSignals(True)

        self.title_edit.setText(title)
        self.x_label_edit.setText(x_label)
        self.y_label_edit.setText(y_label)
        self.x_unit.set_prefix(x_unit)
        self.y_unit.set_prefix(y_unit)
        self.legend_check.setChecked(legend)

        self.blockSignals(False)

    def title(self) -> str:
        return self.title_edit.text().strip()

    def x_label(self) -> str:
        return self.x_label_edit.text().strip()

    def y_label(self) -> str:
        return self.y_label_edit.text().strip()

    def x_unit_prefix(self) -> str:
        return self.x_unit.prefix()

    def y_unit_prefix(self) -> str:
        return self.y_unit.prefix()

    def legend(self) -> bool:
        return self.legend_check.isChecked()

    def _emit_changed(self):
        self.settings_changed.emit()
