from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class VariableTable(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        self.table = QTableWidget(
            0,
            2
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Variable",
                "Value"
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(
            self.table
        )

        self.add_button = QPushButton(
            "Add Variable"
        )

        layout.addWidget(
            self.add_button
        )

        self.add_button.clicked.connect(
            self.add_row
        )

    def add_row(self):

        row = self.table.rowCount()

        self.table.insertRow(row)

    def clear(self):

        self.table.setRowCount(0)

    def variables(self) -> dict:

        result = {}

        for row in range(
            self.table.rowCount()
        ):

            name_item = (
                self.table.item(
                    row,
                    0
                )
            )

            value_item = (
                self.table.item(
                    row,
                    1
                )
            )

            if (
                name_item is None
                or value_item is None
            ):
                continue

            name = (
                name_item.text()
                .strip()
            )

            value_text = (
                value_item.text()
                .strip()
            )

            if not name:
                continue

            result[name] = value_text

        return result

    def set_variables(
        self,
        variables: dict
    ):

        self.clear()

        for name, value in (
            variables.items()
        ):

            row = self.table.rowCount()

            self.table.insertRow(
                row
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(name)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(value)
                )
            )