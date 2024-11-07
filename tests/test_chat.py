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
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon, QCursor
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal, QSize

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Chat(QMainWindow):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #19232d;")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Crear un layout para los otros widgets
        # self.main_content_layout = QVBoxLayout()
        # self.main_content_layout.setContentsMargins(75, 10, 75, 125)  # Márgenes para el contenido

        self.chat_display = QTextEdit(self)
        self.chat_display.setStyleSheet("color: white; background-color: #19232D; border: none;")
        self.chat_display.setReadOnly(True)  # No se puede escribir directamente aquí
        self.layout.addWidget(self.chat_display)
        
        # Crear un layout horizontal para el cuadro de entrada y el botón de envío
        self.input_layout = QHBoxLayout()
        
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
            background-color: #3F556B;
            border: none;
            border-radius: 25px;  /* Esto hace que el botón sea circular */
            width: 55px;  /* Tamaño del botón */
            height: 55px;  /* Tamaño del botón */
            margin-bottom: 3px;
            margin-right: 5px;
        """)
        self.send_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        
        # Añadir el layout de entrada al layout principal
        self.layout.addLayout(self.input_layout)
        
    def send_message(self):
        message = self.message_input.text()
        
        if message:
            # Crear el mensaje del usuario alineado a la derecha
            user_message = f"""
                <div style='text-align: right;'>
                    <strong>User</strong><br>
                    <div style='background-color: #2C3E50; padding: 10px; border-radius: 10px; margin-bottom: 5px; display: inline-block; max-width: 80%; word-wrap: break-word;'>
                        {message}
                    </div>
                </div>
                """
            
            # Respuesta automática del bot alineada a la izquierda
            bot_message = f"""
<div style='text-align: left; direction: ltr;'>
    <img src='src/resources/images/lenachat.png' alt='Foto de Lena' style='width: 30px; height: 30px; vertical-align: middle; margin-right: 10px;'>
    <strong>Lena</strong><br>
    Hola, ¿en qué puedo ayudarte?
</div>
"""


            
            # Combinar ambos mensajes en el chat
            current_content = self.chat_display.toHtml()
            new_content = current_content + user_message + bot_message
            
            # Establecer el contenido completo con HTML
            self.chat_display.setHtml(new_content)
            
            # Limpiar el cuadro de entrada
            self.message_input.clear()


            # Aquí podrías agregar lógica para simular una respuesta automática o procesar el mensaje


        # Añadir el layout de contenido principal al layout de la ventana
        # self.layout.addLayout(self.main_content_layout)
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