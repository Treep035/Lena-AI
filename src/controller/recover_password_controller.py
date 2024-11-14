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
from PyQt5.QtCore import Qt, QEvent, QDate, QSize

from dotenv import load_dotenv

def send_recovery_email(to_email):

    load_dotenv()
    # Configura el servidor SMTP (en este caso para Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv('EMAIL')  # Reemplaza con tu correo
    from_password = os.getenv('PASSWORD')  # Reemplaza con tu contraseña de aplicación

    subject = "Recuperación de Contraseña"
    body = "Este es un correo de recuperación de contraseña. Haz clic en el siguiente enlace para restablecerla."

    # Crea un mensaje MIME multipart
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    # Agrega el cuerpo del mensaje
    msg = MIMEText(body, "plain", "utf-8")
    message.attach(msg)

    sent = False

    try:
        # Conexión al servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Inicia la conexión segura
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, message.as_string())
            print(f"Correo enviado a {to_email}")
            sent = True
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación. Verifica tu correo y contraseña.")
    except smtplib.SMTPException as e:
        print(f"Error al enviar el correo: {e}")
    
    return sent