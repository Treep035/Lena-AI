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

def change_name(event, parent):
    dialog = QDialog(parent)
    dialog.setFixedSize(350, 350)
    dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
    dialog.setStyleSheet("background-color: #3F556B;")

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(0, 0, 0, 0)

    title_bar_dialog = TitleBarDialog()
    layout.addWidget(title_bar_dialog)

    main_content_layout = QVBoxLayout()
    main_content_layout.setContentsMargins(15, 10, 15, 30)

    label = QLabel("Cambiar nombre de usuario")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: white; font-size: 20px; font-weight: 488; padding-bottom: 5px;")

    # Crea el layout para el campo de correo y el botón
    input_layout = QVBoxLayout()
    input_layout.setContentsMargins(0, 0, 0, 0)

    actual_name_input = QLineEdit()
    actual_name_input.setPlaceholderText("Nombre actual...")
    actual_name_input.setFixedSize(325, 50)
    actual_name_input.setStyleSheet("border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: white; background-color: #233240; margin-right: 25px;")

    modified_name_input = QLineEdit()
    modified_name_input.setPlaceholderText("Nuevo nombre...")
    modified_name_input.setFixedSize(325, 50)
    modified_name_input.setStyleSheet("border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: white; background-color: #233240; margin-right: 25px;")

    confirm_modified_name_input = QLineEdit()
    confirm_modified_name_input.setPlaceholderText("Confirmar nuevo nombre...")
    confirm_modified_name_input.setFixedSize(325, 50)
    confirm_modified_name_input.setStyleSheet("border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: white; background-color: #233240; margin-right: 25px;")

    save_changes = QPushButton("Guardar cambios")
    save_changes.setStyleSheet(""" 
        background-color: #2C3E50; 
        color: white; 
        padding: 10px; 
        border: 1px solid #ccc;
        border-radius: 10px; 
        font-size: 16px;
    """)
    save_changes.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor a puntero
    # save_changes.clicked.connect()

    input_layout.addWidget(actual_name_input)
    input_layout.addWidget(modified_name_input)
    input_layout.addWidget(confirm_modified_name_input)
    input_layout.addWidget(save_changes)

    # Agrega el label y el input_layout al main_content_layout
    main_content_layout.addWidget(label)
    main_content_layout.addLayout(input_layout)

    status_label = QLabel()
    status_label.setAlignment(Qt.AlignLeft)
    status_label.setStyleSheet("color: white; font-size: 10px;")
    main_content_layout.addWidget(status_label)

    # Ahora, asigna main_content_layout al layout principal del diálogo
    layout.addLayout(main_content_layout)

    dialog.setLayout(layout)  # Asigna el layout principal al diálogo

    def on_send_clicked_or_enter():
        print("prueba")

    # Conectar el botón con la función
    # send_button.clicked.connect(on_send_clicked_or_enter)

    # Conectar el evento de la tecla Enter
    actual_name_input.returnPressed.connect(on_send_clicked_or_enter)

    dialog.exec_()