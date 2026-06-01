# Analog-Circuit-Design-Assist (ACDA)

アナログ回路設計（Razaviレベル）に基づいた計算補助ツール

本プロジェクトは **PySide6ベースのデスクトップアプリ**として実装する。

---

## 1. フォルダ構成（アーキテクチャ設計）

```

ACDA/
│
├── .streamlit/
│   └── config.toml
│       # 将来削除予定（現在は互換用）
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

## 2. アーキテクチャ設計思想

### 2.1 レイヤ構造

本プロジェクトは以下の4層構造とする：

```

UI Layer (PySide6)
↓
Service Layer
↓
Formula Layer
↓
Data Layer

````

---

### 2.2 各層の責務

#### UI Layer（PySide6）

- PySide6によるデスクトップGUI
- ユーザー入力・表示のみ担当
- 計算ロジックを持たない
- services層のみ呼び出す

---

#### Service Layer（services/）

アプリケーションの中核制御層

- 計算フロー制御
- 入力検証（validator）
- 単位変換
- 数式評価（parser）
- 変数管理
- formula実行制御

---

#### Formula Layer（formulas/）

- 純粋関数のみ
- 状態を持たない
- Razaviベースの回路式実装
- 物理モデルに依存

例：
- gm
- ro
- ID
- Cox

---

#### Data Layer（data/, models/）

- デバイスパラメータ（YAML）
- MOSモデル定義
- 理想化されたLevel1パラメータ

---

## 3. デバイスパラメータの扱い

### 3.1 設計方針

- YAMLベースで管理（DBなし）
- 読み取り専用
- Pythonロジックから独立
- NMOS / PMOSを分離管理

---

### 3.2 例

```yaml
nmos:
  vto: 0.7
  gamma: 0.45
  phi: 0.9
  uo: 350
  lambda: 0.1

pmos:
  vto: -0.8
  gamma: 0.4
  phi: 0.8
  uo: 100
  lambda: 0.2
````

---

### 3.3 ルール

* SI単位系で統一
* 単位変換は services/unit_converter.py
* deviceモデルはimmutable（変更禁止）

---

## 4. Formula設計

### 4.1 原則

* 完全に純関数
* numpy or python標準のみ
* 入力チェックは禁止（validator責務）

---

### 4.2 例

```python
def cal_gm(id, vov):
    return 2 * id / vov
```

---

## 5. Services設計

### 5.1 formula_registry

* 計算式メタ情報管理
* UIと実行の橋渡し

---

### 5.2 formula_executor

* 実行エンジン
* fixed / variadic input対応

---

### 5.3 validator

責務：

* 入力欠損チェック
* 型チェック
* 物理制約チェック
* Expression安全性チェック

---

### 5.4 parser

* 数式文字列 → 評価結果
* sympyベース
* 単位前処理統合

---

### 5.5 variable_store

* ユーザー定義変数管理
* 例：ID, gm, Vov

---

### 5.6 unit_converter

* u, n, k, M 変換
* SI統一

---

## 6. UI設計（PySide6）

### 6.1 方針

* 完全デスクトップアプリ
* MVCに近い構造
* UIはロジックを持たない

---

### 6.2 画面構成

* MainWindow
* Formula Selector
* Input Panel
* Variable Panel
* Result Panel

---

### 6.3 イベントフロー

```
UI操作
 → Service呼び出し
 → Validator
 → Executor
 → Result返却
 → UI表示
```

---

## 7. 禁止ルール（重要）

* eval禁止
* UIに計算ロジックを書かない
* formulasで状態を持たない
* YAMLを直接編集対象にしない
* その他脆弱性を含むコード・アルゴリズムの使用禁止

---

## 8. 設計ゴール

* RazaviレベルのMOS設計補助
* 手計算の自動化
* 回路設計の学習支援
* デスクトップアプリとして完結

---

