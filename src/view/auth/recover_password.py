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

def recover_password(parent):
    dialog = QDialog(parent)
    dialog.setFixedSize(350, 175)
    dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
    dialog.setStyleSheet("background-color: #3F556B;")

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(0, 0, 0, 0)

    title_bar_dialog = TitleBarDialog()
    layout.addWidget(title_bar_dialog)

    main_content_layout = QVBoxLayout()
    main_content_layout.setContentsMargins(15, 10, 15, 30)

    label = QLabel("Forgot your password?")
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: white; font-size: 20px; font-weight: 488; padding-bottom: 5px;")

    # Crea el layout para el campo de correo y el botón
    input_layout = QHBoxLayout()
    input_layout.setContentsMargins(0, 0, 0, 0)

    email_input = QLineEdit()
    email_input.setPlaceholderText("Email...")
    email_input.setFixedSize(300, 40)
    email_input.setStyleSheet("border-radius: 10px; border: 1px solid #ccc; padding-left: 10px; color: white; background-color: #233240; margin-right: 25px;")

    send_button = QPushButton()
    send_icon = QPixmap("src/resources/images/sendmessage/sendwhite.png")  # Asegúrate de que esta ruta sea correcta
    send_button.setIcon(QIcon(send_icon))  # Establece la imagen como ícono
    send_button.setIconSize(QSize(18, 18))

    send_button.setStyleSheet("""
        border-radius: 17px;
        margin-bottom: 3px;
        margin-right: 5px;
        margin-top: 3px;
    """)
    send_button.setCursor(QCursor(Qt.PointingHandCursor))

    input_layout.addWidget(email_input)
    input_layout.addWidget(send_button)

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
        email = email_input.text()
        if email:
            sent = send_recovery_email_controller(email)
            if (sent):
                status_label.setText("Email sent successfully.")
                status_label.setStyleSheet("color: #BDECB6; font-size: 10px;")
                QTimer.singleShot(3000, lambda: dialog.accept())  # Cierra el diálogo después de enviar el correo
            else:
                status_label.setText(f"Error sending email.")
                status_label.setStyleSheet("color: #DE1F21; font-size: 10px;")

    # Conectar el botón con la función
    send_button.clicked.connect(on_send_clicked_or_enter)

    # Conectar el evento de la tecla Enter
    email_input.returnPressed.connect(on_send_clicked_or_enter)

    dialog.exec_()