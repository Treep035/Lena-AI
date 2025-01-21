import os
import smtplib
import secrets
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from model.mail.check_email_to_db import check_email_to_db
from model.mail.save_token_to_db import save_token_to_db

def send_recovery_email(to_email):

    load_dotenv()
    # Configura el servidor SMTP (en este caso para Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = os.getenv('EMAIL')  # Reemplaza con tu correo
    from_password = os.getenv('PASSWORD')  # Reemplaza con tu contraseña de aplicación

    sent = check_email_to_db(to_email)
    if not sent:
        return sent
    
    recover_password_token = secrets.token_urlsafe(48)
    recover_password_token_expiration = datetime.now() + timedelta(hours=1)  # Expira en 1 hora
    save_token_to_db(to_email, recover_password_token, recover_password_token_expiration)
    enlace = f"lenaai://reset_password?token={recover_password_token}"

    subject = "Lena AI - Recuperación de Contraseña"
    body = f"""
Hello,<br>
We have received a request to reset the password for your account. If you did not make this request, you can ignore this message and no changes will be made to your account.<br><br>
If you wish to reset your password, please copy and paste the following link into your browser:<br>
<a href="{enlace}">{enlace}</a><br><br>
This link will expire in 24 hours.<br>
Thank you for using our services.<br>
Best regards,<br>
The Lena AI team.
"""

    # Crea un mensaje MIME multipart
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    # Agrega el cuerpo del mensaje
    msg = MIMEText(body, "html", "utf-8")
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