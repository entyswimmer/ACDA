from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from styles.theme import load_theme

app = QApplication([])

load_theme(app)

window = MainWindow()
window.show()

app.exec()