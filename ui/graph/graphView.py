from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)
from PySide6.QtCore import Qt


class GraphView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._canvas = None

        self._build_ui()

    def _build_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)

        self.placeholder = QLabel("Open a CSV / VCSV file to display a graph")
        self.placeholder.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.placeholder.setStyleSheet(
            """
            QLabel {
                color: #64748B;
                font-size: 16px;
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 48px;
            }
            """
        )
        self.placeholder.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.layout.addWidget(self.placeholder)

    def set_canvas(self, canvas):
        if self._canvas is not None:
            self.layout.removeWidget(self._canvas)
            self._canvas.setParent(None)

        self._canvas = canvas

        if canvas is None:
            self.placeholder.show()
            return

        self.placeholder.hide()
        self.layout.addWidget(canvas)

    def clear(self):
        self.set_canvas(None)
        self.placeholder.show()
