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
from model.auth.validate_fields_change_password import validate_fields_change_password
from model.auth.validate_fields_change_name import validate_fields_change_name
# from model.auth.validate_fields_change_name import validate_fields_change_name

# Función validar los campos del login
def validate_fields_login_controller(self):
    no_fields, invalid_fields, logged_in, id_user = validate_fields_login(self)
    return no_fields, invalid_fields, logged_in, id_user
    
def validate_fields_register_controller(self):
    no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user = validate_fields_register(self)
    return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user

def validate_fields_change_password_controller(self):
    no_fields, not_actual_password, invalid_fields, invalid_regex, same_password = validate_fields_change_password(self)
    return no_fields, not_actual_password, invalid_fields, invalid_regex, same_password

def validate_fields_change_name_controller(self):
    no_fields, not_actual_name, invalid_fields, name_in_use, same_name = validate_fields_change_name(self)
    return no_fields, not_actual_name, invalid_fields, name_in_use, same_name