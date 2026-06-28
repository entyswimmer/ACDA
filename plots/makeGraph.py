from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import numpy as np
from services.unit_converter import UnitConverter


class MakeGraph:
    """
    Matplotlib描画管理クラス

    Responsibilities
    ----------------
    ・Figure生成
    ・Canvas生成
    ・SelectPlotSettingの描画
    ・保存
    """

    def __init__(self):
        self.figure = Figure(
            figsize=(10, 6),
            dpi=100,
            facecolor="white",
        )

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = np.array([])

    # ==========================================================
    # Public
    # ==========================================================

    def get_canvas(self):
        return self.canvas

    def draw(self, setting):
        self.figure.clear()

        rows = setting.get_rows()
        cols = setting.get_cols()

        self.axes = self.figure.subplots(rows, cols)

        if not isinstance(self.axes, np.ndarray):
            self.axes = np.array([self.axes])

        self.axes = self.axes.flatten()

        for ax, subplot in zip(
            self.axes,
            setting.get_subplots(),
        ):
            self._apply_style(ax)
            self._draw_subplot(ax, subplot)

        self.figure.tight_layout(
            pad=1.2,
        )

        self.canvas.draw()

    # ==========================================================
    # Private
    # ==========================================================

    def _apply_style(
        self,
        ax,
    ):
        ax.spines["top"].set_visible(True)
        ax.spines["right"].set_visible(True)
        ax.tick_params(
            direction="in",
            top=True,
            right=True,
            labelsize=14,
        )

    def _draw_subplot(
        self,
        ax,
        subplot,
    ):
        if subplot.x_data is None:
            return
        
        # plot
        converter = UnitConverter()

        x = converter.convert_plot(subplot.x_data, to_prefix=subplot.x_unit)

        for series in subplot.series:
            if not series.visible:
                continue

            y = converter.convert_plot(series.data, to_prefix=series.unit)

            if series.plot_type == "line":
                ax.plot(
                    x,
                    y,
                    label=series.label,
                    color=series.color,
                    linestyle=series.linestyle,
                    marker=series.marker,
                    linewidth=series.linewidth,
                    alpha=series.alpha,
                )

            elif series.plot_type == "scatter":
                ax.scatter(
                    x,
                    y,
                    label=series.label,
                    color=series.color,
                    marker=series.marker,
                    alpha=series.alpha,
                )

            elif series.plot_type == "step":
                ax.step(
                    x,
                    y,
                    label=series.label,
                    color=series.color,
                    linewidth=series.linewidth,
                )

        # title_setting
        if subplot.title:
            ax.set_title(subplot.title)

        xlabel = subplot.x_label

        if xlabel:
            ax.set_xlabel(xlabel)

        ylabel = subplot.y_label
        
        if ylabel:
            ax.set_ylabel(ylabel)

        # Scale
        ax.set_xscale(subplot.x_scale)
        ax.set_yscale(subplot.y_scale)

        # Range
        ax.set_xlim(
            left=subplot.xmin,
            right=subplot.xmax,
        )

        ax.set_ylim(
            bottom=subplot.ymin,
            top=subplot.ymax,
        )

        # Grid
        ax.grid(False)

        if subplot.grid_x:
            ax.xaxis.grid(
                True,
                alpha=0.3,
                linestyle='--'
            )

        if subplot.grid_y:
            ax.yaxis.grid(
                True,
                alpha=0.3,
                linestyle='--'
            )

        # Legend
        if subplot.legend:
            ax.legend(loc="upper right")

    # Save
    def save_png(
        self,
        path,
    ):

        self.figure.savefig(
            path,
            dpi=300,
            bbox_inches="tight",
        )

    def save_svg(
        self,
        path,
    ):
        self.figure.savefig(
            path,
            format="svg",
            bbox_inches="tight",
        )