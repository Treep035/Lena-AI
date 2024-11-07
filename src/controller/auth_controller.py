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
    QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon
from PyQt5.QtCore import Qt, QEvent, QDate

# Función recuperar contraseña
def recover_password(parent):
    QMessageBox.information(parent, "Recuperar contraseña", "Función de recuperación de contraseña activada.")

# Función validar los campos del login
def validate_fields(self):
    email = self.text_email.text().strip()
    password = self.text_password.text().strip()

    # Verifica que los campos no estén vacíos
    if not email or not password:
        QMessageBox.warning(self, "Lena AI", "Please fill in all fields.")
        return

    # Si todo es válido
    QMessageBox.information(self, "Success", "All fields are valid!")