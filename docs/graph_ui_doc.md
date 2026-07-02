# graph画面のUI
---


# UI設計

## ディレクトリ構成
```text
ACDA
│
├── main.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py
│   ├── main_window.py
│   │
│   ├── graph/
│   │   ├── graphView.py
│   │   ├── graphToolBox.py
│   │   ├── columnSelector.py
│   │   ├── subplotEditor.py
│   │   ├── seriesEditor.py
│   │   └── axisEditor.py
│   │
│   ├── styles/
│   │   └── main.qss
│   │
│   └── widgets/
│       ├── unitSelector.py
│       ├── colorSelector.py
│       ├── lineStyleSelector.py
│       └── markerSelector.py
│
├── controller/
│   ├── projectController.py
│   ├── graphController.py
│   └── fileController.py
│
├── services/
│   ├── plotDataLoader.py
│   ├── unitConverter.py
│   └── exportFigure.py
│
├── plots/
│   ├── makeGraph.py
│   └── selectPlotSetting.py
│
└── models/
    └── projectModel.py

⸻

各クラスの責務

mainWindow.py

責務

* 全体レイアウト
* Dock配置
* メニュー配置

持つもの

* GraphView
* ToolBox
* MenuBar
* StatusBar

⸻

graphView.py

責務

* Matplotlib Canvas表示
* MakeGraph保持

持たないもの

* データ処理
* CSV読み込み

⸻

graphToolBox.py

責務

左側の設定画面

例

Data
X Axis
    □ ComboBox
Series
□ TableWidget
Graph
□ Title
□ X Label
□ Y Label
Axis
□ Range
□ Grid
□ Log

⸻

columnSelector.py

責務

DataFrame列選択

例

Time
Voltage
Current
・・・

戻り値

column_name

⸻

seriesEditor.py

責務

PlotSeries編集

編集項目

Label
Color
Line Style
Marker
Line Width
Visible

編集対象

PlotSeries

⸻

subplotEditor.py

責務

SubPlotSetting編集

編集

Title
X Label
Y Label
Legend
Grid
Scale
Range

⸻

axisEditor.py

責務

軸編集

xmin
xmax
ymin
ymax
linear/log
grid x
grid y

⸻

unitSelector.py

責務

表示単位選択

例

Time
s
ms
us
ns

戻り値

""
"m"
"u"
"n"

⸻

graphController.py

責務

UIとMakeGraphを接続

流れ

UI変更
↓
SelectPlotSetting更新
↓
MakeGraph.draw()
↓
Canvas更新

⸻

fileController.py

責務

ファイル操作

Open
Reload
Export PNG
Export SVG
Export PDF

⸻

projectController.py

責務

プロジェクト全体管理

保持

DataFrame
SelectPlotSetting
Current File
Recent Files

⸻

データフロー

CSV
↓
PlotDataLoader
↓
DataFrame
↓
ColumnSelector
↓
SelectPlotSetting
↓
GraphController
↓
MakeGraph
↓
Matplotlib Canvas
↓
GraphView

⸻

ユーザー操作

Open CSV
↓
列選択
↓
Series追加
↓
色変更
↓
単位変更
↓
タイトル変更
↓
Range変更
↓
Graph更新
↓
Export

⸻

今後追加予定

* ヒストグラム
* FFT
* Bode Plot
* Smith Chart
* Cursor
* Peak Search
* CSV Export
* PDF Report
* Figure Template
* Style Preset
* Dark Mode
* Graph Session保存

## この構成をおすすめする理由
現在作成した
- `PlotDataLoader`
- `SelectPlotSetting`
- `MakeGraph`
はそのまま利用でき、**UIはこれらを操作するだけ**になります。
特に重要なのは、**UIが直接 `MakeGraph` や `PlotDataLoader` を操作せず、Controllerを介してやり取りする**ことです。これにより、将来的に設定項目が増えても、UI・描画・データ処理が独立して保守しやすくなります。これは、今後Bode線図やFFTなどの解析機能を追加する際にも拡張しやすい構成です。