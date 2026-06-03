from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QLabel
)

from services.parser import Parser


class InputForm(QWidget):

    def __init__(self):
        super().__init__()

        self._fields = {}

        self._layout = QFormLayout()

        self.setLayout(
            self._layout
        )

        self.parser = Parser()

    def build(
        self,
        meta: dict,
        defaults: dict | None = None
    ):

        self.clear()

        defaults = defaults or {}

        for item in meta["inputs"]:

            name = item["name"]

            line_edit = QLineEdit()

            if name in defaults:

                value = defaults[name]

                if value is not None:

                    line_edit.setText(
                        str(value)
                    )

            if item.get("type") == "variadic":

                line_edit.setPlaceholderText(
                    "1k, 2k, 3k"
                )

            self._layout.addRow(
                QLabel(name),
                line_edit
            )

            self._fields[name] = {
                "widget": line_edit,
                "meta": item
            }

    def values(self):

        result = {}

        for name, info in self._fields.items():

            widget = info["widget"]
            meta = info["meta"]

            text = widget.text().strip()

            if text == "":
                continue

            # ------------------
            # variadic
            # ------------------

            if meta.get("type") == "variadic":

                result[name] = [
                    self.parser.parse(value.strip())
                    for value in text.split(",")
                    if value.strip()
                ]

            # ------------------
            # normal
            # ------------------

            else:

                result[name] = (
                    self.parser.parse(text)
                )

        return result

    def clear(self):

        while self._layout.rowCount():

            self._layout.removeRow(0)

        self._fields.clear()