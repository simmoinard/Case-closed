from PyQt6.QtWidgets import QApplication
import sys
from db_utils import *
from ui import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles.css").read())  # Applique le CSS
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
