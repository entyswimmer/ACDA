from PySide6.QtCore import Signal, Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox,
    QScrollArea,
    QSizePolicy,
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
        layout.setContentsMargins(0, 0, 0, 0)

        group = QGroupBox(
            "Formula"
        )
        group.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
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

        formula_tree = QScrollArea()
        formula_tree.setWidget(
            self.formula_tree
        )
        formula_tree.setWidgetResizable(
            True
        )
        formula_tree.setFrameShape(
            QScrollArea.Shape.NoFrame
        )
        formula_tree.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        formula_tree.setMinimumHeight(
            540
        )
        
        group_layout.addWidget(
            self.formula_tree,
            stretch=2,
        )

        # --------------------
        # Input Form
        # --------------------

        self.input_form = (
            InputForm()
        )

        input_scroll = QScrollArea()
        input_scroll.setWidget(
            self.input_form
        )
        input_scroll.setWidgetResizable(
            True
        )
        input_scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )
        input_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        input_scroll.setMinimumHeight(
            340
        )

        group_layout.addWidget(
            input_scroll,
            stretch=1,
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