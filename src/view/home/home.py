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
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal
import threading
import sys
import os
from resources.styles.theme import change_theme
from controller.theme_controller import get_theme_controller
from controller.process_voice_message_controller import process_voice_message_controller, stop_process_voice_message_controller
from view.home.configuration import Configuration
from view.shared.titlebar import TitleBar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Home(QMainWindow):        
    def __init__(self):
        super().__init__()

        self.iniciat = False
        
        title_bar = TitleBar()
        title_bar.update_theme_titlebar()

        theme = get_theme_controller()
        theme_color = change_theme(self, theme)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet(f"background-color: {theme_color[1]};")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        self.configuracion = Configuration.get_instance()
        self.configuracion.theme_changed.connect(self.update_theme_home)

        # Crear un layout para los otros widgets
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(75, 10, 75, 125)  # Márgenes para el contenido

        # Agregar otros widgets al nuevo layout
        self.label = QLabel()
        self.label.setPixmap(QPixmap("src/resources/images/lena.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajusta la ruta y el tamaño según sea necesario
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("margin-top: 100px;")
        self.label.setCursor(QCursor(Qt.PointingHandCursor))
        self.label.mousePressEvent = self.on_mouse_press 

        # Añadir widgets al layout principal
        self.main_content_layout.addWidget(self.label)

        # Añadir el layout de contenido principal al layout de la ventana
        self.layout.addLayout(self.main_content_layout)

    def on_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            start_assistant(self)

    def update_theme_home(self):
        theme = get_theme_controller()
        theme_color = change_theme(self, theme)
        self.central_widget.setStyleSheet(f"background-color: {theme_color[1]};")

def start_assistant(self):
    # Crear el hilo con la referencia de la función
    self.thread = threading.Thread(target=process_voice_message_controller, args=(self,), daemon=True)
    
    if self.iniciat:  # Si el asistente ya está en ejecución
        # Detener el hilo (asumiendo que 'stop_process_voice_message_controller' lo detiene)
        stop_process_voice_message_controller(self)
        self.iniciat = False
    else:
        # Iniciar el hilo
        self.thread.start()
        self.iniciat = True

