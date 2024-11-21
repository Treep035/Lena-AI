import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from controller.auth_token_controller import check_auth_token_controller

from view.shared.titlebar import TitleBar
from view.auth.login import Login
from view.auth.register import Register

from view.shared.bottombar import BottomBar
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

        # Agregar la barra de título
        self.title_bar = TitleBar()
        self.layout.addWidget(self.title_bar)

        # Instancias de login y register
        self.login_widget = Login()
        self.register_widget = Register()

        # Conectar las señales
        self.login_widget.switch_to_register.connect(self.show_register)
        self.register_widget.switch_to_login.connect(self.show_login)
        self.login_widget.switch_to_home.connect(self.show_home)

        logged_in = check_auth_token_controller()

        if logged_in:
            self.show_home()
        else:
            self.show_login()

    def show_register(self):
        self.layout.removeWidget(self.login_widget)
        self.login_widget.hide()
        self.layout.addWidget(self.register_widget)
        self.register_widget.show()

    def show_login(self):
        self.layout.removeWidget(self.register_widget)
        self.register_widget.hide()
        self.layout.addWidget(self.login_widget)
        self.login_widget.show()

    def show_home(self):
        self.layout.removeWidget(self.register_widget)
        self.register_widget.hide()
        self.layout.removeWidget(self.login_widget)
        self.login_widget.hide()
        
        self.home_widget = Home()
        self.chat_widget = Chat()
        self.account_widget = Account()

        self.bottom_bar = BottomBar()
        
        self.layout.addWidget(self.home_widget)
        
        # Agregar la barra de título
        
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