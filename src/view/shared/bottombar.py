from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QHBoxLayout,
    QSizePolicy,
    QApplication,
    QGraphicsColorizeEffect
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, pyqtSignal

import sys
import os
from resources.styles.theme import change_theme
from controller.theme_controller import get_theme_controller
from view.home.configuration import Configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class BottomBar(QWidget):
    viewChanged = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        theme = get_theme_controller()
        theme_color = change_theme(self, theme)

        self.setFixedHeight(75)

        # Configuración del layout de la barra inferior
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        # Espaciador inicial (con color de fondo) para el margen izquierdo
        self.left_margin_spacer = QWidget()
        self.left_margin_spacer.setFixedWidth(40)  # Ancho del margen izquierdo
        self.left_margin_spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de fondo del espaciador
        hbox.addWidget(self.left_margin_spacer)

        # Imagen 1: Home (izquierda)
        self.home_label = QLabel()
        self.setup_icon(self.home_label, "whitehome", active = True)
        self.home_label.mousePressEvent = lambda event: self.on_icon_click(event, "home")
        hbox.addWidget(self.home_label)

        # Espaciador izquierdo (entre Home y Chat)
        self.left_spacer = QWidget()
        self.left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.left_spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de fondo del espaciador
        hbox.addWidget(self.left_spacer)

        # Imagen 2: Chat (centro)
        self.chat_label = QLabel()
        self.setup_icon(self.chat_label, "whitechat", active = False)
        self.chat_label.mousePressEvent = lambda event: self.on_icon_click(event, "chat")
        hbox.addWidget(self.chat_label)

        # Espaciador derecho (entre Chat y Account)
        self.right_spacer = QWidget()
        self.right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.right_spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de fondo del espaciador
        hbox.addWidget(self.right_spacer)

        # Imagen 3: Account (derecha)
        self.account_label = QLabel()
        self.setup_icon(self.account_label, "whiteaccount", active = False)
        self.account_label.mousePressEvent = lambda event: self.on_icon_click(event, "account")
        hbox.addWidget(self.account_label)

        # Espaciador final (con color de fondo) para el margen derecho
        self.right_margin_spacer = QWidget()
        self.right_margin_spacer.setFixedWidth(40)  # Ancho del margen derecho
        self.right_margin_spacer.setStyleSheet(f"background-color: {theme_color[0]};")  # Color de fondo del espaciador
        hbox.addWidget(self.right_margin_spacer)

        # Estilo de la barra
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {theme_color[0]};
        }}
        QLabel {{
            padding-left: 10px;
        }}
    """)

        self.configuracion = Configuration.get_instance()
        self.configuracion.theme_changed.connect(self.update_theme_bottombar)

    def update_theme_bottombar(self):
        theme = get_theme_controller()
        theme_color = change_theme(self, theme)
        self.left_margin_spacer.setStyleSheet(f"background-color: {theme_color[0]};")
        self.left_spacer.setStyleSheet(f"background-color: {theme_color[0]};")
        self.right_spacer.setStyleSheet(f"background-color: {theme_color[0]};")
        self.right_margin_spacer.setStyleSheet(f"background-color: {theme_color[0]};")
        self.setStyleSheet(f"""
        QWidget {{
            background-color: {theme_color[0]};
        }}
        QLabel {{
            padding-left: 10px;
        }}
    """)

    def setup_icon(self, label, icon_name, active):
        """Configura un QLabel como un icono clickeable, con estado activo/inactivo."""
        image_path = f"src/resources/images/bottombar/{icon_name}{'_inactive' if not active else ''}.png"
        pixmap = QPixmap(image_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setCursor(QCursor(Qt.PointingHandCursor))

    def set_active_icon(self, active_icon):
        """Cambia las imágenes de los íconos según el ícono activo."""
        self.setup_icon(self.home_label, "whitehome", active_icon == "home")
        self.setup_icon(self.chat_label, "whitechat", active_icon == "chat")
        self.setup_icon(self.account_label, "whiteaccount", active_icon == "account")
    
    def on_icon_click(self, event, view_name):
        """Maneja el clic en un ícono, verificando si es clic izquierdo."""
        if event.button() == Qt.LeftButton:  # Solo actuar en clic izquierdo
            self.change_view(view_name)

    def change_view(self, view_name):
        """Cambia la vista y emite una señal con el nombre de la vista seleccionada."""
        self.set_active_icon(view_name)
        self.viewChanged.emit(view_name)  # Emitir señal para que `MainWindow` cambie la vista