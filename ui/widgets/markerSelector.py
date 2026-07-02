from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox


MARKERS = [
    ("None", None),
    ("Circle", "o"),
    ("Square", "s"),
    ("Triangle", "^"),
    ("Diamond", "D"),
    ("Cross", "x"),
    ("Plus", "+"),
]


class MarkerSelector(QComboBox):

    marker_changed = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._markers: list = []
        self.setMinimumHeight(36)

        for label, marker in MARKERS:
            self.addItem(label)
            self._markers.append(marker)

        self.currentIndexChanged.connect(
            self._on_index_changed
        )

    def marker(self):
        index = self.currentIndex()

        if index < 0:
            return None

        return self._markers[index]

    def set_marker(self, marker):
        try:
            index = self._markers.index(marker)
        except ValueError:
            index = 0

        self.setCurrentIndex(index)

    def _on_index_changed(self, _index: int):
        self.marker_changed.emit(self.marker())
