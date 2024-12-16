from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from src.controller.titlebar_controller import mousePressEvent, mouseMoveEvent, eventFilter, minimize

class TitleBarDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(35)
        # self.setStyleSheet("background-color: #4CAF50; border-bottom-right-radius: 10px;")

        # Layout de la barra de título
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)  # Establecer márgenes a 0 para que la barra ocupe toda la pantalla
        hbox.setSpacing(0)

        spacer = QWidget()
        spacer.setStyleSheet("background-color: #2C3E50;")  # Color de la barra
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Hace que el espaciador expanda
        hbox.addWidget(spacer)

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet("color: white; border: none; font-size: 16px; padding-bottom: 5px;")
        self.close_button.clicked.connect(self.close)
        self.close_button.installEventFilter(self)  # Instalar filtro de eventos

        # Añadir botones a la barra de título
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
        if source == self.close_button:
            if event.type() == QEvent.Enter:
                source.setStyleSheet("background-color: #34495E; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.Leave:
                source.setStyleSheet("background-color: #2C3E50; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    source.setStyleSheet("background-color: #1F2A38; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    source.setStyleSheet("background-color: #2C3E50; color: white; border: none; font-size: 16px; padding-bottom: 5px;")
                    if source == self.close_button:
                        self.window().close()  # Cerrar la ventana correctamente
        return super().eventFilter(source, event)