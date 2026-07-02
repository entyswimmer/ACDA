from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget


class ColumnSelector(QWidget):

    column_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Column"))

        self.combo = QComboBox()
        self.combo.setMinimumHeight(36)
        self.combo.currentTextChanged.connect(
            self._on_column_changed
        )

        layout.addWidget(self.combo)

    def set_columns(self, columns: list[str]):
        current = self.combo.currentText()

        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.addItems(columns)

        if current in columns:
            self.combo.setCurrentText(current)
        elif columns:
            self.combo.setCurrentIndex(0)

        self.combo.blockSignals(False)

    def current_column(self) -> str:
        return self.combo.currentText()

    def set_current_column(self, column: str):
        index = self.combo.findText(column)

        if index >= 0:
            self.combo.setCurrentIndex(index)

    def clear(self):
        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.blockSignals(False)

    def _on_column_changed(self, column: str):
        if column:
            self.column_changed.emit(column)
