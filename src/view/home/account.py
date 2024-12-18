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
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon, QPainter, QPainterPath, QCursor
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal, QSize

import sys
import os
from io import BytesIO
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controller.account_load_controller import account_picture_load_controller, account_username_load_controller
from view.shared.bottombar import BottomBar

class Account(QMainWindow):
    viewChanged = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #233240;")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        self.configure_content_layout = QVBoxLayout()
        self.configure_content_layout.setContentsMargins(15, 50, 75, 0)
        self.configure_content_layout.setSpacing(0)

        self.layout.addLayout(self.configure_content_layout)

        self.configuration_button = QPushButton(self)
        configuration_icon = QPixmap("src/resources/images/configuration/white/configurationblanco.png")  # Asegúrate de usar la ruta correcta a tu imagen
        self.configuration_button.setIcon(QIcon(configuration_icon))

        self.configuration_button.setIconSize(QSize(40, 40))

        self.configuration_button.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                border: none;
                border-radius: 37px;  /* Esto hace que el botón sea circular */
                width: 75px;  /* Tamaño del botón */
                height: 75px;  /* Tamaño del botón */
                margin-bottom: 3px;
                margin-right: 5px;
            }
            QPushButton:hover {
                background-color: #364758;  /* Color al pasar el cursor */
            }
        """)
        self.configuration_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.configuration_button.mousePressEvent = lambda event: self.on_icon_click(event, "configuration")
        self.configure_content_layout.addWidget(self.configuration_button, alignment=Qt.AlignLeft)

        # Crear un layout para los otros widgets
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(75, 10, 75, 215)  # Márgenes para el contenido
        self.main_content_layout.setSpacing(0)  # Añadir más espacio entre widgets

        # Añadir el layout de contenido principal al layout de la ventana
        self.layout.addLayout(self.main_content_layout)
        
        # Añadir imagen de perfil
        self.profile_pic_label = QLabel()
        self.profile_pic_label.setAlignment(Qt.AlignCenter)
        self.profile_pic_label.setFixedSize(150, 150)  # Tamaño fijo para la imagen
        self.main_content_layout.addWidget(self.profile_pic_label, alignment=Qt.AlignCenter)

        user_image_path = account_picture_load_controller()
        pixmap = QPixmap(user_image_path)
        size = 150
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

        # Establecer el pixmap circular en la QLabel
        self.profile_pic_label.setPixmap(circular_pixmap)

        self.username_label = QLabel()
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setStyleSheet("color: white; font-size: 36px;")
        self.main_content_layout.addWidget(self.username_label, alignment=Qt.AlignCenter)

        # Cargar texto desde la base de datos
        username = account_username_load_controller()
        self.username_label.setText(username)

    def on_icon_click(self, event, view_name):
        """Maneja el clic en un ícono, verificando si es clic izquierdo."""
        if event.button() == Qt.LeftButton:  # Solo actuar en clic izquierdo
            self.change_view(view_name)
        
    def change_view(self, view_name):
        """Cambia la vista y emite una señal con el nombre de la vista seleccionada."""
        self.viewChanged.emit(view_name)  # Emitir señal para que `MainWindow` cambie la vista