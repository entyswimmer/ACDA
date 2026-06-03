from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget


def make_scroll_area(
    widget: QWidget,
    *,
    min_width: int = 0,
    min_height: int = 0,
) -> QScrollArea:

    scroll = QScrollArea()

    scroll.setWidget(widget)
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(
        QScrollArea.Shape.NoFrame
    )
    scroll.setHorizontalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    )
    scroll.setVerticalScrollBarPolicy(
        Qt.ScrollBarPolicy.ScrollBarAsNeeded
    )

    if min_width:
        widget.setMinimumWidth(min_width)

    if min_height:
        scroll.setMinimumHeight(min_height)

    return scroll
