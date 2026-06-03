# utils/paths.py

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
STYLE_DIR = ROOT_DIR / "ui" / "styles"
DOCS_DIR = ROOT_DIR / "docs"