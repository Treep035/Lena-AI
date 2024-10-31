import sys
from PyQt5.QtWidgets import QApplication

def open_login():
    from src.view.login import MainWindow as LoginWindow  # Importa la ventana de inicio de sesión
    window = LoginWindow()  # Crear la ventana de inicio de sesión
    window.show()  # Mostrarla

def open_register():
    print("Abriendo la ventana")
    from src.view.register import MainWindow as RegisterWindow  # Importa la ventana de registro
    window = RegisterWindow()  # Crear la ventana de inicio de sesión
    window.show()  # Mostrarla
    print("inicializando")