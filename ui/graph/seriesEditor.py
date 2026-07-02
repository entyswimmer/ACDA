from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QComboBox,
    QCheckBox,
    QDoubleSpinBox,
    QAbstractItemView,
    QWidget,
)

from ui.widgets.colorSelector import ColorSelector, DEFAULT_COLORS
from ui.widgets.lineStyleSelector import LineStyleSelector
from ui.widgets.markerSelector import MarkerSelector


class SeriesEditor(QWidget):

    series_changed = Signal()
    add_requested = Signal()
    remove_requested = Signal(int)

    COLUMNS = [
        "Column",
        "Label",
        "Color",
        "Line",
        "Marker",
        "Width",
        "Visible",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self._available_columns: list[str] = []
        self._updating = False

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget(0, len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setMinimumHeight(180)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.cellChanged.connect(
            self._on_cell_changed
        )

        layout.addWidget(self.table)

        button_row = QHBoxLayout()

        self.add_button = QPushButton("Add Series")
        self.add_button.clicked.connect(
            self.add_requested.emit
        )

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(
            self._on_remove
        )

        button_row.addWidget(self.add_button)
        button_row.addWidget(self.remove_button)
        button_row.addStretch()

        layout.addLayout(button_row)

    def set_available_columns(self, columns: list[str]):
        self._available_columns = columns

    def load_series(self, series_list: list[dict]):
        self._updating = True

        self.table.setRowCount(len(series_list))

        for row, series in enumerate(series_list):
            self._set_row(row, series)

        self._updating = False

    def add_empty_series(self, column: str = ""):
        if not column and self._available_columns:
            column = self._available_columns[0]

        row = self.table.rowCount()
        self._updating = True
        self.table.insertRow(row)
        self._set_row(
            row,
            {
                "column": column,
                "label": column,
                "color": DEFAULT_COLORS[row % len(DEFAULT_COLORS)],
                "linestyle": "-",
                "marker": None,
                "linewidth": 2.0,
                "visible": True,
            },
        )
        self._updating = False
        self.series_changed.emit()

    def series_data(self) -> list[dict]:
        result = []

        for row in range(self.table.rowCount()):
            result.append(self._get_row(row))

        return result

    def _set_row(self, row: int, series: dict):
        column_combo = QComboBox()
        column_combo.setMinimumHeight(32)
        column_combo.addItems(self._available_columns)

        if series.get("column") in self._available_columns:
            column_combo.setCurrentText(series["column"])

        column_combo.currentTextChanged.connect(
            lambda _text, r=row: self._on_widget_changed(r)
        )

        label_item = QTableWidgetItem(series.get("label", ""))

        color = ColorSelector(series.get("color"))
        color.color_changed.connect(
            lambda _c, r=row: self._on_widget_changed(r)
        )

        linestyle = LineStyleSelector()
        linestyle.set_linestyle(series.get("linestyle", "-"))
        linestyle.style_changed.connect(
            lambda _s, r=row: self._on_widget_changed(r)
        )

        marker = MarkerSelector()
        marker.set_marker(series.get("marker"))
        marker.marker_changed.connect(
            lambda _m, r=row: self._on_widget_changed(r)
        )

        width = QDoubleSpinBox()
        width.setRange(0.5, 10.0)
        width.setSingleStep(0.5)
        width.setValue(series.get("linewidth", 2.0))
        width.valueChanged.connect(
            lambda _v, r=row: self._on_widget_changed(r)
        )

        visible = QCheckBox()
        visible.setChecked(series.get("visible", True))
        visible.setStyleSheet("margin-left: 16px;")
        visible.toggled.connect(
            lambda _v, r=row: self._on_widget_changed(r)
        )

        self.table.setCellWidget(row, 0, column_combo)
        self.table.setItem(row, 1, label_item)
        self.table.setCellWidget(row, 2, color)
        self.table.setCellWidget(row, 3, linestyle)
        self.table.setCellWidget(row, 4, marker)
        self.table.setCellWidget(row, 5, width)

        visible_widget = QWidget()
        visible_layout = QHBoxLayout(visible_widget)
        visible_layout.setContentsMargins(0, 0, 0, 0)
        visible_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        visible_layout.addWidget(visible)
        self.table.setCellWidget(row, 6, visible_widget)

    def _get_row(self, row: int) -> dict:
        column_widget = self.table.cellWidget(row, 0)
        color_widget = self.table.cellWidget(row, 2)
        linestyle_widget = self.table.cellWidget(row, 3)
        marker_widget = self.table.cellWidget(row, 4)
        width_widget = self.table.cellWidget(row, 5)
        visible_widget = self.table.cellWidget(row, 6)

        label_item = self.table.item(row, 1)

        visible = True
        if visible_widget:
            checkbox = visible_widget.findChild(QCheckBox)
            if checkbox:
                visible = checkbox.isChecked()

        return {
            "column": column_widget.currentText(),
            "label": label_item.text() if label_item else "",
            "color": color_widget.color(),
            "linestyle": linestyle_widget.linestyle(),
            "marker": marker_widget.marker(),
            "linewidth": width_widget.value(),
            "visible": visible,
        }

    def _on_cell_changed(self, row: int, column: int):
        if self._updating or column != 1:
            return

        self.series_changed.emit()

    def _on_widget_changed(self, _row: int):
        if self._updating:
            return

        self.series_changed.emit()

    def _on_remove(self):
        row = self.table.currentRow()

        if row < 0:
            return

        self.remove_requested.emit(row)

    def remove_row(self, row: int):
        if row < 0 or row >= self.table.rowCount():
            return

        self._updating = True
        self.table.removeRow(row)
        self._updating = False

        self.series_changed.emit()

    def clear(self):
        self._updating = True
        self.table.setRowCount(0)
        self._updating = False
