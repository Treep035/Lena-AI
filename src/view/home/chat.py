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
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon, QCursor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal, QSize, QTimer, QBuffer, QIODevice

import base64
from io import BytesIO

import random
import webbrowser
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.controller.process_message_controller import process_message_controller
from src.controller.account_load_controller import account_username_load_controller, account_picture_load_controller

class Chat(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jugando_piedra_papel_tijeras = False
        self.adivinanza_actual = None

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #233240;")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Crear un layout para los otros widgets
        # self.main_content_layout = QVBoxLayout()
        # self.main_content_layout.setContentsMargins(75, 10, 75, 125)  # Márgenes para el contenido

        self.chat_display = QTextEdit(self)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                color: white; 
                background-color: #233240; 
                border: none;
                font-size: 15px;
            }
            QScrollBar:vertical {
                background: #2C3E50;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3F556B;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.chat_display.setReadOnly(True)  # No se puede escribir directamente aquí
        self.layout.addWidget(self.chat_display)
        
        # Crear un layout horizontal para el cuadro de entrada y el botón de envío
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 15, 0, 0)
        
        # Crear el cuadro de entrada para nuevos mensajes
        self.message_input = QLineEdit(self)
        self.message_input.setStyleSheet("""
            color: white; 
            background-color: #3F556B; 
            border: none;
            border-top-right-radius: 20px;  /* Solo redondear la esquina superior derecha */
            border-bottom-right-radius: 20px;  /* Solo redondear la esquina inferior derecha */ 
            padding-left: 12px;
            margin-bottom: 3px;
        """)
        self.message_input.setPlaceholderText("Envía un mensaje a Lena AI")
        self.message_input.setFixedHeight(55)
        self.input_layout.addWidget(self.message_input)
        
        # Crear el botón para enviar el mensaje
        self.send_button = QPushButton(self)
        send_icon = QPixmap("src/resources/images/sendmessage/sendwhite.png")  # Reemplaza con la ruta de la imagen que deseas usar
        self.send_button.setIcon(QIcon(send_icon))  # Establece la imagen como ícono
        
        self.send_button.setIconSize(QSize(18, 18))

        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #3F556B;
                border: none;
                border-radius: 25px;  /* Esto hace que el botón sea circular */
                width: 55px;  /* Tamaño del botón */
                height: 55px;  /* Tamaño del botón */
                margin-bottom: 3px;
                margin-right: 5px;
            }
            QPushButton:hover {
                background-color: #364758;  /* Color al pasar el cursor */
            }
        """)
        self.send_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        
        # Añadir el layout de entrada al layout principal
        self.layout.addLayout(self.input_layout)
        
    def send_message(self):
        original_message = self.message_input.text()
        message = original_message.strip().lower()  # Convertir el mensaje a minúsculas y quitar espacios

        username = account_username_load_controller()

        user_image_path = account_picture_load_controller()
        pixmap = QPixmap(user_image_path)
        size = 52
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)  # Fondo transparente

        # Pintar la imagen en un círculo
        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        # Crear un buffer en memoria
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)

        # Guardar la imagen en el buffer
        circular_pixmap.save(buffer, format='PNG')

        # Asegúrate de mover el puntero al principio del buffer
        buffer.seek(0)

        # Leer los datos completos del buffer y convertirlo a base64
        img_base64 = base64.b64encode(buffer.read(buffer.size())).decode('utf-8')

        if message:
            # Crear el mensaje del usuario alineado a la derecha
            user_message = f"""
<div style="text-align: right; direction: rtl; display: flex; align-items: center; justify-content: flex-end; margin-right: 35px;">
    <strong>{username}</strong>
    <img src='data:image/png;base64,{img_base64}' alt='Foto de Lena' style='width: 30px; height: 30px; vertical-align: middle; margin-left: 10px;'>
</div>
<div style="margin-right: 75px; text-align: left; padding: 10px 15px; border-radius: 10px; margin-bottom: 20px; background-color: #2C3E50; display: inline-block; max-width: 80%; word-wrap: break-word; overflow-wrap: break-word; white-space: pre-wrap;">
    <span style="display: block; margin-left: 0;">{original_message}</span>
</div>
"""
            
            current_content = self.chat_display.toHtml()
            self.chat_display.setHtml(current_content + user_message)
            self.chat_display.moveCursor(QTextCursor.End)

            self.message_input.clear()

            QTimer.singleShot(100, lambda: self.show_bot_response(message))

    def show_bot_response(self, message):
        bot_response = process_message_controller(self, message)

        # Mostrar mensaje del bot
        bot_message = f"""
<div style='text-align: left; direction: ltr; display: flex; align-items: center;'>
    <img src='src/resources/images/lenachat.png' alt='Foto de Lena' style='width: 30px; height: 30px; vertical-align: middle; margin-right: 10px;'>
    <strong>Lena</strong>
</div>
<div style='margin-left: 80px; margin-right: 80px; text-align: left; padding: 10px 15px; border-radius: 10px; margin-bottom: 20px;'>
{bot_response}
</div>
"""

        current_content = self.chat_display.toHtml()
        self.chat_display.setHtml(current_content + bot_message)
        self.chat_display.moveCursor(QTextCursor.End)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() == Qt.ShiftModifier:
                # Si Shift + Enter, añadir un salto de línea en el QLineEdit
                self.message_input.insert("\n")
            else:
                # Si solo Enter, enviar el mensaje
                self.send_message()
        else:
            super().keyPressEvent(event)  # Dejar que otros eventos se manejen normalmente