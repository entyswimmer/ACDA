from pathlib import Path

import pandas as pd


class PlotDataLoader:
    """
    CSV / VCSV 読み込み・DataFrame管理クラス
    """

    def __init__(self):

        self.df: pd.DataFrame | None = None

    def load(self, file_path: str):
        """
        CSV / VCSVを読み込む
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        suffix = path.suffix.lower()

        if suffix == ".csv":
            self.df = self._load_csv(path)

        elif suffix == ".vcsv":
            self.df = self._load_vcsv(path)

        else:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )

    def _load_csv(
        self,
        path: Path,
    ) -> pd.DataFrame:
        """
        通常CSV読み込み
        """

        return pd.read_csv(path)

    def _load_vcsv(
        self,
        path: Path,
    ) -> pd.DataFrame:
        """
        Virtuoso VCSV読み込み
        """

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as f:

            lines = [next(f) for _ in range(6)]

        traces_raw = [
            t.replace(";", "").strip()
            for t in lines[1].split(",")
        ]

        traces = [
            t
            for t in traces_raw
            for _ in (0, 1)
        ]

        variables = [
            v.replace(";", "").strip()
            for v in lines[4].split(",")
        ]

        units = [
            u.replace(";", "").strip()
            for u in lines[5].split(",")
        ]

        column_names = [
            f"{trace} | {var} [{unit}]"
            for trace, var, unit in zip(
                traces,
                variables,
                units,
            )
        ]

        return pd.read_csv(
            path,
            skiprows=6,
            header=None,
            names=column_names,
        )

    def get_dataframe(self) -> pd.DataFrame:
        """
        DataFrame取得
        """

        self._check_loaded()

        return self.df

    def get_columns(self) -> list[str]:
        """
        列名一覧取得
        """

        self._check_loaded()

        return self.df.columns.tolist()

    def get_column(
        self,
        column_name: str,
    ) -> pd.Series:
        """
        指定列取得
        """

        self._check_loaded()

        return self.df[column_name]

    def get_shape(self) -> tuple[int, int]:
        """
        行数・列数取得
        """

        self._check_loaded()

        return self.df.shape

    def _check_loaded(self):
        """
        DataFrameが読み込まれているか確認
        """

        if self.df is None:
            raise RuntimeError(
                "Data is not loaded."
            )