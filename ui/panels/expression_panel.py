from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QGroupBox
)


class ExpressionPanel(QWidget):

    evaluate_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        group = QGroupBox(
            "Expression Calculator"
        )

        layout.addWidget(group)

        group_layout = QVBoxLayout(
            group
        )

        # ------------------
        # Expression
        # ------------------

        group_layout.addWidget(
            QLabel("Expression")
        )

        self.expression_edit = (
            QTextEdit()
        )

        self.expression_edit.setPlaceholderText(
            "2k + 3k\nsqrt(4)\n10u * 100k"
        )
        self.expression_edit.setMinimumHeight(
            160
        )

        group_layout.addWidget(
            self.expression_edit,
            stretch=1,
        )

        # ------------------
        # Evaluate
        # ------------------

        self.evaluate_button = (
            QPushButton(
                "Evaluate"
            )
        )

        group_layout.addWidget(
            self.evaluate_button
        )

        self.evaluate_button.clicked.connect(
            self._on_evaluate
        )

    def _on_evaluate(self):

        expr = self.expression()

        if expr:

            self.evaluate_requested.emit(
                expr
            )

    def expression(self) -> str:

        return (
            self.expression_edit
            .toPlainText()
            .strip()
        )

    def set_expression(
        self,
        expr: str
    ):

        self.expression_edit.setPlainText(
            expr
        )

    def clear(self):

        self.expression_edit.clear()