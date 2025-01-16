import sys
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
from PyQt5.QtCore import Qt, QEvent, QDate, QSize, QTimer

from view.shared.titlebar_dialog import TitleBarDialog
from controller.recover_password_controller import send_recovery_email_controller
from controller.theme_controller import get_theme_controller
from controller.auth_controller import validate_fields_change_password_controller
from resources.styles.theme import change_theme

def change_password(event, parent):

    theme = get_theme_controller()
    theme_color = change_theme(parent, theme)

    def toggle_password_visibility(theme_color, self):
        if toggle_button.isChecked():
            self.text_actual_password.setEchoMode(QLineEdit.Normal)
            toggle_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/hidepassword.png"))
        else:
            self.text_actual_password.setEchoMode(QLineEdit.Password)
            toggle_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/showpassword.png"))

    def toggle_password_visibility_2(theme_color, self):
        if toggle_button_2.isChecked():
            self.text_new_password.setEchoMode(QLineEdit.Normal)
            toggle_button_2.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/hidepassword.png"))
        else:
            self.text_new_password.setEchoMode(QLineEdit.Password)
            toggle_button_2.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/showpassword.png"))

    def toggle_password_visibility_3(theme_color, self):
        if toggle_button_3.isChecked():
            self.text_confirm_new_password.setEchoMode(QLineEdit.Normal)
            toggle_button_3.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/hidepassword.png"))
        else:
            self.text_confirm_new_password.setEchoMode(QLineEdit.Password)
            toggle_button_3.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/showpassword.png"))

    def on_save_changes_button_click():
        no_fields, not_actual_password, invalid_fields, invalid_regex, same_password = validate_fields_change_password_controller(parent)
        if no_fields:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label)
            status_label.show()
            status_label.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Por favor, completa todos los campos</a>")
            status_label.setAlignment(Qt.AlignCenter)
        
        if not_actual_password:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>La contraseña actual es incorrecta</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if invalid_fields:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Las dos contraseñas no coinciden</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if invalid_regex:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Contraseña inválida</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if same_password:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>La nueva contraseña debe ser diferente</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if not no_fields and not not_actual_password and not invalid_fields and not invalid_regex and not same_password:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label)
            status_label.show()
            status_label.setText("<a href='#' style='color: #0e7101; font-size: 15px; font-weight: bold; text-decoration: none;'>Contraseña cambiada con éxito</a>")
            status_label.setAlignment(Qt.AlignCenter)
            QTimer.singleShot(3000, dialog.close)

    def remove_error_message(self):
        main_content_layout.removeWidget(status_label)
        status_label.hide()

    dialog = QDialog(parent)
    dialog.setFixedSize(350, 350)
    dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
    dialog.setStyleSheet(f"background-color: {theme_color[2]};")

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(0, 0, 0, 0)

    title_bar_dialog = TitleBarDialog()
    layout.addWidget(title_bar_dialog)

    main_content_layout = QVBoxLayout()
    main_content_layout.setContentsMargins(15, 10, 15, 30)

    label = QLabel("Cambiar contraseña")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(f"color: {theme_color[4]}; font-size: 20px; font-weight: 488; padding-bottom: 5px;")

    # Crea el layout para el campo de correo y el botón
    input_layout = QVBoxLayout()
    input_layout.setContentsMargins(0, 0, 0, 0)

    parent.text_actual_password = QLineEdit()
    parent.text_actual_password.setPlaceholderText("Contraseña actual...")
    parent.text_actual_password.setStyleSheet(f"color: {theme_color[4]}; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: {theme_color[1]};")
    parent.text_actual_password.setEchoMode(QLineEdit.Password)
    parent.text_actual_password.setFixedSize(320, 50)
    parent.text_actual_password.textChanged.connect(remove_error_message)
    # text_actual_password.textChanged.connect(remove_error_message)

    toggle_button = QPushButton()
    toggle_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/showpassword.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
    toggle_button.setCheckable(True)
    toggle_button.setStyleSheet("background: transparent; border: none; padding-right: 15px; padding-top: 3px;")
    toggle_button.setCursor(Qt.PointingHandCursor)
    toggle_button.clicked.connect(lambda: toggle_password_visibility(theme_color, parent))

    passwords_layout = QVBoxLayout()
    passwords_layout.setContentsMargins(0, 0, 0, 0)

    password_layout = QHBoxLayout()
    password_layout.setContentsMargins(0, 0, 0, 0)
    password_layout.addWidget(parent.text_actual_password)
    password_layout.addWidget(toggle_button)

    parent.text_new_password = QLineEdit()
    parent.text_new_password.setPlaceholderText("Nueva contraseña...")
    parent.text_new_password.setStyleSheet(f"color: {theme_color[4]}; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: {theme_color[1]};")
    parent.text_new_password.setEchoMode(QLineEdit.Password)
    parent.text_new_password.setFixedSize(320, 50)
    parent.text_new_password.textChanged.connect(remove_error_message)
    # text_actual_password.textChanged.connect(remove_error_message)

    toggle_button_2 = QPushButton()
    toggle_button_2.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/showpassword.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
    toggle_button_2.setCheckable(True)
    toggle_button_2.setStyleSheet("background: transparent; border: none; padding-right: 15px; padding-top: 3px;")
    toggle_button_2.setCursor(Qt.PointingHandCursor)
    toggle_button_2.clicked.connect(lambda: toggle_password_visibility_2(theme_color, parent))

    password_layout_2 = QHBoxLayout()
    password_layout_2.addWidget(parent.text_new_password)
    password_layout_2.addWidget(toggle_button_2)

    parent.text_confirm_new_password = QLineEdit()
    parent.text_confirm_new_password.setPlaceholderText("Confirmar nueva contraseña...")
    parent.text_confirm_new_password.setStyleSheet(f"color: {theme_color[4]}; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: {theme_color[1]};")
    parent.text_confirm_new_password.setEchoMode(QLineEdit.Password)
    parent.text_confirm_new_password.setFixedSize(320, 50)
    parent.text_confirm_new_password.textChanged.connect(remove_error_message)
    # text_actual_password.textChanged.connect(remove_error_message)

    toggle_button_3 = QPushButton()
    toggle_button_3.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/password/showpassword.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
    toggle_button_3.setCheckable(True)
    toggle_button_3.setStyleSheet("background: transparent; border: none; padding-right: 15px; padding-top: 3px;")
    toggle_button_3.setCursor(Qt.PointingHandCursor)
    toggle_button_3.clicked.connect(lambda: toggle_password_visibility_3(theme_color, parent))

    password_layout_3 = QHBoxLayout()
    password_layout_3.addWidget(parent.text_confirm_new_password)
    password_layout_3.addWidget(toggle_button_3)

    save_changes = QPushButton("Guardar cambios")
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

    passwords_layout.addLayout(password_layout)
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