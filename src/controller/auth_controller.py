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

import bcrypt
import re
from datetime import datetime

from model.database.db_connection import connect_to_db
from model.auth.validate_fields_login import validate_fields_login
from model.auth.validate_fields_register import validate_fields_register

# Función validar los campos del login
def validate_fields_login_controller(self):
    no_fields, invalid_fields, logged_in, id_user = validate_fields_login(self)
    return no_fields, invalid_fields, logged_in, id_user
    

def validate_fields_register_controller(self):
    validate_fields_register(self)