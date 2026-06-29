import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from services.plotDataLoader import PlotDataLoader
from plots.selectPlotSetting import (
    SelectPlotSetting,
    SubPlotSetting,
)
from plots.makeGraph import MakeGraph


FILE_PATH = "tests/Neuron01.vcsv"

app = QApplication(sys.argv)

# ======================================================
# Data Load
# ======================================================

loader = PlotDataLoader()
loader.load(FILE_PATH)

columns = loader.get_columns()

print(columns)

# ======================================================
# Plot Setting
# ======================================================

setting = SelectPlotSetting()

# ---------- 2行1列 ----------
setting.set_layout(
    rows=2,
    cols=1,
)

# ======================================================
# Subplot 1 : Voltage
# ======================================================

subplot1 = SubPlotSetting()

subplot1.title = "Voltage"
subplot1.x_data = loader.get_column(columns[0])
subplot1.x_label = "t [ms]"
subplot1.x_unit = "m"          # s → ms に変換
subplot1.y_label = "V [mV]"
subplot1.y_unit = "m"
subplot1.legend = True
subplot1.grid_x = True
subplot1.grid_y = True
subplot1.xmin = 0
subplot1.xmax = 1000

subplot1.add_series(
    data=loader.get_column(columns[1]),
    label=columns[1],
    unit=subplot1.y_unit,                   # V
)

setting.add_subplot(subplot1)

# ======================================================
# Subplot 2 : Current
# ======================================================

subplot2 = SubPlotSetting()

subplot2.title = "Current"
subplot2.x_data = loader.get_column(columns[4])
subplot2.x_label = "t [ms]"
subplot2.x_unit = "m"          # s → ms に変換
subplot2.y_label = "I [uA]"
subplot2.y_unit = "u"
subplot2.legend = True
subplot2.grid_x = True
subplot2.grid_y = True
subplot2.xmin = 0
subplot2.xmax = 1000

subplot2.add_series(
    data=loader.get_column(columns[3]),
    label=columns[3],
    color="skyblue",
    unit=subplot2.y_unit,                   # A
)

subplot2.add_series(
    data=loader.get_column(columns[5]),
    label=columns[5],
    color="limegreen",
    unit=subplot2.y_unit,                   # A
)

setting.add_subplot(subplot2)

# ======================================================
# Draw
# ======================================================

graph = MakeGraph()
graph.draw(setting)

# ======================================================
# Window
# ======================================================

window = QMainWindow()

window.setCentralWidget(
    graph.get_canvas()
)

window.resize(1000, 900)

window.show()

sys.exit(app.exec())