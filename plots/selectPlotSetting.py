from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class PlotSeries:
    """
    1本のプロット系列
    """
    data: np.ndarray
    label: str
    unit: str = ""
    color: Optional[str] = None
    linestyle: str = "-"
    marker: Optional[str] = None
    linewidth: float = 2.0
    alpha: float = 1.0
    visible: bool = True
    plot_type: str = "line"     

@dataclass
class SubPlotSetting:
    x_data: Optional[np.ndarray] = None
    x_label: str = ""
    x_unit: str = ""
    y_label: str = ""
    y_unit: str = ""
    title: str = ""
    series: list[PlotSeries] = field(default_factory=list)
    legend: bool = True
    grid_x: bool = False
    grid_y: bool = False
    x_scale: str = "linear"
    y_scale: str = "linear"
    xmin: float | None = None
    xmax: float | None = None
    ymin: float | None = None
    ymax: float | None = None

    def add_series(
        self,
        data,
        label,
        unit="",
        color=None,
        linestyle="-",
        marker=None,
        linewidth=2.0,
        alpha=1.0,
        visible=True,
        plot_type="line",
    ):
        self.series.append(
            PlotSeries(
                data=data,
                label=label,
                unit=unit,
                color=color,
                linestyle=linestyle,
                marker=marker,
                linewidth=linewidth,
                alpha=alpha,
                visible=visible,
                plot_type=plot_type,
            )
        )

    def remove_series(self, index: int):
        del self.series[index]

class SelectPlotSetting:
    """
    グラフ描画設定クラス
    """

    def __init__(self):
        self.clear()

    # ==========================================================
    # 初期化
    # ==========================================================

    def clear(self):
        self.rows = 1
        self.cols = 1

        self.subplots: list[SubPlotSetting] = []

    
    # ==========================================================
    # Layout
    # ==========================================================

    def set_layout(
        self,
        rows=1,
        cols=1,
    ):
        self.rows = rows
        self.cols = cols


    # ==========================================================
    # SubPlot
    # ==========================================================

    def add_subplot(
        self,
        subplot: SubPlotSetting,
    ):
        self.subplots.append(subplot)


    def remove_subplot(
        self,
        index: int,
    ):
        del self.subplots[index]


    def clear_subplot(self):
        self.subplots.clear()


    # ==========================================================
    # Subplot_Getter
    # ==========================================================

    def get_rows(self):
        return self.rows


    def get_cols(self):
        return self.cols


    def get_subplots(self):
        return self.subplots