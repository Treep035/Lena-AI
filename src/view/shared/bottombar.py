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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class BottomBar(QWidget):
    viewChanged = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setFixedHeight(75)

        # Configuración del layout de la barra inferior
        hbox = QHBoxLayout(self)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        # Espaciador inicial (con color de fondo) para el margen izquierdo
        left_margin_spacer = QWidget()
        left_margin_spacer.setFixedWidth(40)  # Ancho del margen izquierdo
        left_margin_spacer.setStyleSheet("background-color: #2C3E50;")  # Color de fondo del espaciador
        hbox.addWidget(left_margin_spacer)

        # Imagen 1: Home (izquierda)
        self.home_label = QLabel()
        self.setup_icon(self.home_label, "whitehome", active = True)
        self.home_label.mousePressEvent = lambda event: self.change_view("home")
        hbox.addWidget(self.home_label)

        # Espaciador izquierdo (entre Home y Chat)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        left_spacer.setStyleSheet("background-color: #2C3E50;")  # Color de fondo del espaciador
        hbox.addWidget(left_spacer)

        # Imagen 2: Chat (centro)
        self.chat_label = QLabel()
        self.setup_icon(self.chat_label, "whitechat", active = False)
        self.chat_label.mousePressEvent = lambda event: self.change_view("chat")
        hbox.addWidget(self.chat_label)

        # Espaciador derecho (entre Chat y Account)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_spacer.setStyleSheet("background-color: #2C3E50;")  # Color de fondo del espaciador
        hbox.addWidget(right_spacer)

        # Imagen 3: Account (derecha)
        self.account_label = QLabel()
        self.setup_icon(self.account_label, "whiteaccount", active = False)
        self.account_label.mousePressEvent = lambda event: self.change_view("account")
        hbox.addWidget(self.account_label)

        # Espaciador final (con color de fondo) para el margen derecho
        right_margin_spacer = QWidget()
        right_margin_spacer.setFixedWidth(40)  # Ancho del margen derecho
        right_margin_spacer.setStyleSheet("background-color: #2C3E50;")  # Color de fondo del espaciador
        hbox.addWidget(right_margin_spacer)

        # Estilo de la barra
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
            }
            QLabel {
                padding-left: 10px;
            }
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

    def change_view(self, view_name):
        """Cambia la vista y emite una señal con el nombre de la vista seleccionada."""
        self.set_active_icon(view_name)
        self.viewChanged.emit(view_name)  # Emitir señal para que `MainWindow` cambie la vista