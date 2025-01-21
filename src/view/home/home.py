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
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal, QTimer
import threading
import sys
import os
from resources.styles.theme import change_theme
from controller.theme_controller import get_theme_controller
from controller.process_voice_message_controller import process_voice_message_controller, stop_process_voice_message_controller
from controller.stop_animation_controller import StopAnimationSignal
from view.home.configuration import Configuration
from view.shared.titlebar import TitleBar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Home(QMainWindow):        
    def __init__(self):
        super().__init__()

        self.started= False
        self.already_started= False
        self.image_timer = QTimer(self)  # Timer para el efecto
        self.image_timer.timeout.connect(self.animate_image)  # Conectar el temporizador al método
        self.image_scale_factor = 1.0  # Factor de escala inicial
        self.image_growing = True
        
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
        self.original_pixmap = QPixmap("src/resources/images/lena.png").scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(self.original_pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("margin-top: 100px;")
        self.label.setCursor(QCursor(Qt.PointingHandCursor))
        self.label.mousePressEvent = self.on_mouse_press 
        self.stop_animation_signal_instance = StopAnimationSignal.get_instance()
        self.stop_animation_signal_instance.stop_animation_signal.connect(self.stop_animation)

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

    def animate_image(self):
        if self.image_growing:
            self.image_scale_factor += 0.005  # Incremento intermedio para ajustar la velocidad
            if self.image_scale_factor >= 1.1:  # Límite superior
                self.image_growing = False
        else:
            self.image_scale_factor -= 0.005  # Decremento intermedio para ajustar la velocidad
            if self.image_scale_factor <= 1.0:  # Límite inferior
                self.image_growing = True

        # Redimensionar la imagen
        scaled_pixmap = self.original_pixmap.scaled(
            int(200 * self.image_scale_factor),
            int(200 * self.image_scale_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.label.setPixmap(scaled_pixmap)

    def stop_animation(self):
        self.image_timer.stop()
        self.label.setPixmap(self.original_pixmap)

def start_assistant(self):
    
    self.thread = threading.Thread(target=process_voice_message_controller, args=(self,), daemon=True)
    
    if self.started:  # Si el asistente ya está en ejecución
        # Detener el hilo (asumiendo que 'stop_process_voice_message_controller' lo detiene)
        stop_process_voice_message_controller(self)
    else:
        # Iniciar el hilo
        self.thread.start()
        self.started = True
        self.image_timer.start(16)

    self.already_started = True
    print(f"Cantidad de hilos activos: {len(threading.enumerate())}")
    print("Hilos activos:", [thread.name for thread in threading.enumerate()])