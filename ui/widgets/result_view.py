from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit
)


class ResultView(QWidget):

    def __init__(self):
        super().__init__()

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

        if unit:

            text = f"{value} {unit}"

        else:

            text = str(value)

        self._text.setPlainText(
            text
        )

    def show_formula_result(
        self,
        formula_name: str,
        value,
        unit: str = ""
    ):

        if unit:

            text = (
                f"{formula_name} = "
                f"{value} {unit}"
            )

        else:

            text = (
                f"{formula_name} = "
                f"{value}"
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