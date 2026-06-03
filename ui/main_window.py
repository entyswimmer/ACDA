from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget
)

from services.model_loader import ModelLoader
from services.formula_registry import FormulaRegistry
from services.formula_executor import FormulaExecutor
from services.default_value_provider import DefaultValueProvider
from services.device_resolver import DeviceResolver
from services.validator import Validator
from services.parser import Parser

from panels.device_panel import DevicePanel
from panels.formula_panel import FormulaPanel
from panels.result_panel import ResultPanel
from panels.expression_panel import ExpressionPanel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Analog Circuit Design Assist"
        )

        self.resize(
            1200,
            800
        )

        # -------------------------
        # Services
        # -------------------------

        self.registry = FormulaRegistry()

        self.executor = FormulaExecutor()

        self.device_resolver = DeviceResolver()

        self.validator = Validator()

        self.parser = Parser()

        self.model_loader = ModelLoader()

        self.default_provider = (
            DefaultValueProvider(
                self.registry,
                self.device_resolver
            )
        )

        # -------------------------
        # Device Model
        # -------------------------

        self.device = (
            self.model_loader.load(
                "data/razavi_level1.yaml"
            )
        )

        # -------------------------
        # UI
        # -------------------------

        self._build_ui()

        self._connect_signals()

    def _build_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        root = QVBoxLayout()

        central.setLayout(
            root
        )

        self.tabs = QTabWidget()

        root.addWidget(
            self.tabs
        )

        # =====================================
        # Formula Calculator
        # =====================================

        formula_tab = QWidget()

        formula_layout = QVBoxLayout()

        formula_tab.setLayout(
            formula_layout
        )

        self.device_panel = DevicePanel(
            self.device,
            self.device_resolver
        )

        self.formula_panel = FormulaPanel(
            self.registry
        )

        self.result_panel = ResultPanel()

        formula_layout.addWidget(
            self.device_panel
        )

        formula_layout.addWidget(
            self.formula_panel
        )

        formula_layout.addWidget(
            self.result_panel
        )

        self.tabs.addTab(
            formula_tab,
            "Formula"
        )

        # =====================================
        # Expression Calculator
        # =====================================

        expression_tab = QWidget()

        expression_layout = QVBoxLayout()

        expression_tab.setLayout(
            expression_layout
        )

        self.expression_panel = (
            ExpressionPanel()
        )

        self.expression_result_panel = (
            ResultPanel()
        )

        expression_layout.addWidget(
            self.expression_panel
        )

        expression_layout.addWidget(
            self.expression_result_panel
        )

        self.tabs.addTab(
            expression_tab,
            "Expression"
        )

    def _connect_signals(self):

        self.formula_panel.formula_selected.connect(
            self.on_formula_selected
        )

        self.formula_panel.calculate_requested.connect(
            self.on_calculate
        )

        self.expression_panel.evaluate_requested.connect(
            self.on_expression_evaluate
        )

    # =====================================
    # Formula Selection
    # =====================================

    def on_formula_selected(
        self,
        formula_key
    ):

        try:

            meta = self.registry.get(
                formula_key
            )

            device_type = (
                self.device_panel.selected_device()
            )

            defaults = (
                self.default_provider.get_defaults(
                    formula_key=formula_key,
                    device=self.device,
                    device_type=device_type
                )
            )

            self.formula_panel.load_formula(
                meta,
                defaults
            )

        except Exception as e:

            self.result_panel.show_error(
                str(e)
            )

    # =====================================
    # Formula Calculate
    # =====================================

    def on_calculate(
        self,
        formula_key,
        values
    ):

        try:

            meta = self.registry.get(
                formula_key
            )

            self.validator.validate(
                formula_key,
                meta,
                values
            )

            result = (
                self.executor.call(
                    meta,
                    values
                )
            )

            self.result_panel.show_result(
                meta["name"],
                result,
                meta["unit"]
            )

        except Exception as e:

            self.result_panel.show_error(
                str(e)
            )

    # =====================================
    # Expression
    # =====================================

    def on_expression_evaluate(
        self,
        expression
    ):

        try:

            self.validator.validate_expression(
                expression
            )

            result = (
                self.parser.parse(
                    expression
                )
            )

            self.expression_result_panel.show_result(
                "Expression",
                result
            )

        except Exception as e:

            self.expression_result_panel.show_error(
                str(e)
            )