from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# from src.controller.titlebar_controller import mousePressEvent, mouseMoveEvent, eventFilter, minimize

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(35)
        # self.setStyleSheet("background-color: #4CAF50; border-bottom-right-radius: 10px;")

        # Layout de la barra de título
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)  # Establecer márgenes a 0 para que la barra ocupe toda la pantalla
        hbox.setSpacing(0)

        # Imagen (lena.png)
        self.image_label = QLabel()
        pixmap = QPixmap("src/resources/images/lenaicon.ico").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Cargar y escalar la imagen
        self.image_label.setPixmap(pixmap)

        # Etiqueta de título
        self.title_label = QLabel("Lena AI")
        self.title_label.setStyleSheet("color: white; font-size: 16px;")

        hbox.addWidget(self.image_label)
        hbox.addWidget(self.title_label)

        spacer = QWidget()
        spacer.setStyleSheet("background-color: #2C3E50;")  # Color de la barra
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Hace que el espaciador expanda
        hbox.addWidget(spacer)

        # Botones de la barra de título
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setStyleSheet("color: white; border: none; font-size: 16px; padding-bottom: 5px;")
        self.minimize_button.clicked.connect(self.minimize)
        self.minimize_button.installEventFilter(self)  # Instalar filtro de eventos

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet("color: white; border: none; font-size: 16px; padding-bottom: 5px;")
        self.close_button.clicked.connect(self.close)
        self.close_button.installEventFilter(self)  # Instalar filtro de eventos

        # Añadir botones a la barra de título
        hbox.addWidget(self.minimize_button)
        hbox.addWidget(self.close_button)

        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
            }
            QLabel {
                padding-left: 10px;
            }
        """)

        self.start = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos() - self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.start is not None:
            self.window().move(event.globalPos() - self.start)
            event.accept()


    def eventFilter(self, source, event):
        if source in (self.minimize_button, self.close_button):
            if event.type() == QEvent.Enter:
                source.setStyleSheet("background-color: #34495E; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.Leave:
                source.setStyleSheet("background-color: #2C3E50; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.MouseButtonPress:
                source.setStyleSheet("background-color: #1F2A38; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.MouseButtonRelease:
                source.setStyleSheet("background-color: #2C3E50; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
                if source == self.minimize_button:
                    self.minimize()  # Minimizar la ventana si se libera el botón de minimizar
                elif source == self.close_button:
                    self.window().close()  # Cerrar la ventana correctamente
        return super().eventFilter(source, event)

    def minimize(self):
        self.window().showMinimized()