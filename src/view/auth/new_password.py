import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    QSizePolicy,
    QDialog,
    QDialogButtonBox
)
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon, QCursor
from PyQt5.QtCore import Qt, QEvent, QDate, QSize, QTimer, QCoreApplication
from PyQt5.QtGui import QIcon

from view.shared.titlebar_dialog import TitleBarDialog
from controller.auth_controller import validate_fields_recover_password_controller
# from controller.recover_password_controller import send_recovery_email_controller
from controller.theme_controller import get_theme_controller
# from controller.auth_controller import validate_fields_change_password_controller
from resources.styles.theme import change_theme

class NewPassword(QDialog):
    def __init__(self, token=None, app=None):
        super().__init__()
        self.token = token
        self.app = app
        theme = get_theme_controller()
        hola = "hola"
        theme_color = change_theme(hola, theme)

        def toggle_password_visibility_2(theme_color):
            if toggle_button_2.isChecked():
                self.text_new_password.setEchoMode(QLineEdit.Normal)
                base_path = os.path.dirname(os.path.abspath(__file__))
                base_path_up = os.path.abspath(os.path.join(base_path, "../.."))
                icon_path = os.path.join(base_path_up, "resources", "images", theme_color[4], "password", "hidepassword.png")
                toggle_button_2.setIcon(QIcon(icon_path))
            else:
                self.text_new_password.setEchoMode(QLineEdit.Password)
                base_path = os.path.dirname(os.path.abspath(__file__))
                base_path_up = os.path.abspath(os.path.join(base_path, "../.."))
                icon_path = os.path.join(base_path_up, "resources", "images", theme_color[4], "password", "showpassword.png")
                toggle_button_2.setIcon(QIcon(icon_path))

        def toggle_password_visibility_3(theme_color):
            if toggle_button_3.isChecked():
                self.text_confirm_new_password.setEchoMode(QLineEdit.Normal)
                base_path = os.path.dirname(os.path.abspath(__file__))
                base_path_up = os.path.abspath(os.path.join(base_path, "../.."))
                icon_path = os.path.join(base_path_up, "resources", "images", theme_color[4], "password", "hidepassword.png")
                toggle_button_3.setIcon(QIcon(icon_path))
            else:
                self.text_confirm_new_password.setEchoMode(QLineEdit.Password)
                base_path = os.path.dirname(os.path.abspath(__file__))
                base_path_up = os.path.abspath(os.path.join(base_path, "../.."))
                icon_path = os.path.join(base_path_up, "resources", "images", theme_color[4], "password", "showpassword.png")
                toggle_button_3.setIcon(QIcon(icon_path))

        def on_save_changes_button_click():
            no_fields, invalid_token, invalid_fields, invalid_regex, same_password = validate_fields_recover_password_controller(self)

            if no_fields:
                main_content_layout.removeWidget(status_label_invalid)
                status_label_invalid.hide()
                main_content_layout.addWidget(status_label)
                status_label.show()
                status_label.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Please fill in all fields</a>")
                status_label.setAlignment(Qt.AlignCenter)

            if invalid_token:
                main_content_layout.removeWidget(status_label_invalid)
                status_label_invalid.hide()
                main_content_layout.addWidget(status_label_invalid)
                status_label_invalid.show()
                status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Invalid token</a>")
                status_label_invalid.setAlignment(Qt.AlignCenter)

            if invalid_fields:
                main_content_layout.removeWidget(status_label_invalid)
                status_label_invalid.hide()
                main_content_layout.addWidget(status_label_invalid)
                status_label_invalid.show()
                status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>The two passwords do not match</a>")
                status_label_invalid.setAlignment(Qt.AlignCenter)

            if invalid_regex:
                main_content_layout.removeWidget(status_label_invalid)
                status_label_invalid.hide()
                main_content_layout.addWidget(status_label_invalid)
                status_label_invalid.show()
                status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Invalid password</a>")
                status_label_invalid.setAlignment(Qt.AlignCenter)

            if same_password:
                main_content_layout.removeWidget(status_label_invalid)
                status_label_invalid.hide()
                main_content_layout.addWidget(status_label_invalid)
                status_label_invalid.show()
                status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>The new password must be different</a>")
                status_label_invalid.setAlignment(Qt.AlignCenter)

            if not no_fields and not invalid_token and not invalid_fields and not invalid_regex and not same_password:
                main_content_layout.removeWidget(status_label_invalid)
                status_label_invalid.hide()
                main_content_layout.addWidget(status_label)
                status_label.show()
                status_label.setText("<a href='#' style='color: #1db00a; font-size: 15px; font-weight: bold; text-decoration: none;'>Password successfully changed</a>")
                status_label.setAlignment(Qt.AlignCenter)
                QTimer.singleShot(3000, lambda: (self.close(), QApplication.quit(),))

        def remove_error_message(self):
            main_content_layout.removeWidget(status_label)
            status_label.hide()

        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path_up = os.path.abspath(os.path.join(base_path, "../.."))
        icon_path = os.path.join(base_path_up, "resources", "images", "lenaicon.ico")

        dialog = QDialog()
        dialog.setWindowIcon(QIcon(icon_path))
        dialog.setWindowTitle("Lena AI - Recover Password")
        dialog.setFixedSize(350, 300)
        dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        dialog.setStyleSheet(f"background-color: {theme_color[2]};")

        base_path = os.path.dirname(os.path.abspath(__file__))
        base_path_up = os.path.abspath(os.path.join(base_path, "../.."))

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        title_bar_dialog = TitleBarDialog()
        layout.addWidget(title_bar_dialog)

        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(15, 10, 15, 30)

        label = QLabel("New password")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"color: {theme_color[4]}; font-size: 20px; font-weight: 488; padding-bottom: 5px;")

        # Crea el layout para el campo de correo y el botón
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)

        passwords_layout = QVBoxLayout()
        passwords_layout.setContentsMargins(0, 0, 0, 0)

        self.text_new_password = QLineEdit()
        self.text_new_password.setPlaceholderText("New password...")
        self.text_new_password.setStyleSheet(f"color: {theme_color[4]}; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: {theme_color[1]};")
        self.text_new_password.setEchoMode(QLineEdit.Password)
        self.text_new_password.setFixedSize(320, 50)
        self.text_new_password.textChanged.connect(remove_error_message)

        toggle_button_2 = QPushButton()
        icon_path = os.path.join(base_path_up, "resources", "images", theme_color[4], "password", "showpassword.png")
        toggle_button_2.setIcon(QIcon(icon_path))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
        toggle_button_2.setCheckable(True)
        toggle_button_2.setStyleSheet("background: transparent; border: none; padding-right: 15px; padding-top: 3px;")
        toggle_button_2.setCursor(Qt.PointingHandCursor)
        toggle_button_2.clicked.connect(lambda: toggle_password_visibility_2(theme_color))

        password_layout_2 = QHBoxLayout()
        password_layout_2.addWidget(self.text_new_password)
        password_layout_2.addWidget(toggle_button_2)

        self.text_confirm_new_password = QLineEdit()
        self.text_confirm_new_password.setPlaceholderText("Confirm new password...")
        self.text_confirm_new_password.setStyleSheet(f"color: {theme_color[4]}; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: {theme_color[1]};")
        self.text_confirm_new_password.setEchoMode(QLineEdit.Password)
        self.text_confirm_new_password.setFixedSize(320, 50)
        self.text_confirm_new_password.textChanged.connect(remove_error_message)
        # text_actual_password.textChanged.connect(remove_error_message)

        toggle_button_3 = QPushButton()
        icon_path_3 = os.path.join(base_path_up, "resources", "images", theme_color[4], "password", "showpassword.png")
        toggle_button_3.setIcon(QIcon(icon_path_3))
        toggle_button_3.setCheckable(True)
        toggle_button_3.setStyleSheet("background: transparent; border: none; padding-right: 15px; padding-top: 3px;")
        toggle_button_3.setCursor(Qt.PointingHandCursor)
        toggle_button_3.clicked.connect(lambda: toggle_password_visibility_3(theme_color))

        password_layout_3 = QHBoxLayout()
        password_layout_3.addWidget(self.text_confirm_new_password)
        password_layout_3.addWidget(toggle_button_3)

        save_changes = QPushButton("Save changes")
        save_changes.setStyleSheet(f""" 
            background-color: {theme_color[0]}; 
            color: {theme_color[4]}; 
            padding: 10px; 
            border: 1px solid #ccc;
            border-radius: 10px; 
            font-size: 16px;
        """)
        save_changes.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor a puntero
        save_changes.clicked.connect(on_save_changes_button_click)

        passwords_layout.addLayout(password_layout_2)
        passwords_layout.addLayout(password_layout_3)
        input_layout.addLayout(passwords_layout)
        input_layout.addWidget(save_changes)

        # Agrega el label y el input_layout al main_content_layout
        main_content_layout.addWidget(label)
        main_content_layout.addLayout(input_layout)

        status_label = QLabel()
        status_label.setAlignment(Qt.AlignCenter)

        status_label_invalid = QLabel()
        status_label_invalid.setAlignment(Qt.AlignCenter)

        # Ahora, asigna main_content_layout al layout principal del diálogo
        layout.addLayout(main_content_layout)

        dialog.setLayout(layout)  # Asigna el layout principal al diálogo

        dialog.exec_()
        QApplication.quit()

    def closeEvent(self, event):
        # Aquí puedes realizar cualquier limpieza antes de cerrar
        print("El diálogo se ha cerrado.")
        event.accept()

