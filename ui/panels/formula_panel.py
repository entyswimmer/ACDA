from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox
)

from ui.widgets.formula_tree import (
    FormulaTree
)

from ui.widgets.input_form import (
    InputForm
)


class FormulaPanel(QWidget):

    formula_selected = Signal(str)

    calculate_requested = Signal(
        str,
        dict
    )

    def __init__(
        self,
        registry
    ):
        super().__init__()

        self.registry = registry

        self.current_formula = None

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        group = QGroupBox(
            "Formula"
        )

        layout.addWidget(group)

        group_layout = QVBoxLayout(
            group
        )

        # --------------------
        # Formula Tree
        # --------------------

        self.formula_tree = (
            FormulaTree(
                self.registry
            )
        )

        group_layout.addWidget(
            self.formula_tree
        )

        # --------------------
        # Input Form
        # --------------------

        self.input_form = (
            InputForm()
        )

        group_layout.addWidget(
            self.input_form
        )

        # --------------------
        # Calculate
        # --------------------

        self.calculate_button = (
            QPushButton(
                "Calculate"
            )
        )

        group_layout.addWidget(
            self.calculate_button
        )

        # --------------------
        # Signal
        # --------------------

        self.formula_tree.formula_selected.connect(
            self._on_formula_selected
        )

        self.calculate_button.clicked.connect(
            self._on_calculate
        )

    def _on_formula_selected(
        self,
        formula_key
    ):

        self.current_formula = (
            formula_key
        )

        self.formula_selected.emit(
            formula_key
        )

    def _on_calculate(self):

        if not self.current_formula:
            return

        values = (
            self.input_form.values()
        )

        self.calculate_requested.emit(
            self.current_formula,
            values
        )

    def load_formula(
        self,
        meta,
        defaults
    ):

        self.input_form.build(
            meta,
            defaults
        )