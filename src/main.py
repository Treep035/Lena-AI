import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from view.shared.titlebar import TitleBar
from view.auth.login import Login
from view.auth.register import Register

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

        # Mostrar el formulario de login inicialmente
        self.layout.addWidget(self.login_widget)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())