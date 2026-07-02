from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox


TIME_UNITS = [
    ("s", ""),
    ("ms", "m"),
    ("µs", "u"),
    ("ns", "n"),
]

VOLTAGE_UNITS = [
    ("V", ""),
    ("mV", "m"),
    ("µV", "u"),
]

CURRENT_UNITS = [
    ("A", ""),
    ("mA", "m"),
    ("µA", "u"),
    ("nA", "n"),
]

GENERIC_UNITS = [
    ("", ""),
    ("k", "k"),
    ("m", "m"),
    ("µ", "u"),
    ("n", "n"),
    ("p", "p"),
]


class UnitSelector(QComboBox):

    prefix_changed = Signal(str)

    def __init__(
        self,
        units=None,
        parent=None,
    ):
        super().__init__(parent)

        self._prefixes: list[str] = []

        self.setMinimumHeight(36)
        self.set_units(units or GENERIC_UNITS)

        self.currentIndexChanged.connect(
            self._on_index_changed
        )

    def set_units(
        self,
        units: list[tuple[str, str]],
    ):
        self.blockSignals(True)

        self.clear()
        self._prefixes.clear()

        for label, prefix in units:
            self.addItem(label)
            self._prefixes.append(prefix)

        self.blockSignals(False)

    def prefix(self) -> str:
        index = self.currentIndex()

        if index < 0:
            return ""

        return self._prefixes[index]

    def set_prefix(self, prefix: str):
        try:
            index = self._prefixes.index(prefix)
        except ValueError:
            index = 0

        self.setCurrentIndex(index)

    def _on_index_changed(self, _index: int):
        self.prefix_changed.emit(self.prefix())
