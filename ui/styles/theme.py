from pathlib import Path

def load_theme(app):

    qss_path = (
        Path(__file__).parent
        / "main.qss"
    )

    with open(
        qss_path,
        encoding="utf-8"
    ) as f:

        app.setStyleSheet(
            f.read()
        )