# グラフの作成機能追加

---

ver2.0としてアップデート内容はVirtuosoのデータからグラフの作成が可能になる

## 1. 機能の要件定義

#### 1-1. 必要機能

- csv, vcsvファイルのデータフレーム化(OSデフォルトのファイルマネージャーからファイル選択可能)
- 列名の取得 + 選択(単位変換も)
- 最小値+最大値+log+表示サイズ+タイトル+xlabel+ylabel+legend+gridの選択
- グラフの保存機能(OSデフォルトのファイルマネージャー保存場所の選択が可能)
- データの解析機能
- グラフで使用する色＋フォントの選択(非必須要件)

#### 1-2. グラフ種類

- 単プロット
- 複数のデータを同一グラフにプロット
- 複数のデータを複数グラフにプロットし1枚にする
- グラフタイプの選択が可能(markerの使用や散布図にするか等)

#### 1-3. グラフ機能

対応形式

- csv
- vcsv

グラフ

- Line
- Scatter
- Line+Marker
- Step

軸

- Linear
- Log-X
- Log-Y
- Log-Log

表示

- Title
- XLabel
- YLabel
- Legend
- Grid
- Axis Range

解析

- Max
- Min
- Mean
- RMS

保存

- PNG
- SVG

操作

- Zoom
- Pan
- Cursor表示
これらを無効化

Virtuoso対応

- Tran
- AC
- DC

---

## 2. 最小構成

```markdown
ACDA/
│
│
├── data/
│   └── razavi_level1.yaml
│       # デバイスパラメータ定義（固定モデルデータ）
│
├── formulas/
│   ├── frequency.py
│   ├── passive.py
│   └── mos_basic.py
│       # 純粋な物理・回路式（副作用なし）
│
├── models/
│   └── device.py
│       # MOSデバイス構造定義（NMOS / PMOS）
│
├── plots/ #追加機能
│   ├── analyzer.py # データの分析(線形回帰や微積等を想定)
│   ├── makeGraph.py# グラフの作成
|   ├── select_data.py # 追加  グラフ化するデータの選択や描画設定の作成
│
├── services/
│   ├── formula_registry.py
│       # 計算式メタデータ管理（UIとロジックの橋渡し）
│
│   ├── formula_executor.py
│       # 計算実行エンジン（統一インターフェース）
│
│   ├── validator.py
│       # 入力チェック（型・範囲・安全性）
│
│   ├── unit_converter.py
│       # 単位変換（u, n, k, M）
│
│   ├── variable_store.py
│       # ユーザー変数管理（ID, gmなど）
│
│   ├── parser.py
│       # 数式パーサ（Expression処理）
│
│   └── model_loader.py
│       # YAML → Deviceモデル変換
│  
│  　├── plotDataLoader.py　# 追加 グラフ化データの追加＋グラフ化
│     
│  　├── plotExporter.py #必要なら後々作成
│
├── ui/
│   ├── main_window.py
│       # PySide6 メインウィンドウ
│
│   ├── formula_view.py
│       # 式選択・入力UI
│
│   ├── variable_view.py
│       # 変数管理UI
│
│   └── result_view.py
│       # 計算結果表示UI
│  
│   ├── plot_tab.py # グラフ関連UIのコントロール
│   ├── data_panel.py　# 追加 選択データの表示UI
│   ├── graph_panel.py　# 追加 グラフデータの表示UI
│   ├── setting_panel.py # 追加　グラフの調整UI
│   ├── analysis_panel.py # データ解析結果の表示UI
│
├── tests/
│   ├── test_formulas.py
│   ├── test_parser.py
│   └── test_validator.py
│
├── utils/
│   └── path.py
│       # OS非依存パス解決
│
├── docs/
│   └── design.md
│       # 本設計ドキュメント
│
├── main.py
│   # PySide6 アプリエントリポイント
│
├── README.md
└── requirements.txt

```

---

## 3. ロジック実装マニュアル

#### 3-1. グラフ作成に追加するライブラリ

- pyqtgraphを採用(カーソル位置表示＋ズーム+ドラッグ移動は可能に)

#### 3-2. データI/O

- ユーザーがos標準のファイルマネージャーを使用可能

#### 3-3. データ解析

- データ解析画面にチェックが入ればそれもグラフと同時出力にする形に(優先度低)

---

## 4. UI実装マニュアル

- streamlit風に作成
- modernUIになるように調整

---

## 5. 新規ファイルの責務分離

#### **5-1. plots/analyzer.py**

責務

- DataFrameに対する解析処理
- 最大値(Max)計算
- 最小値(Min)計算
- 平均値(Mean)計算
- 実効値(RMS)計算
- 将来的なFFT・微分・積分・回帰分析の追加先

担当しないもの

- UI表示
- ファイル読込
- グラフ描画

---

#### **5-2. plots/make_graph.py**

責務

- pyqtgraphによるグラフ生成
- 単プロット描画
- 複数系列描画
- グラフスタイル適用
- 軸設定適用
- グラフ更新

担当しないもの

- ファイル読込
- データ解析
- UIイベント処理

---

#### **5-3. services/data_loader.py**

責務

- csv読込
- vcsv読込
- DataFrame生成
- データ形式判定
- Tran/AC/DCデータ判定
- 列名取得

担当しないもの

- UI表示
- グラフ描画
- データ解析

入出力例

```python
df = load(path)

columns = get_columns(df)

analysis_type = detect_type(df)
```

---

#### **5-4. services/select_data.py**

責務

- グラフ描画対象データの管理
- X軸データ管理
- Y軸データ管理
- 複数系列の管理
- 単位変換の適用
- 軸範囲設定

担当しないもの

- グラフ描画
- UI表示

入出力例

```python
selection.set_x("time")

selection.add_y("Vout")

selection.add_y("Vin")
```

---

#### **5-5. ui/plot_tab.py**

責務

- グラフタブ全体の制御
- 各パネルのレイアウト管理
- シグナル接続
- データロード後の更新通知

担当しないもの

- データ解析
- グラフ描画ロジック

---

#### **5-6. ui/data_panel.py**

責務

- 読み込んだデータ一覧表示
- DataFrame情報表示
- 列名一覧表示
- 選択可能データの表示

表示例

```
time
Vin
Vout
Vmem
```

---

#### **5-7. ui/graph_panel.py**

責務

- pyqtgraphウィジェット配置
- グラフ表示領域管理
- ズーム操作
- パン操作
- カーソル位置表示

表示例

```
x = 25.4 us
y = 412 mV
```

---

#### **5-8. ui/setting_panel.py**

責務

- グラフ設定UI
- タイトル設定
- 軸ラベル設定
- Grid設定
- Legend設定
- Log設定
- 軸範囲設定
- グラフ種類設定

対象設定

```
Title
XLabel
YLabel
Grid
Legend
Linear
Log-X
Log-Y
Log-Log
Line
Scatter
Step
```

---

#### **5-9. ui/analysis_panel.py**

責務

- データ解析結果表示
- Max表示
- Min表示
- Mean表示
- RMS表示

表示例