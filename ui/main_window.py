from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QSplitter,
)

from ui.widgets.scroll_area import make_scroll_area

from services.model_loader import ModelLoader
from services.formula_registry import FormulaRegistry
from services.formula_executor import FormulaExecutor
from services.default_value_provider import DefaultValueProvider
from services.device_resolver import DeviceResolver
from services.validator import Validator
from services.parser import Parser

from ui.panels.device_panel import DevicePanel
from ui.panels.formula_panel import FormulaPanel
from ui.panels.result_panel import ResultPanel
from ui.panels.expression_panel import ExpressionPanel

from ui.graph.graphView import GraphView
from ui.graph.graphToolBox import GraphToolBox

from controller.projectController import ProjectController
from controller.graphController import GraphController
from controller.fileController import FileController

from utils.paths import DATA_DIR

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
                DATA_DIR/"razavi_level1.yaml"
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
        self.tabs.setUsesScrollButtons(
            False
        )

        root.addWidget(
            self.tabs
        )

        # =====================================
        # Formula Calculator
        # =====================================

        formula_tab = QWidget()

        formula_layout = QVBoxLayout(
            formula_tab
        )
        formula_layout.setContentsMargins(
            8,
            8,
            8,
            8
        )

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.device_panel = DevicePanel(
            self.device,
            self.device_resolver
        )

        device_scroll = make_scroll_area(
            self.device_panel,
            min_width=320,
        )

        right_splitter = QSplitter(
            Qt.Orientation.Vertical
        )

        right_splitter.setChildrenCollapsible(
            False
        )

        self.formula_panel = FormulaPanel(
            self.registry
        )

        self.result_panel = ResultPanel()

        right_splitter.addWidget(
            self.formula_panel
        )

        right_splitter.addWidget(
            self.result_panel
        )

        right_splitter.setStretchFactor(
            0,
            3
        )

        right_splitter.setStretchFactor(
            1,
            1
        )

        right_splitter.setSizes(
            [600, 200]
        )

        right_scroll = make_scroll_area(
            right_splitter,
            min_width=480,
        )

        splitter.addWidget(
            device_scroll
        )
        splitter.addWidget(
            right_scroll
        )
        splitter.setStretchFactor(
            0,
            0,
        )
        splitter.setStretchFactor(
            1,
            1,
        )
        splitter.setSizes(
            [360, 820]
        )

        formula_layout.addWidget(
            splitter
        )

        self.tabs.addTab(
            formula_tab,
            "Formula"
        )

        # =====================================
        # Expression Calculator
        # =====================================

        expression_tab = QWidget()

        expression_layout = QVBoxLayout(
            expression_tab
        )
        expression_layout.setContentsMargins(
            8,
            8,
            8,
            8
        )

        self.expression_panel = (
            ExpressionPanel()
        )

        self.expression_result_panel = (
            ResultPanel()
        )

        expression_content = QWidget()

        expression_content_layout = (
            QVBoxLayout(
                expression_content
            )
        )
        expression_content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        expression_content_layout.addWidget(
            self.expression_panel,
            stretch=2,
        )

        expression_content_layout.addWidget(
            self.expression_result_panel,
            stretch=1,
        )

        expression_scroll = make_scroll_area(
            expression_content,
            min_width=560,
        )

        expression_layout.addWidget(
            expression_scroll
        )

        self.tabs.addTab(
            expression_tab,
            "Expression"
        )

        # =====================================
        # Graph
        # =====================================

        graph_tab = QWidget()

        graph_layout = QVBoxLayout(
            graph_tab
        )
        graph_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        graph_splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.graph_project = ProjectController()

        self.graph_tool_box = GraphToolBox()
        self.graph_view = GraphView()

        self.graph_controller = GraphController(
            self.graph_project,
            self.graph_view,
            self.graph_tool_box,
        )

        self.file_controller = FileController(
            self.graph_project,
            self.graph_controller,
            self.graph_tool_box,
            parent=self,
        )

        tool_box_scroll = make_scroll_area(
            self.graph_tool_box,
            min_width=360,
        )

        graph_splitter.addWidget(
            tool_box_scroll
        )
        graph_splitter.addWidget(
            self.graph_view
        )
        graph_splitter.setStretchFactor(
            0,
            0,
        )
        graph_splitter.setStretchFactor(
            1,
            1,
        )
        graph_splitter.setSizes(
            [380, 820]
        )

        graph_layout.addWidget(
            graph_splitter
        )

        self.tabs.addTab(
            graph_tab,
            "Graph"
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