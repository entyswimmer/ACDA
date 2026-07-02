from PySide6.QtWidgets import QFileDialog, QMessageBox


class FileController:

    FILE_FILTER = (
        "Data Files (*.csv *.vcsv);;"
        "CSV Files (*.csv);;"
        "VCSV Files (*.vcsv);;"
        "All Files (*)"
    )

    def __init__(
        self,
        project,
        graph_controller,
        tool_box,
        parent=None,
    ):
        self.project = project
        self.graph_controller = graph_controller
        self.tool_box = tool_box
        self.parent = parent

        self._connect_signals()

    def _connect_signals(self):
        self.tool_box.open_button.clicked.connect(
            self.open_file
        )
        self.tool_box.reload_button.clicked.connect(
            self.reload_file
        )
        self.tool_box.export_button.clicked.connect(
            self.export_png
        )

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Open Data File",
            "",
            self.FILE_FILTER,
        )

        if not path:
            return

        try:
            self.project.load_file(path)
            self.graph_controller.sync_from_project()
            self.graph_controller.refresh()
        except Exception as error:
            self._show_error(str(error))

    def reload_file(self):
        if not self.project.current_file:
            self._show_error("No file is loaded.")
            return

        try:
            self.project.reload()
            self.graph_controller.sync_from_project()
            self.graph_controller.refresh()
        except Exception as error:
            self._show_error(str(error))

    def export_png(self):
        if not self.project.is_loaded:
            self._show_error("Load a file before exporting.")
            return

        default_name = "graph.png"

        if self.project.current_file:
            default_name = (
                Path(self.project.current_file).stem
                + ".png"
            )

        path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Export PNG",
            default_name,
            "PNG Files (*.png)",
        )

        if not path:
            return

        if not path.lower().endswith(".png"):
            path += ".png"

        try:
            self.graph_controller.make_graph.save_png(path)
        except Exception as error:
            self._show_error(str(error))

    def _show_error(self, message: str):
        QMessageBox.warning(
            self.parent,
            "Graph",
            message,
        )
