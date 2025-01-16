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
from controller.theme_controller import get_theme_controller
from resources.styles.theme import change_theme
from view.home.configuration import Configuration

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

        theme = get_theme_controller()
        theme_color = change_theme(self, theme)

        self.jugando_piedra_papel_tijeras = False
        self.adivinanza_actual = None

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f"background-color: {theme_color[1]}")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Crear un layout para los otros widgets
        # self.main_content_layout = QVBoxLayout()
        # self.main_content_layout.setContentsMargins(75, 10, 75, 125)  # Márgenes para el contenido

        self.chat_display = QTextEdit(self)
        self.chat_display.setStyleSheet(f"""
            QTextEdit {{
                color: {theme_color[4]}; 
                background-color: {theme_color[1]}; 
                border: none;
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                background: {theme_color[0]};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme_color[2]};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        self.chat_display.setReadOnly(True)  # No se puede escribir directamente aquí
        self.layout.addWidget(self.chat_display)

        # Crear el botón circular en la esquina superior izquierda
        self.clear_button = QPushButton(self)
        self.clear_button.setFixedSize(50, 50)  # Tamaño del botón circular
        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_color[2]};
                border: none;
                border-radius: 25px;  /* Hace que el botón sea perfectamente circular */
                position: absolute;
            }}
            QPushButton:hover {{
                background-color: {theme_color[0]};
            }}
        """)
        self.clear_button.setCursor(QCursor(Qt.PointingHandCursor))

        # Cargar la imagen dentro del botón
        self.clear_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/clear/clear.png"))
        self.clear_button.setIconSize(QSize(35, 35))  # Tamaño de la imagen dentro del botón

        self.clear_button.move(10, 10)
        self.clear_button.clicked.connect(self.clear_chat)
        # self.layout.addWidget(self.clear_button)

        # Crear el botón de "Flecha hacia abajo"
        self.scroll_button = QPushButton(self)
        self.scroll_button.setFixedSize(35, 35)
        self.scroll_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_color[2]};
                border: none;
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background-color: {theme_color[0]};
            }}
        """)
        self.scroll_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.scroll_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/downarrow/downarrow.png"))
        self.scroll_button.setIconSize(QSize(15, 15))
        self.scroll_button.clicked.connect(self.scroll_to_bottom)
        self.scroll_button.hide()  # Ocultar inicialmente

        # Conectar el evento de scroll
        self.chat_display.verticalScrollBar().valueChanged.connect(self.handle_scroll)
        
        # Crear un layout horizontal para el cuadro de entrada y el botón de envío
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 2, 0, 0)
        
        # Crear el cuadro de entrada para nuevos mensajes
        self.message_input = QLineEdit(self)
        self.message_input.setStyleSheet(f"""
            color: {theme_color[4]}; 
            background-color: {theme_color[2]}; 
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
        send_icon = QPixmap(f"src/resources/images/{theme_color[4]}/sendmessage/sendmessage.png")  # Reemplaza con la ruta de la imagen que deseas usar
        self.send_button.setIcon(QIcon(send_icon))  # Establece la imagen como ícono
        
        self.send_button.setIconSize(QSize(18, 18))

        self.send_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_color[2]};
                border: none;
                border-radius: 25px;  /* Esto hace que el botón sea circular */
                width: 55px;  /* Tamaño del botón */
                height: 55px;  /* Tamaño del botón */
                margin-bottom: 3px;
                margin-right: 5px;
            }}
            QPushButton:hover {{
                background-color: {theme_color[0]};  /* Color al pasar el cursor */
            }}
        """)
        self.send_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        
        # Añadir el layout de entrada al layout principal
        self.layout.addLayout(self.input_layout)

        self.configuracion = Configuration.get_instance()
        self.configuracion.theme_changed.connect(self.update_theme_chat)
        
    def handle_scroll(self):
        scrollbar = self.chat_display.verticalScrollBar()
        if scrollbar.value() < scrollbar.maximum():  # Usuario no está en el final
            self.scroll_button.show()
        else:  # Usuario está en el final
            self.scroll_button.hide()

    def scroll_to_bottom(self):
        scrollbar = self.chat_display.verticalScrollBar()
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(lambda: self.smooth_scroll(scrollbar))
        self.scroll_timer.start(5)  # Velocidad rápida

    def smooth_scroll(self, scrollbar):
        current_value = scrollbar.value()
        max_value = scrollbar.maximum()
        step = 15  # Velocidad de desplazamiento
        if current_value + step >= max_value:
            scrollbar.setValue(max_value)
            self.scroll_timer.stop()
        else:
            scrollbar.setValue(current_value + step)

    def send_message(self):
        theme = get_theme_controller()
        theme_color = change_theme(self, theme)

        original_message = self.message_input.text()
        message = original_message.strip().lower()  # Convertir el mensaje a minúsculas y quitar espacios

        username = account_username_load_controller()

        user_image_path = account_picture_load_controller(theme_color)
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
<div style="margin-right: 75px; text-align: left; padding: 10px 15px; border-radius: 10px; margin-bottom: 20px; background-color: {theme_color[0]}; display: inline-block; max-width: 80%; word-wrap: break-word; overflow-wrap: break-word; white-space: pre-wrap;">
    <span style="display: block; margin-left: 0;">{original_message}</span>
</div>
"""
            
            current_content = self.chat_display.toHtml()
            self.chat_display.setHtml(current_content + user_message)
            self.chat_display.moveCursor(QTextCursor.End)
            self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

            self.message_input.clear()

            QTimer.singleShot(100, lambda: self.show_bot_response(message))

    def show_bot_response(self, message):
        theme = get_theme_controller()
        theme_color = change_theme(self, theme)
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
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def clear_chat(self):
        self.chat_display.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.clear_button.move(10, 10)
        self.scroll_button.move(self.width() - 240, self.height() - 100)

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

    def update_theme_chat(self):
        theme = get_theme_controller()
        theme_color = change_theme(self, theme)
        self.central_widget.setStyleSheet(f"background-color: {theme_color[1]}")
        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_color[2]};
                border: none;
                border-radius: 25px;  /* Hace que el botón sea perfectamente circular */
                position: absolute;
            }}
            QPushButton:hover {{
                background-color: {theme_color[0]};
            }}
        """)
        self.clear_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/clear/clear.png"))
        self.scroll_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_color[2]};
                border: none;
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background-color: {theme_color[0]};
            }}
        """)
        self.scroll_button.setIcon(QIcon(f"src/resources/images/{theme_color[4]}/downarrow/downarrow.png"))
        self.chat_display.setStyleSheet(f"""
            QTextEdit {{
                color: {theme_color[4]}; 
                background-color: {theme_color[1]}; 
                border: none;
                font-size: 15px;
            }}
            QScrollBar:vertical {{
                background: {theme_color[0]};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme_color[2]};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

        self.message_input.setStyleSheet(f"""
            color: {theme_color[4]}; 
            background-color: {theme_color[2]}; 
            border: none;
            border-top-right-radius: 20px;  /* Solo redondear la esquina superior derecha */
            border-bottom-right-radius: 20px;  /* Solo redondear la esquina inferior derecha */ 
            padding-left: 12px;
            margin-bottom: 3px;
        """)

        send_icon = QPixmap(f"src/resources/images/{theme_color[4]}/sendmessage/sendmessage.png")  # Reemplaza con la ruta de la imagen que deseas usar
        self.send_button.setIcon(QIcon(send_icon))  # Establece la imagen como ícono
        
        self.send_button.setIconSize(QSize(18, 18))
        self.send_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_color[2]};
                border: none;
                border-radius: 25px;  /* Esto hace que el botón sea circular */
                width: 55px;  /* Tamaño del botón */
                height: 55px;  /* Tamaño del botón */
                margin-bottom: 3px;
                margin-right: 5px;
            }}
            QPushButton:hover {{
                background-color: {theme_color[0]};  /* Color al pasar el cursor */
            }}
        """)
        # current_content = self.chat_display.toHtml()  # Obtener el contenido actual
        # self.chat_display.clear()  # Limpiar el QTextEdit
        # self.chat_display.setHtml(current_content)