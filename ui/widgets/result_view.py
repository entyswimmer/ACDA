from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit
)

from services.unit_converter import UnitConverter


class ResultView(QWidget):

    def __init__(self):
        super().__init__()

        self._formatter = UnitConverter()

        self._text = QTextEdit()

        self._text.setReadOnly(True)

        layout = QVBoxLayout()

        layout.addWidget(
            self._text
        )

        self.setLayout(layout)

    def show_result(
        self,
        value,
        unit: str = ""
    ):

        formatted = self._formatter.format_value(
            value
        )

        if unit:

            text = f"{formatted} {unit}"

        else:

            text = formatted

        self._text.setPlainText(
            text
        )

    def show_formula_result(
        self,
        formula_name: str,
        value,
        unit: str = ""
    ):

        formatted = self._formatter.format_value(
            value
        )

        if unit:

            text = (
                f"{formula_name} = "
                f"{formatted} {unit}"
            )

        else:

            text = (
                f"{formula_name} = "
                f"{formatted}"
            )

        self._text.setPlainText(
            text
        )

    def show_error(
        self,
        message: str
    ):

        self._text.setPlainText(
            f"Error: {message}"
        )

    def clear(self):

        self._text.clear()