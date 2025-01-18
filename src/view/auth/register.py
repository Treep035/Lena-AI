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

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.controller.auth_controller import validate_fields_register_controller
from src.controller.auth_token_controller import generate_tokens_controller, insert_tokens_controller

class Register(QMainWindow):
    switch_to_login = pyqtSignal()
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
        self.main_content_layout.setContentsMargins(75, 10, 75, 100)  # Márgenes para el contenido

        # Agregar otros widgets al nuevo layout
        self.label = QLabel()
        self.label.setPixmap(QPixmap("src/resources/images/lena.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajusta la ruta y el tamaño según sea necesario
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("margin-top: 30px;")

        self.welcome_label = QLabel("Create an account")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color: white; font-size: 35px; margin-bottom:10px;")  # Ajusta el estilo según tu preferencia

        self.text_username = QLineEdit()
        self.text_username.setPlaceholderText("Username...")
        self.text_username.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px;")
        self.text_username.setFixedSize(300, 50)
        self.text_username.textChanged.connect(self.remove_error_message)

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
        
        self.date_birthdate = QDateEdit()
        image_path = os.path.abspath("./src/resources/images/white/calendar/calendar.png")
        if not os.path.exists(image_path):
            print(f"¡La imagen no se encuentra en la ruta: {image_path}!")
        self.date_birthdate.setStyleSheet("""
    QDateEdit {
        color: white;
        border-radius: 10px; 
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
        border-width: 1px 1px 1px 0px; /* Sin borde a la izquierda */
        border-style: solid;
        border-color: #ccc;
        padding: 3px;
        padding-left: 10px;
        background-color: #233240;  /* Fondo más oscuro */
    }
    QDateEdit::down-arrow {
        image: url({image_path});  /* Imagen personalizada para la flecha */
        width: 16px;  /* Ajusta el tamaño de la flecha */
        height: 16px;
        margin: 0px;
    }   
        QDateEdit::down-button:hover {
            image: url({image_path});  /* Imagen diferente cuando se pasa el mouse sobre la flecha */
        }
    QDateEdit::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-radius: 10px;
    }
    QCalendarWidget {
        border: 1px solid #555;
        border-radius: 10px;
        background-color: #2B3E50;  /* Fondo principal del calendario */
        color: white;  /* Color de texto */
    }
    QCalendarWidget QToolButton {
        color: white;
        background-color: #3F556B;
        border: none;
        font-weight: bold;
        height: 30px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: #5A7393;
    }
    QCalendarWidget QToolButton::menu-indicator {
        image: none;  /* Oculta el icono de menú desplegable */
    }
    QCalendarWidget QTableView {
        border: none;
        background-color: #2B3E50;
        color: #E0E0E0;
    }
    QCalendarWidget QTableView::item:selected {
        background-color: #486A84;
        color: white;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #3F556B;
        border-radius: 10px;
    }
""")
        self.date_birthdate.setFixedSize(125, 50)
        self.date_birthdate.setCalendarPopup(True)
        self.date_birthdate.setDate(QDate.currentDate())

        self.button = QPushButton("Register")
        self.button.setStyleSheet(""" 
            background-color: #2C3E50; 
            color: white; 
            padding: 10px; 
            border: 1px solid #ccc;
            border-radius: 10px; 
            font-size: 16px;
        """)
        self.button.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor a puntero
        self.button.clicked.connect(self.on_register_button_click)

        self.already_account_label = QLabel("<a href='#' style='color: #94A7BB; text-decoration: none;'>Do you already have an account?</a>")
        self.already_account_label.setStyleSheet("color: #1ABC9C; font-size: 12px;")
        self.already_account_label.setAlignment(Qt.AlignCenter)
        self.already_account_label.setFixedSize(185, 20)
        self.already_account_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.already_account_label.linkActivated.connect(self.switch_to_login.emit)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.status_label_invalid = QLabel()
        self.status_label_invalid.setAlignment(Qt.AlignCenter)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.text_password)
        password_layout.addWidget(self.toggle_button)

        self.birthdate_label = QLabel("Birthdate...")
        self.birthdate_label.setStyleSheet("""
            color: #A0A0A0; 
            border-radius: 10px; 
            border-top-right-radius: 0px; 
            border-bottom-right-radius: 0px; 
            border-width: 1px 0 1px 1px; 
            border-style: solid; 
            border-color: #ccc; 
            padding: 15px 3px 13px 8px;
        """)
        self.birthdate_label.setAlignment(Qt.AlignLeft)
        self.birthdate_label.setFixedWidth(200)      

        birthdate_layout_3 = QHBoxLayout()
        birthdate_layout_3.addWidget(self.birthdate_label)
        birthdate_layout_3.setContentsMargins(0, 0, 0, 0)

        birthdate_layout_2 = QHBoxLayout()
        birthdate_layout_2.setContentsMargins(0, 0, 0, 0)
        birthdate_layout_2.addWidget(self.date_birthdate)

        birthdate_layout = QHBoxLayout()
        birthdate_layout.addLayout(birthdate_layout_3)  # Añadir el texto
        birthdate_layout.addLayout(birthdate_layout_2)
        
        # Añadir widgets al layout principal
        self.main_content_layout.addWidget(self.label)
        self.main_content_layout.addWidget(self.welcome_label)
        self.main_content_layout.addWidget(self.text_username)
        self.main_content_layout.addWidget(self.text_email)
        self.main_content_layout.addLayout(password_layout)
        self.main_content_layout.addLayout(birthdate_layout)
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

    def on_register_button_click(self):
        no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user = validate_fields_register_controller(self)
        if no_fields:
            self.main_content_layout.removeWidget(self.status_label_invalid)
            self.status_label_invalid.hide()
            self.main_content_layout.addWidget(self.status_label)
            self.status_label.show()
            self.status_label.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Please, fill in all fields</a>")
            self.status_label.setAlignment(Qt.AlignCenter)
        elif name_in_use:
            self.main_content_layout.addWidget(self.status_label_invalid)
            self.status_label_invalid.show()
            self.status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>The username is already in use</a>")
            self.status_label_invalid.setAlignment(Qt.AlignCenter)
        elif invalid_regex_email:
            self.main_content_layout.addWidget(self.status_label_invalid)
            self.status_label_invalid.show()
            self.status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Invalid email</a>")
            self.status_label_invalid.setAlignment(Qt.AlignCenter)
        elif email_in_use:
            self.main_content_layout.addWidget(self.status_label_invalid)
            self.status_label_invalid.show()
            self.status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>The email is already in use</a>")
            self.status_label_invalid.setAlignment(Qt.AlignCenter)
        elif invalid_regex_password:
            self.main_content_layout.addWidget(self.status_label_invalid)
            self.status_label_invalid.show()
            self.status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Invalid password</a>")
            self.status_label_invalid.setAlignment(Qt.AlignCenter)
        elif invalid_data_birthdate:
            self.main_content_layout.addWidget(self.status_label_invalid)
            self.status_label_invalid.show()
            self.status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>You must be older than 18</a>")
            self.status_label_invalid.setAlignment(Qt.AlignCenter)
        elif logged_in:
            self.main_content_layout.removeWidget(self.status_label_invalid)
            self.status_label_invalid.hide()
            self.main_content_layout.addWidget(self.status_label)
            self.status_label.show()
            self.status_label.setText("<a href='#' style='color: #1ABC9C; font-size: 15px; font-weight: bold; text-decoration: none;'>Registered successfully</a>")
            self.status_label.setAlignment(Qt.AlignCenter)
            auth_token, refresh_token, auth_token_expiration, refresh_token_expiration = generate_tokens_controller()
            insert_tokens_controller(id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration)
            QTimer.singleShot(3000, self.remove_error_message)
            QTimer.singleShot(3000, self.switch_to_home.emit)
            QTimer.singleShot(3000, lambda: self.clear_fields())
            
    def clear_fields(self):
        self.text_username.clear()
        self.text_email.clear()
        self.text_password.clear()
        self.date_birthdate.setDate(QDate.currentDate())
        self.toggle_button.setChecked(False)
        self.toggle_password_visibility()

    def remove_error_message(self):
        self.main_content_layout.removeWidget(self.status_label)
        self.status_label.hide()