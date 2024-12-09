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
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.controller.auth_controller import validate_fields_register_controller

class Register(QMainWindow):
    switch_to_login = pyqtSignal()
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
        self.label.setStyleSheet("margin-top: 30px;")

        self.welcome_label = QLabel("Create an account")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color: white; font-size: 35px; margin-bottom:10px;")  # Ajusta el estilo según tu preferencia

        self.text_username = QLineEdit()
        self.text_username.setPlaceholderText("Username...")
        self.text_username.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px;")
        self.text_username.setFixedSize(300, 50)

        self.text_email = QLineEdit()
        self.text_email.setPlaceholderText("Email...")
        self.text_email.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px;")
        self.text_email.setFixedSize(300, 50)

        self.text_password = QLineEdit()
        self.text_password.setPlaceholderText("Password...")
        self.text_password.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px;")
        self.text_password.setEchoMode(QLineEdit.Password)
        self.text_password.setFixedSize(300, 50)

        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("background: transparent; border: none; padding-right: 10px;")
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.clicked.connect(self.toggle_password_visibility)
        
        self.date_birthdate = QDateEdit()
        image_path = os.path.abspath("./src/resources/images/calendar/black/calendarblack.png")
        if not os.path.exists(image_path):
            print(f"¡La imagen no se encuentra en la ruta: {image_path}!")
        self.date_birthdate.setStyleSheet("""
    QDateEdit {
        color: white;
        border-radius: 10px;
        border: 1px solid #ccc;
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
        self.date_birthdate.setFixedSize(300, 50)
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
        self.button.clicked.connect(lambda: validate_fields_register_controller(self))

        self.already_account_label = QLabel("<a href='#' style='color: #94A7BB; text-decoration: none;'>Do you already have an account?</a>")
        self.already_account_label.setStyleSheet("color: #1ABC9C; font-size: 12px;")
        self.already_account_label.setAlignment(Qt.AlignCenter)
        self.already_account_label.setFixedSize(185, 20)
        self.already_account_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.already_account_label.linkActivated.connect(self.switch_to_login.emit)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.text_password)
        password_layout.addWidget(self.toggle_button)

        # Añadir widgets al layout principal
        self.main_content_layout.addWidget(self.label)
        self.main_content_layout.addWidget(self.welcome_label)
        self.main_content_layout.addWidget(self.text_username)
        self.main_content_layout.addWidget(self.text_email)
        self.main_content_layout.addLayout(password_layout)
        self.main_content_layout.addWidget(self.date_birthdate)
        self.main_content_layout.addWidget(self.button)
        self.main_content_layout.addWidget(self.already_account_label)

        # Añadir el layout de contenido principal al layout de la ventana
        self.layout.addLayout(self.main_content_layout)

    def toggle_password_visibility(self):
        if self.toggle_button.isChecked():
            self.text_password.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setIcon(QIcon("src/resources/images/password/white/hidepasswordwhite.png"))
        else:
            self.text_password.setEchoMode(QLineEdit.Password)
            self.toggle_button.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))