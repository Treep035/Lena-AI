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
from controller.theme_controller import get_theme_controller
from resources.styles.theme import change_theme
from view.home.configuration import Configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# from src.controller.titlebar_controller import mousePressEvent, mouseMoveEvent, eventFilter, minimize

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()

        self.theme = get_theme_controller()
        theme_color = change_theme(self, self.theme)

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
        self.title_label.setStyleSheet(f"color: {theme_color[4]}; font-size: 16px;")

        hbox.addWidget(self.image_label)
        hbox.addWidget(self.title_label)

        self.spacer = QWidget()
        self.spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de la barra
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Hace que el espaciador expanda
        hbox.addWidget(self.spacer)

        # Botones de la barra de título
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setStyleSheet(f"color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
        self.minimize_button.clicked.connect(self.minimize)
        self.minimize_button.installEventFilter(self)  # Instalar filtro de eventos

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet(f"color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
        self.close_button.clicked.connect(self.close)
        self.close_button.installEventFilter(self)  # Instalar filtro de eventos

        # Añadir botones a la barra de título
        hbox.addWidget(self.minimize_button)
        hbox.addWidget(self.close_button)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_color[0]};
            }}
            QLabel {{
                padding-left: 10px;
            }}
        """)

        self.start = None

        self.configuracion = Configuration.get_instance()
        self.configuracion.theme_changed.connect(self.update_theme_titlebar)
        self.configuracion.restart_theme.connect(self.restart_theme_titlebar)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos() - self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.start is not None:
            self.window().move(event.globalPos() - self.start)
            event.accept()


    def eventFilter(self, source, event):
        theme_color = change_theme(self, self.theme)
        if source in (self.minimize_button, self.close_button):
            if event.type() == QEvent.Enter:
                source.setStyleSheet(f"background-color: {theme_color[2]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.Leave:
                source.setStyleSheet(f"background-color: {theme_color[0]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    source.setStyleSheet(f"background-color: {theme_color[3]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    source.setStyleSheet(f"background-color: {theme_color[0]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                    if source == self.minimize_button:
                        self.minimize()  # Minimizar la ventana si se libera el botón de minimizar
                    elif source == self.close_button:
                        self.window().close()  # Cerrar la ventana correctamente
        return super().eventFilter(source, event)

    def minimize(self):
        self.window().showMinimized()
    
    def update_theme_titlebar(self):
        theme = get_theme_controller()
        theme_color = change_theme(self, theme)
        
        self.title_label.setStyleSheet(f"color: {theme_color[4]}; font-size: 16px;")
        self.spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de la barra
        self.minimize_button.setStyleSheet(f"color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
        self.close_button.setStyleSheet(f"color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_color[0]};
            }}
            QLabel {{
                padding-left: 10px;
            }}
        """)
        def update_button_styles(source, event):
            if source in (self.minimize_button, self.close_button):
                if event.type() == QEvent.Enter:
                    source.setStyleSheet(f"background-color: {theme_color[2]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                elif event.type() == QEvent.Leave:
                    source.setStyleSheet(f"background-color: {theme_color[0]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                elif event.type() == QEvent.MouseButtonPress:
                    if event.button() == Qt.LeftButton:
                        source.setStyleSheet(f"background-color: {theme_color[3]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                elif event.type() == QEvent.MouseButtonRelease:
                    if event.button() == Qt.LeftButton:
                        source.setStyleSheet(f"background-color: {theme_color[0]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                        if source == self.minimize_button:
                            self.minimize()  # Minimizar la ventana si se libera el botón de minimizar
                        elif source == self.close_button:
                            self.window().close()  # Cerrar la ventana correctamente
        
        # Redefine el método `eventFilter` para usar los nuevos estilos
        def eventFilter(self, source, event):
            update_button_styles(source, event)
            return super().eventFilter(source, event)
        
        # Vuelve a asignar el método a la clase
        self.eventFilter = eventFilter.__get__(self, TitleBar)
        
    def restart_theme_titlebar(self):
        theme = "default"
        theme_color = change_theme(self, theme)

        self.title_label.setStyleSheet(f"color: {theme_color[4]}; font-size: 16px;")
        self.spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de la barra
        self.minimize_button.setStyleSheet(f"color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
        self.close_button.setStyleSheet(f"color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_color[0]};
            }}
            QLabel {{
                padding-left: 10px;
            }}
        """)

        def update_button_styles(source, event):
            if source in (self.minimize_button, self.close_button):
                if event.type() == QEvent.Enter:
                    source.setStyleSheet(f"background-color: {theme_color[2]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                elif event.type() == QEvent.Leave:
                    source.setStyleSheet(f"background-color: {theme_color[0]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                elif event.type() == QEvent.MouseButtonPress:
                    if event.button() == Qt.LeftButton:
                        source.setStyleSheet(f"background-color: {theme_color[3]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                elif event.type() == QEvent.MouseButtonRelease:
                    if event.button() == Qt.LeftButton:
                        source.setStyleSheet(f"background-color: {theme_color[0]}; color: {theme_color[4]}; border: none; font-size: 16px; padding-bottom: 5px;")
                        if source == self.minimize_button:
                            self.minimize()  # Minimizar la ventana si se libera el botón de minimizar
                        elif source == self.close_button:
                            self.window().close()  # Cerrar la ventana correctamente
    
        def eventFilter(self, source, event):
                update_button_styles(source, event)
                return super().eventFilter(source, event)
            
            # Vuelve a asignar el método a la clase
        self.eventFilter = eventFilter.__get__(self, TitleBar)