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
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal

switch_to_register = pyqtSignal()
switch_to_login = pyqtSignal()

def switch_to_register(self):
    # Emitir la señal al hacer clic en el enlace
    self.switch_to_register.emit()

def switch_to_login(self):
    # Emitir la señal al hacer clic en el enlace
    self.switch_to_login.emit()