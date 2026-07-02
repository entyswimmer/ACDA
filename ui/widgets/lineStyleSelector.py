from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox


LINE_STYLES = [
    ("Solid", "-"),
    ("Dashed", "--"),
    ("Dash-Dot", "-."),
    ("Dotted", ":"),
]


class LineStyleSelector(QComboBox):

    style_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._styles: list[str] = []
        self.setMinimumHeight(36)

        for label, style in LINE_STYLES:
            self.addItem(label)
            self._styles.append(style)

        self.currentIndexChanged.connect(
            self._on_index_changed
        )

    def linestyle(self) -> str:
        index = self.currentIndex()

        if index < 0:
            return "-"

        return self._styles[index]

    def set_linestyle(self, style: str):
        try:
            index = self._styles.index(style)
        except ValueError:
            index = 0

        self.setCurrentIndex(index)

    def _on_index_changed(self, _index: int):
        self.style_changed.emit(self.linestyle())
