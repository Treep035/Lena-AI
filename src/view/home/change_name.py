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
from PyQt5.QtCore import Qt, QEvent, QDate, QSize, QTimer, pyqtSignal

from view.shared.titlebar_dialog import TitleBarDialog
from controller.recover_password_controller import send_recovery_email_controller
from controller.theme_controller import get_theme_controller
from resources.styles.theme import change_theme
from controller.auth_controller import validate_fields_change_name_controller

def change_name(event, parent):

    theme = get_theme_controller()
    theme_color = change_theme(parent, theme)

    def on_save_changes_button_click(self):
        no_fields, not_actual_name, invalid_fields, name_in_use, same_name = validate_fields_change_name_controller(parent)
        if no_fields:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label)
            status_label.show()
            status_label.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Por favor, completa todos los campos</a>")
            status_label.setAlignment(Qt.AlignCenter)
        
        if not_actual_name:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>El nombre actual es incorrecto</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if invalid_fields:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>Los dos nombres no coinciden</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if name_in_use:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>El nuevo nombre ya está en uso</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if same_name:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label_invalid)
            status_label_invalid.show()
            status_label_invalid.setText("<a href='#' style='color: #C53B3D ; font-size: 15px; font-weight: bold; text-decoration: none;'>El nuevo nombre no puede ser el mismo que el actual</a>")
            status_label_invalid.setAlignment(Qt.AlignCenter)

        if not no_fields and not not_actual_name and not invalid_fields and not name_in_use and not same_name:
            main_content_layout.removeWidget(status_label_invalid)
            status_label_invalid.hide()
            main_content_layout.addWidget(status_label)
            status_label.show()
            status_label.setText("<a href='#' style='color: #0e7101; font-size: 15px; font-weight: bold; text-decoration: none;'>Nombre de usuario cambiado con éxito</a>")
            status_label.setAlignment(Qt.AlignCenter)
            self.account_username_update_signal.emit()
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

    label = QLabel("Cambiar nombre de usuario")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet(f"color: {theme_color[4]}; font-size: 20px; font-weight: 488; padding-bottom: 5px;")

    # Crea el layout para el campo de correo y el botón
    input_layout = QVBoxLayout()
    input_layout.setContentsMargins(0, 0, 0, 0)

    parent.actual_name_input = QLineEdit()
    parent.actual_name_input.setPlaceholderText("Nombre actual...")
    parent.actual_name_input.setFixedSize(345, 50)
    parent.actual_name_input.setStyleSheet(f"border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: {theme_color[4]}; background-color: {theme_color[1]}; margin-right: 25px;")
    parent.actual_name_input.textChanged.connect(remove_error_message)

    parent.modified_name_input = QLineEdit()
    parent.modified_name_input.setPlaceholderText("Nuevo nombre...")
    parent.modified_name_input.setFixedSize(345, 50)
    parent.modified_name_input.setStyleSheet(f"border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: {theme_color[4]}; background-color: {theme_color[1]}; margin-right: 25px;")
    parent.modified_name_input.textChanged.connect(remove_error_message)

    parent.confirm_modified_name_input = QLineEdit()
    parent.confirm_modified_name_input.setPlaceholderText("Confirmar nuevo nombre...")
    parent.confirm_modified_name_input.setFixedSize(345, 50)
    parent.confirm_modified_name_input.setStyleSheet(f"border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: {theme_color[4]}; background-color: {theme_color[1]}; margin-right: 25px;")
    parent.confirm_modified_name_input.textChanged.connect(remove_error_message)

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
    save_changes.clicked.connect(lambda: on_save_changes_button_click(parent))

    input_layout.addWidget(parent.actual_name_input)
    input_layout.addWidget(parent.modified_name_input)
    input_layout.addWidget(parent.confirm_modified_name_input)
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