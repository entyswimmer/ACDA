from pathlib import Path

from services.plotDataLoader import PlotDataLoader
from plots.selectPlotSetting import (
    SelectPlotSetting,
    SubPlotSetting,
)


class ProjectController:

    def __init__(self):
        self.loader = PlotDataLoader()
        self.setting = SelectPlotSetting()
        self.current_file: str | None = None
        self.recent_files: list[str] = []

        self._series_meta: list[dict] = []
        self._x_column: str | None = None

    @property
    def is_loaded(self) -> bool:
        return self.loader.df is not None

    def get_columns(self) -> list[str]:
        if not self.is_loaded:
            return []

        return self.loader.get_columns()

    def get_column_data(self, column: str):
        return self.loader.get_column(column)

    def get_setting(self) -> SelectPlotSetting:
        return self.setting

    def get_subplot(self) -> SubPlotSetting | None:
        subplots = self.setting.get_subplots()

        if not subplots:
            return None

        return subplots[0]

    def get_series_meta(self) -> list[dict]:
        return list(self._series_meta)

    def set_series_meta(self, meta: list[dict]):
        self._series_meta = list(meta)

    def clear(self):
        self.loader = PlotDataLoader()
        self.setting.clear()
        self.current_file = None
        self._series_meta = []
        self._x_column = None

    def _ensure_subplot(self) -> SubPlotSetting:
        subplots = self.setting.get_subplots()

        if subplots:
            return subplots[0]

        self.setting.set_layout(1, 1)

        subplot = SubPlotSetting()
        self.setting.add_subplot(subplot)

        return subplot

    def load_file(self, file_path: str):
        path = str(Path(file_path))

        self.loader.load(path)
        self.current_file = path
        self._add_recent(path)

        columns = self.get_columns()

        self.setting.clear()
        self.setting.set_layout(1, 1)

        subplot = SubPlotSetting()

        if columns:
            x_column = columns[0]
            self._x_column = x_column
            subplot.x_data = self.get_column_data(x_column)
            subplot.x_label = x_column

        self.setting.add_subplot(subplot)
        self._series_meta = []

    def reload(self):
        if not self.current_file:
            raise RuntimeError("No file is loaded.")

        saved_meta = list(self._series_meta)
        saved_x = self._x_column
        subplot = self.get_subplot()

        saved_subplot = None
        saved_axis = None

        if subplot:
            saved_subplot = {
                "title": subplot.title,
                "x_label": subplot.x_label,
                "y_label": subplot.y_label,
                "x_unit": subplot.x_unit,
                "y_unit": subplot.y_unit,
                "legend": subplot.legend,
            }
            saved_axis = {
                "xmin": subplot.xmin,
                "xmax": subplot.xmax,
                "ymin": subplot.ymin,
                "ymax": subplot.ymax,
                "x_scale": subplot.x_scale,
                "y_scale": subplot.y_scale,
                "grid_x": subplot.grid_x,
                "grid_y": subplot.grid_y,
            }

        self.load_file(self.current_file)

        columns = self.get_columns()

        if saved_x and saved_x in columns:
            self.set_x_column(saved_x)
        elif columns:
            self.set_x_column(columns[0])

        if saved_meta:
            self.set_series_meta(saved_meta)
            self.apply_series_meta()

        subplot = self.get_subplot()

        if subplot and saved_subplot:
            for key, value in saved_subplot.items():
                setattr(subplot, key, value)

        if subplot and saved_axis:
            for key, value in saved_axis.items():
                setattr(subplot, key, value)

    def set_x_column(self, column: str):
        self._x_column = column

        subplot = self._ensure_subplot()
        subplot.x_data = self.get_column_data(column)

        if not subplot.x_label:
            subplot.x_label = column

    def get_x_column(self) -> str | None:
        return self._x_column

    def apply_series_meta(self):
        subplot = self._ensure_subplot()
        subplot.series.clear()

        y_unit = subplot.y_unit or ""

        for meta in self._series_meta:
            column = meta.get("column", "")

            if not column:
                continue

            subplot.add_series(
                data=self.get_column_data(column),
                label=meta.get("label") or column,
                unit=y_unit,
                color=meta.get("color"),
                linestyle=meta.get("linestyle", "-"),
                marker=meta.get("marker"),
                linewidth=meta.get("linewidth", 2.0),
                visible=meta.get("visible", True),
            )

    def apply_subplot_settings(
        self,
        *,
        title: str,
        x_label: str,
        y_label: str,
        x_unit: str,
        y_unit: str,
        legend: bool,
    ):
        subplot = self._ensure_subplot()

        subplot.title = title
        subplot.x_label = x_label
        subplot.y_label = y_label
        subplot.x_unit = x_unit
        subplot.y_unit = y_unit
        subplot.legend = legend

    def apply_axis_settings(
        self,
        *,
        xmin,
        xmax,
        ymin,
        ymax,
        x_scale: str,
        y_scale: str,
        grid_x: bool,
        grid_y: bool,
    ):
        subplot = self._ensure_subplot()

        subplot.xmin = xmin
        subplot.xmax = xmax
        subplot.ymin = ymin
        subplot.ymax = ymax
        subplot.x_scale = x_scale
        subplot.y_scale = y_scale
        subplot.grid_x = grid_x
        subplot.grid_y = grid_y

    def _add_recent(self, path: str):
        if path in self.recent_files:
            self.recent_files.remove(path)

        self.recent_files.insert(0, path)
        self.recent_files = self.recent_files[:10]
