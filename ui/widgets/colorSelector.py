from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QColorDialog


DEFAULT_COLORS = [
    "#3B82F6",
    "#EF4444",
    "#22C55E",
    "#F59E0B",
    "#8B5CF6",
    "#EC4899",
    "#06B6D4",
    "#64748B",
]


class ColorSelector(QPushButton):

    color_changed = Signal(str)

    def __init__(
        self,
        color: str = "#3B82F6",
        parent=None,
    ):
        super().__init__(parent)

        self._color = color
        self.setMinimumSize(36, 36)
        self.setMaximumSize(36, 36)
        self.clicked.connect(self._pick_color)
        self._apply_style()

    def color(self) -> str:
        return self._color

    def set_color(self, color: str):
        if not color:
            color = DEFAULT_COLORS[0]

        self._color = color
        self._apply_style()
        self.color_changed.emit(self._color)

    def _apply_style(self):
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self._color};
                border: 2px solid #E2E8F0;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                border: 2px solid #3B82F6;
            }}
            """
        )

    def _pick_color(self):
        picked = QColorDialog.getColor(
            QColor(self._color),
            self,
            "Select Color",
        )

        if picked.isValid():
            self.set_color(picked.name())
