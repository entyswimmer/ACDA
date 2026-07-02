from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)

from ui.graph.columnSelector import ColumnSelector
from ui.graph.seriesEditor import SeriesEditor
from ui.graph.subplotEditor import SubplotEditor
from ui.graph.axisEditor import AxisEditor


class GraphToolBox(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # -------------------------
        # File
        # -------------------------

        file_group = QGroupBox("File")
        file_layout = QVBoxLayout(file_group)

        self.file_label = QLabel("No file loaded")
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet(
            "color: #64748B; font-weight: normal;"
        )
        file_layout.addWidget(self.file_label)

        file_buttons = QHBoxLayout()

        self.open_button = QPushButton("Open CSV")
        self.reload_button = QPushButton("Reload")
        self.export_button = QPushButton("Export PNG")

        file_buttons.addWidget(self.open_button)
        file_buttons.addWidget(self.reload_button)
        file_buttons.addWidget(self.export_button)

        file_layout.addLayout(file_buttons)

        layout.addWidget(file_group)

        # -------------------------
        # Data
        # -------------------------

        data_group = QGroupBox("Data")
        data_group.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )
        data_layout = QVBoxLayout(data_group)

        data_layout.addWidget(QLabel("X Axis"))
        self.x_column = ColumnSelector()
        data_layout.addWidget(self.x_column)

        layout.addWidget(data_group)

        # -------------------------
        # Series
        # -------------------------

        series_group = QGroupBox("Series")
        series_group.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        series_layout = QVBoxLayout(series_group)

        self.series_editor = SeriesEditor()
        series_layout.addWidget(self.series_editor)

        layout.addWidget(series_group, stretch=1)

        # -------------------------
        # Graph
        # -------------------------

        graph_group = QGroupBox("Graph")
        graph_layout = QVBoxLayout(graph_group)

        self.subplot_editor = SubplotEditor()
        graph_layout.addWidget(self.subplot_editor)

        layout.addWidget(graph_group)

        # -------------------------
        # Axis
        # -------------------------

        axis_group = QGroupBox("Axis")
        axis_layout = QVBoxLayout(axis_group)

        self.axis_editor = AxisEditor()
        axis_layout.addWidget(self.axis_editor)

        layout.addWidget(axis_group)

        layout.addStretch()

    def set_file_path(self, path: str | None):
        if path:
            self.file_label.setText(path)
            self.file_label.setStyleSheet(
                "color: #0F172A; font-weight: normal;"
            )
        else:
            self.file_label.setText("No file loaded")
            self.file_label.setStyleSheet(
                "color: #64748B; font-weight: normal;"
            )

    def set_columns(self, columns: list[str]):
        self.x_column.set_columns(columns)
        self.series_editor.set_available_columns(columns)

    def clear(self):
        self.set_file_path(None)
        self.x_column.clear()
        self.series_editor.clear()
        self.series_editor.set_available_columns([])
