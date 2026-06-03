from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox
)

from ui.widgets.result_view import (
    ResultView
)


class ResultPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(150) #変更
        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        group = QGroupBox(
            "Result"
        )

        layout.addWidget(group)

        group_layout = QVBoxLayout(
            group
        )

        self.result_view = (
            ResultView()
        )

        group_layout.addWidget(
            self.result_view
        )

    def show_result(
        self,
        formula_name: str,
        value,
        unit: str = ""
    ):

        self.result_view.show_formula_result(
            formula_name,
            value,
            unit
        )

    def show_error(
        self,
        message: str
    ):

        self.result_view.show_error(
            message
        )

    def clear(self):

        self.result_view.clear()