from plots.makeGraph import MakeGraph


class GraphController:

    def __init__(
        self,
        project,
        graph_view,
        tool_box,
    ):
        self.project = project
        self.graph_view = graph_view
        self.tool_box = tool_box

        self.make_graph = MakeGraph()

        self._connect_signals()

    def _connect_signals(self):
        toolbox = self.tool_box

        toolbox.x_column.column_changed.connect(
            self._on_x_column_changed
        )

        toolbox.series_editor.series_changed.connect(
            self._on_series_changed
        )
        toolbox.series_editor.add_requested.connect(
            self._on_add_series
        )
        toolbox.series_editor.remove_requested.connect(
            self._on_remove_series
        )

        toolbox.subplot_editor.settings_changed.connect(
            self._on_subplot_changed
        )
        toolbox.axis_editor.settings_changed.connect(
            self._on_axis_changed
        )

    def sync_from_project(self):
        toolbox = self.tool_box
        columns = self.project.get_columns()
        subplot = self.project.get_subplot()

        toolbox.set_file_path(self.project.current_file)
        toolbox.set_columns(columns)

        if not columns:
            toolbox.series_editor.clear()
            return

        x_column = (
            self.project.get_x_column()
            or (columns[0] if columns else "")
        )

        toolbox.x_column.set_current_column(x_column)

        series_meta = self.project.get_series_meta()

        if not series_meta and subplot and subplot.series:
            series_meta = [
                {
                    "column": item.label,
                    "label": item.label,
                    "color": item.color,
                    "linestyle": item.linestyle,
                    "marker": item.marker,
                    "linewidth": item.linewidth,
                    "visible": item.visible,
                }
                for item in subplot.series
            ]
            self.project.set_series_meta(series_meta)

        toolbox.series_editor.load_series(series_meta)

        if subplot:
            toolbox.subplot_editor.load_settings(
                title=subplot.title,
                x_label=subplot.x_label,
                y_label=subplot.y_label,
                x_unit=subplot.x_unit,
                y_unit=subplot.y_unit,
                legend=subplot.legend,
            )
            toolbox.axis_editor.load_settings(
                xmin=subplot.xmin,
                xmax=subplot.xmax,
                ymin=subplot.ymin,
                ymax=subplot.ymax,
                x_scale=subplot.x_scale,
                y_scale=subplot.y_scale,
                grid_x=subplot.grid_x,
                grid_y=subplot.grid_y,
            )

    def refresh(self):
        if not self.project.is_loaded:
            self.graph_view.clear()
            return

        setting = self.project.get_setting()
        self.make_graph.draw(setting)

        if self.graph_view._canvas is None:
            self.graph_view.set_canvas(
                self.make_graph.get_canvas()
            )

    def _apply_ui_to_project(self):
        toolbox = self.tool_box

        self.project.set_x_column(
            toolbox.x_column.current_column()
        )

        series_meta = toolbox.series_editor.series_data()
        self.project.set_series_meta(series_meta)

        subplot = toolbox.subplot_editor
        self.project.apply_subplot_settings(
            title=subplot.title(),
            x_label=subplot.x_label(),
            y_label=subplot.y_label(),
            x_unit=subplot.x_unit_prefix(),
            y_unit=subplot.y_unit_prefix(),
            legend=subplot.legend(),
        )

        self.project.apply_series_meta()

        axis = toolbox.axis_editor
        self.project.apply_axis_settings(
            xmin=axis.xmin(),
            xmax=axis.xmax(),
            ymin=axis.ymin(),
            ymax=axis.ymax(),
            x_scale=axis.x_scale_value(),
            y_scale=axis.y_scale_value(),
            grid_x=axis.grid_x_enabled(),
            grid_y=axis.grid_y_enabled(),
        )

    def _on_x_column_changed(self, column: str):
        self.project.set_x_column(column)
        self.refresh()

    def _on_series_changed(self):
        self._apply_ui_to_project()
        self.refresh()

    def _on_add_series(self):
        columns = self.project.get_columns()
        x_column = self.tool_box.x_column.current_column()

        default_column = ""
        for column in columns:
            if column != x_column:
                default_column = column
                break

        if not default_column and columns:
            default_column = columns[0]

        self.tool_box.series_editor.add_empty_series(
            default_column
        )
        self._on_series_changed()

    def _on_remove_series(self, row: int):
        self.tool_box.series_editor.remove_row(row)
        self._on_series_changed()

    def _on_subplot_changed(self):
        self._apply_ui_to_project()
        self.refresh()

    def _on_axis_changed(self):
        self._apply_ui_to_project()
        self.refresh()
