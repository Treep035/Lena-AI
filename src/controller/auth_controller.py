import sys
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

from model.database.db_connection import connect_to_db

# Función validar los campos del login
def validate_fields_login(self):
    email = self.text_email.text().strip()
    password = self.text_password.text().strip()

    # Verifica que los campos no estén vacíos
    if not email or not password:
        QMessageBox.warning(self, "Lena AI", "Please fill in all fields.")
        return

    # Si todo es válido
    QMessageBox.information(self, "Success", "All fields are valid!")

def validate_fields_register(self):
    username = self.text_username.text().strip()
    email = self.text_email.text().strip()
    password = self.text_password.text().strip()
    birthdate = self.date_birthdate.date()

    # Verifica que los campos no estén vacíos
    if not username or not email or not password:
        QMessageBox.warning(self, "Lena AI", "Please fill in all fields.")
        return
        
    connection = None
    cursor = None
        
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()

            theme_mode = "default"
            language = "eng"
                
            query = "INSERT INTO users (username, email, password, birthday, theme_mode, language) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, email, password, birthdate, theme_mode, language))
            connection.commit()
            
        QMessageBox.information(self, "Success", "Registration successful!")
    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Si todo es válido
    QMessageBox.information(self, "Success", "All fields are valid!")