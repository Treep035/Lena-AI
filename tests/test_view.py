import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QTextEdit,
    QHBoxLayout,
    QDateEdit,
    QLineEdit,
    QMessageBox,
    QSpacerItem,
    QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon
from PyQt5.QtCore import Qt, QEvent, QDate

from src.view.titlebar import TitleBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lena AI")
        self.setGeometry(100, 100, 450, 725)
        self.setFixedSize(450, 725)
        self.setWindowIcon(QIcon('./lena.ico'))

        # Eliminar la barra de título predeterminada
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Crear y establecer la barra de título personalizada
        self.title_bar = TitleBar()

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.title_bar)  # Añadir la barra de título
        
        # Configurar el widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
