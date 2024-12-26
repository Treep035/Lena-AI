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

def change_password(event, parent):

    def toggle_password_visibility():
        if toggle_button.isChecked():
            text_actual_password.setEchoMode(QLineEdit.Normal)
            toggle_button.setIcon(QIcon("src/resources/images/password/white/hidepasswordwhite.png"))
        else:
            text_actual_password.setEchoMode(QLineEdit.Password)
            toggle_button.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))

    def toggle_password_visibility_2():
        if toggle_button_2.isChecked():
            text_new_password.setEchoMode(QLineEdit.Normal)
            toggle_button_2.setIcon(QIcon("src/resources/images/password/white/hidepasswordwhite.png"))
        else:
            text_new_password.setEchoMode(QLineEdit.Password)
            toggle_button_2.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))

    def toggle_password_visibility_3():
        if toggle_button_3.isChecked():
            text_confirm_new_password.setEchoMode(QLineEdit.Normal)
            toggle_button_3.setIcon(QIcon("src/resources/images/password/white/hidepasswordwhite.png"))
        else:
            text_confirm_new_password.setEchoMode(QLineEdit.Password)
            toggle_button_3.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))

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

    label = QLabel("Cambiar contraseña")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: white; font-size: 20px; font-weight: 488; padding-bottom: 5px;")

    # Crea el layout para el campo de correo y el botón
    input_layout = QVBoxLayout()
    input_layout.setContentsMargins(0, 0, 0, 0)

    text_actual_password = QLineEdit()
    text_actual_password.setPlaceholderText("Contraseña actual...")
    text_actual_password.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: #233240;")
    text_actual_password.setEchoMode(QLineEdit.Password)
    text_actual_password.setFixedSize(300, 50)
    # text_actual_password.textChanged.connect(remove_error_message)

    toggle_button = QPushButton()
    toggle_button.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
    toggle_button.setCheckable(True)
    toggle_button.setStyleSheet("background: transparent; border: none; padding-right: 30px; padding-top: 3px;")
    toggle_button.setCursor(Qt.PointingHandCursor)
    toggle_button.clicked.connect(toggle_password_visibility)

    passwords_layout = QVBoxLayout()
    passwords_layout.setContentsMargins(0, 0, 0, 0)

    password_layout = QHBoxLayout()
    password_layout.setContentsMargins(0, 0, 0, 0)
    password_layout.addWidget(text_actual_password)
    password_layout.addWidget(toggle_button)

    text_new_password = QLineEdit()
    text_new_password.setPlaceholderText("Nueva contraseña...")
    text_new_password.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: #233240;")
    text_new_password.setEchoMode(QLineEdit.Password)
    text_new_password.setFixedSize(300, 50)
    # text_actual_password.textChanged.connect(remove_error_message)

    toggle_button_2 = QPushButton()
    toggle_button_2.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
    toggle_button_2.setCheckable(True)
    toggle_button_2.setStyleSheet("background: transparent; border: none; padding-right: 30px; padding-top: 3px;")
    toggle_button_2.setCursor(Qt.PointingHandCursor)
    toggle_button_2.clicked.connect(toggle_password_visibility_2)

    password_layout_2 = QHBoxLayout()
    password_layout_2.addWidget(text_new_password)
    password_layout_2.addWidget(toggle_button_2)

    text_confirm_new_password = QLineEdit()
    text_confirm_new_password.setPlaceholderText("Confirmar nueva contraseña...")
    text_confirm_new_password.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px; padding-left: 10px; padding-right: 45px; background-color: #233240;")
    text_confirm_new_password.setEchoMode(QLineEdit.Password)
    text_confirm_new_password.setFixedSize(300, 50)
    # text_actual_password.textChanged.connect(remove_error_message)

    toggle_button_3 = QPushButton()
    toggle_button_3.setIcon(QIcon("src/resources/images/password/white/showpasswordwhite.png"))  # Cambia "path/to/eye_icon.png" a la ruta de tu icono de ojo self
    toggle_button_3.setCheckable(True)
    toggle_button_3.setStyleSheet("background: transparent; border: none; padding-right: 30px; padding-top: 3px;")
    toggle_button_3.setCursor(Qt.PointingHandCursor)
    toggle_button_3.clicked.connect(toggle_password_visibility_3)

    password_layout_3 = QHBoxLayout()
    password_layout_3.addWidget(text_confirm_new_password)
    password_layout_3.addWidget(toggle_button_3)

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

    passwords_layout.addLayout(password_layout)
    passwords_layout.addLayout(password_layout_2)
    passwords_layout.addLayout(password_layout_3)
    input_layout.addLayout(passwords_layout)
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
    # actual_name_input.returnPressed.connect(on_send_clicked_or_enter)

    dialog.exec_()