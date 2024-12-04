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

import random
import webbrowser
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Chat(QMainWindow):
    def __init__(self):
        super().__init__()

        self.jugando_piedra_papel_tijeras = False

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
        self.chat_display.setStyleSheet("""
            QTextEdit {
                color: white; 
                background-color: #19232D; 
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
        message = self.message_input.text().strip().lower()  # Convertir el mensaje a minúsculas y quitar espacios

        # Diccionario de respuestas automáticas
        respuestas_bot = {
            ("hola", "buenas", "hi"): "¡Hola! ¿Cómo estás?",
            ("adiós", "bye", "hasta luego"): "¡Hasta luego! Espero verte pronto.",
            ("¿cómo estás?", "que tal estas?", "cómo te encuentras"): "Estoy aquí para ayudarte. ¿En qué puedo asistirte?",
            ("gracias", "thank you"): "¡De nada! Siempre a tu servicio.",
        }

        programas_disponibles = {
            "calculadora": "calc",  # En Windows
            "bloc de notas": "notepad",  # En Windows
            "navegador": "https://www.google.com",  # Cambiar por el navegador instalado
            "explorador": "explorer",  # Explorador de archivos en Windows
            "word": "winword",  # Microsoft Word en Windows
            "excel": "excel",  # Abre Microsoft Excel
            "powerpoint": "powerpnt", # Abre Microsoft PowerPoint
        }

        # Comprobar si el mensaje comienza con "busca"
        if any(form in message for form in ["busca", "busques", "buscases", "buscar"]):
            # Dividir el mensaje en palabras y encontrar la posición de la forma del verbo
            palabras = message.split()
            try:
                # Encontrar el índice de cualquiera de las formas del verbo
                indice_busca = next(i for i, word in enumerate(palabras) if word in ["busca", "busques", "buscases", "buscar"])
                # Combinar las palabras después de la forma del verbo para formar la consulta
                query = " ".join(palabras[indice_busca + 1:]).strip()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    bot_response = f"Buscando en Google: {query}"
                else:
                    bot_response = "Por favor, especifica qué deseas buscar."
            except StopIteration:
                bot_response = "No entendí qué buscar. Por favor, intenta de nuevo."

        elif message.startswith("abre"):
            programa = message[5:].strip()  # Obtener el texto después de "abre"
            if programa in programas_disponibles:
                try:
                    os.startfile(programas_disponibles[programa]) 
                    bot_response = f"Abriendo {programa}..."
                except Exception as e:
                    bot_response = f"No se pudo abrir {programa}: {str(e)}"
            else:
                bot_response = f"No conozco el programa '{programa}'. Por favor, verifica el nombre."

        elif message.startswith("cara o cruz"):
            resultado = random.choice(["Cara", "Cruz"])
            bot_response = f"El resultado es: {resultado}."

        elif "piedra papel tijeras" in message:
            # Instrucciones para jugar
            bot_response = (
                "¡Vamos a jugar Piedra, Papel o Tijeras! Escribe 'piedra', 'papel' o 'tijeras' para hacer tu elección."
            )
            self.jugando_piedra_papel_tijeras = True

        elif self.jugando_piedra_papel_tijeras:
            if message in ["piedra", "papel", "tijeras"]:
                opciones = ["piedra", "papel", "tijeras"]
                eleccion_bot = random.choice(opciones)

                if message == eleccion_bot:
                    resultado = "¡Empate!"
                elif (message == "piedra" and eleccion_bot == "tijeras") or \
                     (message == "papel" and eleccion_bot == "piedra") or \
                     (message == "tijeras" and eleccion_bot == "papel"):
                    resultado = "¡Ganaste!"
                else:
                    resultado = "Perdiste."

                bot_response = (
                    f"Tú elegiste: {message.capitalize()}. Lena eligió: {eleccion_bot.capitalize()}. {resultado}"
                )
                self.jugando_piedra_papel_tijeras = False  # Termina el juego
            else:
                bot_response = "Por favor, elige entre 'piedra', 'papel' o 'tijeras'."

        elif message.lower().startswith("nota de texto"):
            # Extraer el contenido de la nota
            contenido_nota = message[13:].strip()  # Quita "nota de texto"
            if contenido_nota:
                documents_path = os.path.join(os.path.expanduser("~"))
                # Crear un archivo de texto
                file_path = os.path.join(documents_path, "LenaAI.txt")  # Cambia el nombre del archivo si es necesario
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(contenido_nota)

                # Abrir el archivo en el bloc de notas
                os.startfile(file_path)

                bot_response = f"Nota de texto creada. Abriendo el documento..."
            else:
                bot_response = "Por favor, escribe algo después de 'nota de texto' para crear la nota."
        else:
            # Buscar una respuesta automática en el diccionario
            bot_response = next(
                (respuestas_bot[key] for key in respuestas_bot if message in key),
                "Lo siento, no entiendo esa pregunta."
            )

        for keys, response in respuestas_bot.items():
            if message in keys:
                bot_response = response
                break
        
        if message:
            # Crear el mensaje del usuario alineado a la derecha
            user_message = f"""
                <div style='text-align: right; margin-right: 75px;'>
                    <strong>User</strong><br>
                    <div style='background-color: #2C3E50; padding: 10px; border-radius: 10px; margin-bottom: 5px; display: inline-block; max-width: 80%; word-wrap: break-word;'>
                        {message}
                    </div>
                </div>
                """
            
            # Respuesta automática según el mensaje
            bot_message = f"""
            <div style='text-align: left; direction: ltr;'>
                <img src='src/resources/images/lenachat.png' alt='Foto de Lena' style='width: 30px; height: 30px; vertical-align: middle; margin-right: 10px; margin-left: -30px;'>
                <strong>Lena</strong><br>
                <div style='margin-left: 40px;'>{bot_response}</div>
            </div>
            """
            
            # Combinar ambos mensajes en el chat
            current_content = self.chat_display.toHtml()
            new_content = current_content + user_message + bot_message
            
            # Establecer el contenido completo con HTML
            self.chat_display.setHtml(new_content)

            self.chat_display.moveCursor(QTextCursor.End) 
            
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