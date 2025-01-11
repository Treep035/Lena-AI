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
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal, QTimer
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.controller.auth_controller import validate_fields_login_controller
from src.view.auth.recover_password import recover_password
from src.controller.auth_token_controller import generate_tokens_controller, insert_tokens_controller

class Login(QMainWindow):
    switch_to_register = pyqtSignal()
    switch_to_home = pyqtSignal()
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #233240;")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Crear un layout para los otros widgets
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(75, 10, 75, 125)  # Márgenes para el contenido

        # Agregar otros widgets al nuevo layout
        self.label = QLabel()
        self.label.setPixmap(QPixmap("src/resources/images/lena.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajusta la ruta y el tamaño según sea necesario
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("margin-top: 100px;")

        # Nuevo QLabel para el texto de bienvenida
        self.welcome_label = QLabel("Welcome back!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color: white; font-size: 35px; font-weight: 488;")  # Ajusta el estilo según tu preferencia

        self.text_email = QLineEdit()
        self.text_email.setPlaceholderText("Email...")
        self.text_email.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px;")
        self.text_email.setFixedSize(300, 50)
        self.text_email.textChanged.connect(self.remove_error_message)

        self.text_password = QLineEdit()
        self.text_password.setPlaceholderText("Password...")
        self.text_password.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px;")
        self.text_password.setEchoMode(QLineEdit.Password)
        self.text_password.setFixedSize(300, 50)
        self.text_password.textChanged.connect(self.remove_error_message)

        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon("src/resources/images/white/password/showpassword.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("background: transparent; border: none; padding-right: 10px;")
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.clicked.connect(self.toggle_password_visibility)

        self.forgot_password_label = QLabel("<a href='#' style='color: #94A7BB; text-decoration: none;'>Forgot your password?</a>")
        self.forgot_password_label.setStyleSheet("color: #1ABC9C; font-size: 13px;")
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.setFixedSize(135, 20)
        self.forgot_password_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.forgot_password_label.linkActivated.connect(lambda: recover_password(self))

        self.button = QPushButton("Login")
        self.button.setStyleSheet(""" 
            background-color: #2C3E50; 
            color: white; 
            padding: 10px; 
            border: 1px solid #ccc;
            border-radius: 10px; 
            font-size: 16px;
        """)
        self.button.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor a puntero
        self.button.clicked.connect(self.on_login_button_click)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.status_label_invalid = QLabel()
        self.status_label_invalid.setAlignment(Qt.AlignCenter)

        self.already_account_label = QLabel("<a href='#' style='color: #94A7BB; text-decoration: none;'>Don't have an account?</a>")
        self.already_account_label.setStyleSheet("color: #1ABC9C; font-size: 13px;")
        self.already_account_label.setAlignment(Qt.AlignCenter)
        self.already_account_label.setFixedSize(300, 20)
        self.already_account_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.already_account_label.linkActivated.connect(self.switch_to_register.emit)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.text_password)
        password_layout.addWidget(self.toggle_button)

        # Añadir widgets al layout principal
        self.main_content_layout.addWidget(self.label)
        self.main_content_layout.addWidget(self.welcome_label)
        self.main_content_layout.addWidget(self.text_email)
        self.main_content_layout.addLayout(password_layout)
        self.main_content_layout.addWidget(self.forgot_password_label)
        self.main_content_layout.addWidget(self.button)
        self.main_content_layout.addWidget(self.already_account_label)

        # Añadir el layout de contenido principal al layout de la ventana
        self.layout.addLayout(self.main_content_layout)
    
    def toggle_password_visibility(self):
        if self.toggle_button.isChecked():
            self.text_password.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setIcon(QIcon("src/resources/images/white/password/hidepassword.png"))
        else:
            self.text_password.setEchoMode(QLineEdit.Password)
            self.toggle_button.setIcon(QIcon("src/resources/images/white/password/showpassword.png"))

    def on_login_button_click(self):
        no_fields, invalid_fields, logged_in, id_user = validate_fields_login_controller(self)
        if no_fields:
            self.main_content_layout.removeWidget(self.status_label_invalid)
            self.status_label_invalid.hide()
            self.main_content_layout.addWidget(self.status_label)
            self.status_label.show()
            self.status_label.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Please, fill in all fields</a>")
            self.status_label.setAlignment(Qt.AlignCenter)
        elif invalid_fields:
            self.main_content_layout.addWidget(self.status_label_invalid)
            self.status_label_invalid.show()
            self.status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>The email or password is incorrect</a>")
            self.status_label_invalid.setAlignment(Qt.AlignCenter)
            
        elif logged_in:
            self.main_content_layout.removeWidget(self.status_label_invalid)
            self.status_label_invalid.hide()
            self.main_content_layout.addWidget(self.status_label)
            self.status_label.show()
            self.status_label.setText("<a href='#' style='color: #1ABC9C; font-size: 15px; font-weight: bold; text-decoration: none;'>Logged in successfully</a>")
            self.status_label.setAlignment(Qt.AlignCenter)
            auth_token, refresh_token, auth_token_expiration, refresh_token_expiration = generate_tokens_controller()
            insert_tokens_controller(id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration)
            QTimer.singleShot(3000, self.remove_error_message)
            QTimer.singleShot(3000, self.switch_to_home.emit)
            QTimer.singleShot(3000, lambda: self.clear_fields())
            
    def clear_fields(self):
        self.text_email.clear()
        self.text_password.clear()
    
    def remove_error_message(self):
        self.main_content_layout.removeWidget(self.status_label)
        self.status_label.hide()
    
    def get_email(self):
        # Obtener el texto ingresado en el QLineEdit
        email = self.text_email.text()
        return email