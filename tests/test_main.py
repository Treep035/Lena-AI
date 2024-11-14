import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from view.shared.bottombar import BottomBar
from view.shared.titlebar import TitleBar
from view.home.home import Home
from view.home.chat import Chat
from view.home.account import Account

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("src/resources/images/lenaicon.ico"))
        self.setWindowTitle("Lena AI")
        self.setGeometry(100, 100, 450, 725)
        self.setFixedSize(450, 725)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Crear layout principal
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setCentralWidget(self.central_widget)

        self.title_bar = TitleBar()
        self.layout.addWidget(self.title_bar)

        self.home_widget = Home()
        self.layout.addWidget(self.home_widget)

        self.chat_widget = Chat()

        self.account_widget = Account()

        # Agregar la barra de título
        self.bottom_bar = BottomBar()
        self.layout.addWidget(self.bottom_bar)

        self.bottom_bar.viewChanged.connect(self.showOption)

    def showOption(self, view_name):
        if view_name == "home":
            self.layout.removeWidget(self.chat_widget)
            self.chat_widget.hide()
            self.layout.removeWidget(self.account_widget)
            self.account_widget.hide()
            self.layout.removeWidget(self.bottom_bar)
            self.bottom_bar.hide()
            self.layout.addWidget(self.home_widget)
            self.home_widget.show()
            self.layout.addWidget(self.bottom_bar)
            self.bottom_bar.show()
        elif view_name == "chat":
            self.layout.removeWidget(self.home_widget)
            self.home_widget.hide()
            self.layout.removeWidget(self.account_widget)
            self.account_widget.hide()
            self.layout.removeWidget(self.bottom_bar)
            self.bottom_bar.hide()
            self.layout.addWidget(self.chat_widget)
            self.chat_widget.show()
            self.layout.addWidget(self.bottom_bar)
            self.bottom_bar.show()
        elif view_name == "account":
            self.layout.removeWidget(self.home_widget)
            self.home_widget.hide()
            self.layout.removeWidget(self.chat_widget)
            self.chat_widget.hide()
            self.layout.removeWidget(self.bottom_bar)
            self.bottom_bar.hide()
            self.layout.addWidget(self.account_widget)
            self.account_widget.show()
            self.layout.addWidget(self.bottom_bar)
            self.bottom_bar.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())