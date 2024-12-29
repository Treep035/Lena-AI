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
    QSizePolicy,
    QFileDialog,
    QComboBox
)
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon, QCursor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QEvent, QDate, pyqtSignal, QSize, QTimer, QBuffer, QIODevice

from controller.save_configuration_controller import save_configuration_controller
from view.home.change_name import change_name
from view.home.change_password import change_password
from controller.sign_out_controller import sign_out_controller
from controller.theme_controller import update_theme_controller

class Configuration(QMainWindow):
    _instance = None

    @staticmethod
    def get_instance():
        if Configuration._instance is None:
            Configuration._instance = Configuration()
        return Configuration._instance
    
    viewChanged = pyqtSignal(str)
    restart_theme = pyqtSignal()
    account_picture_update_signal = pyqtSignal()
    theme_changed = pyqtSignal()
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

        self.back_content_layout = QVBoxLayout()
        self.back_content_layout.setContentsMargins(15, 20, 85, 0)
        self.back_content_layout.setSpacing(0)

        self.layout.addLayout(self.back_content_layout)

        self.back_button = QPushButton(self)
        back_button = QPixmap("src/resources/images/back/white/whiteback.png")  # Asegúrate de usar la ruta correcta a tu imagen
        self.back_button.setIcon(QIcon(back_button))

        self.back_button.setIconSize(QSize(45, 45))

        self.back_button.setFlat(True)
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.mousePressEvent = lambda event: self.on_icon_click(event, "account")
        self.back_content_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        self.options_content_layout = QVBoxLayout()
        self.options_content_layout.setContentsMargins(15, 5, 15, 130)
        self.options_content_layout.setSpacing(0)

        self.layout.addLayout(self.options_content_layout)

        # Crear un QWidget para contener los layouts
        self.profilePictureButton = QWidget()
        self.profilePictureButton.setMinimumWidth(415)
        self.profilePictureButton.setMaximumHeight(65)

        # Crear el layout principal de self.uno
        main_layout = QHBoxLayout(self.profilePictureButton)

        # Crear QLabel para mostrar la imagen
        change_profile_pic_icon = QPixmap("src/resources/images/profile/white/profile.png")
        change_profile_pic_icon = change_profile_pic_icon.scaled(34, 34, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(change_profile_pic_icon)

        image_label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        # Añadir la imagen al layout principal
        main_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Crear un layout para el texto
        label = QLabel("Cambiar foto de perfil")
        main_layout.setAlignment(Qt.AlignLeft)

        label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        main_layout.addWidget(label)

        # Estilo del QWidget
        self.profilePictureButton.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                border: none;
                border-radius: 27px;
                margin-bottom: 3px;
                color: white;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QWidget:hover {
                background-color: #364758;
            }
        """)

        # Cambiar el cursor a un puntero de mano al pasar sobre el widget
        self.profilePictureButton.setCursor(QCursor(Qt.PointingHandCursor))

        # Añadir el widget al layout principal
        self.options_content_layout.addWidget(self.profilePictureButton, alignment=Qt.AlignCenter)

        # Conectar el clic al método que abrirá el diálogo
        self.profilePictureButton.mousePressEvent = lambda event: self.open_file_dialog(event)
        # self.uno.mousePressEvent(self.open_file_dialog)
        

        self.profileUsernameButton = QWidget()
        self.profileUsernameButton.setMinimumWidth(415)
        self.profileUsernameButton.setMaximumHeight(65)

        # Crear el layout principal de self.uno
        main_layout = QHBoxLayout(self.profileUsernameButton)

        # Crear QLabel para mostrar la imagen
        change_profile_pic_icon = QPixmap("src/resources/images/change_username/white/tblanco.png")
        change_profile_pic_icon = change_profile_pic_icon.scaled(30, 30, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(change_profile_pic_icon)

        image_label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        # Añadir la imagen al layout principal
        main_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Crear un layout para el texto
        label = QLabel("Cambiar nombre de usuario")
        main_layout.setAlignment(Qt.AlignLeft)

        label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        main_layout.addWidget(label)

        # Estilo del QWidget
        self.profileUsernameButton.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                border: none;
                border-radius: 27px;
                margin-bottom: 3px;
                color: white;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QWidget:hover {
                background-color: #364758;
            }
        """)

        # Cambiar el cursor a un puntero de mano al pasar sobre el widget
        self.profileUsernameButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.profileUsernameButton.mousePressEvent = lambda event: change_name(event, self)
        # Añadir el widget al layout principal
        self.options_content_layout.addWidget(self.profileUsernameButton, alignment=Qt.AlignCenter)


        self.profilePasswordButton = QWidget()
        self.profilePasswordButton.setMinimumWidth(415)
        self.profilePasswordButton.setMaximumHeight(65)

        # Crear el layout principal de self.uno
        main_layout = QHBoxLayout(self.profilePasswordButton)

        # Crear QLabel para mostrar la imagen
        change_profile_pic_icon = QPixmap("src/resources/images/password/in_configuration/white/ocultarcontraseñablanco.png")
        change_profile_pic_icon = change_profile_pic_icon.scaled(30, 30, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(change_profile_pic_icon)

        image_label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        # Añadir la imagen al layout principal
        main_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Crear un layout para el texto
        label = QLabel("Cambiar contraseña")
        main_layout.setAlignment(Qt.AlignLeft)

        label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        main_layout.addWidget(label)

        # Estilo del QWidget
        self.profilePasswordButton.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                border: none;
                border-radius: 27px;
                margin-bottom: 3px;
                color: white;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QWidget:hover {
                background-color: #364758;
            }
        """)

        # Cambiar el cursor a un puntero de mano al pasar sobre el widget
        self.profilePasswordButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.profilePasswordButton.mousePressEvent = lambda event: change_password(event, self)

        # Añadir el widget al layout principal
        self.options_content_layout.addWidget(self.profilePasswordButton, alignment=Qt.AlignCenter)

        self.profileLanguageButton = QWidget()
        self.profileLanguageButton.setMinimumWidth(415)
        self.profileLanguageButton.setMaximumHeight(65)

        # Crear el layout principal de self.uno
        main_layout = QHBoxLayout(self.profileLanguageButton)

        # Crear QLabel para mostrar la imagen
        change_profile_pic_icon = QPixmap("src/resources/images/language/white/idiomablanco.png")
        change_profile_pic_icon = change_profile_pic_icon.scaled(35, 35, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(change_profile_pic_icon)

        image_label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        # Añadir la imagen al layout principal
        main_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Crear un layout para el texto
        label = QLabel("Idioma")
        main_layout.setAlignment(Qt.AlignLeft)

        label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        main_layout.addWidget(label)

        # Estilo del QWidget
        self.profileLanguageButton.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                border: none;
                border-radius: 27px;
                margin-bottom: 3px;
                color: white;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QWidget:hover {
                background-color: #364758;
            }
        """)

        # Cambiar el cursor a un puntero de mano al pasar sobre el widget
        self.profileLanguageButton.setCursor(QCursor(Qt.PointingHandCursor))

        # Añadir el widget al layout principal
        self.options_content_layout.addWidget(self.profileLanguageButton, alignment=Qt.AlignCenter)

        self.profileThemeButton = QWidget()
        self.profileThemeButton.setMinimumWidth(415)
        self.profileThemeButton.setMaximumHeight(65)

        # Crear el layout principal de self.uno
        main_layout_final = QHBoxLayout(self.profileThemeButton)
        main_layout = QHBoxLayout()

        # Crear QLabel para mostrar la imagen
        change_profile_pic_icon = QPixmap("src/resources/images/theme/white/temablanco.png")
        change_profile_pic_icon = change_profile_pic_icon.scaled(35, 35, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(change_profile_pic_icon)

        image_label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
        """)

        # Añadir la imagen al layout principal
        main_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Crear un layout para el texto
        label = QLabel("Temas")
        main_layout.setAlignment(Qt.AlignLeft)

        label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
        """)

        main_layout.addWidget(label)

        main_layout_2 = QHBoxLayout()

        combobox_theme = QComboBox()
        combobox_theme.addItems(["Default", "Light", "Dark", "Pink", "Special"])  # Agregar elementos
        main_layout_2.setAlignment(Qt.AlignRight)
        combobox_theme.setStyleSheet("""
            QComboBox {
                color: white;  /* Cambiar color del texto */
                background-color: #2C3E50;  /* Evitar que tenga fondo */
                border-radius: 5px;  /* Bordes redondeados */
                padding: 5px;  /* Espaciado interno */
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.1);  /* El fondo sigue siendo transparente */
            }
            QComboBox::drop-down {
            }
            QComboBox::down-arrow {
            }
            QComboBox QAbstractItemView {
                background-color: #34495E;  /* Color de fondo del menú desplegable */
                color: white;  /* Color del texto en el menú */
                selection-background-color: #2C3E50;
                selection-color: white;  /* Color del texto del elemento seleccionado */
                border-radius: 5px;  /* Bordes redondeados */
                outline: none;  /* Evitar el contorno */
                padding: 5px;
                spacing: 10px;  /* Espaciado entre las opciones */
            }
            QComboBox QAbstractItemView::item {
                padding-left: 15px;  /* Espaciado interno izquierdo */
                padding-right: 15px;  /* Espaciado interno derecho */
                padding-top: 10px;  /* Espaciado interno superior */
                padding-bottom: 10px;  /* Espaciado interno inferior */
            }
        """)
        combobox_theme.setCursor(QCursor(Qt.PointingHandCursor))

        self.themes = {
            0: "default",   # Opción 1
            1: "light",    # Opción 2
            2: "dark",  # Opción 3
            3: "pink",
            4: "special"
        }

        combobox_theme.currentIndexChanged.connect(self.selection_changed)

        main_layout_2.addWidget(combobox_theme)

        # Estilo del QWidget
        self.profileThemeButton.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                border: none;
                border-radius: 27px;
                margin-bottom: 3px;
                color: white;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
        """)
        # Cambiar el cursor a un puntero de mano al pasar sobre el widget
        main_layout_final.addLayout(main_layout)
        main_layout_final.addLayout(main_layout_2)

        # Añadir el widget al layout principal
        self.options_content_layout.addWidget(self.profileThemeButton, alignment=Qt.AlignCenter)

        self.profileSignOutButton = QWidget()
        self.profileSignOutButton.setMinimumWidth(415)
        self.profileSignOutButton.setMaximumHeight(65)

        # Crear el layout principal de self.uno
        main_layout = QHBoxLayout(self.profileSignOutButton)

        # Crear QLabel para mostrar la imagen
        change_profile_pic_icon = QPixmap("src/resources/images/signout/red/redsignout.png")
        change_profile_pic_icon = change_profile_pic_icon.scaled(35, 35, Qt.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(change_profile_pic_icon)

        image_label.setStyleSheet("""
            QLabel {
                color: white;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        # Añadir la imagen al layout principal
        main_layout.addWidget(image_label, alignment=Qt.AlignLeft)

        # Crear un layout para el texto
        label = QLabel("Sign out")
        main_layout.setAlignment(Qt.AlignLeft)

        label.setStyleSheet("""
            QLabel {
                color: red;  /* Cambiar color del texto */
                background-color: transparent;  /* Evitar que tenga fondo */
                padding-left: 10px;  /* Alinear texto con la imagen */
            }
            QLabel:hover {
                background-color: transparent;  /* El fondo sigue siendo transparente */
            }
        """)

        main_layout.addWidget(label)

        # Estilo del QWidget
        self.profileSignOutButton.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                border: none;
                border-radius: 27px;
                margin-bottom: 3px;
                color: white;
                font-size: 18px;
                text-align: left;
                padding-left: 15px;
            }
            QWidget:hover {
                background-color: #364758;
            }
        """)

        # Cambiar el cursor a un puntero de mano al pasar sobre el widget
        self.profileSignOutButton.setCursor(QCursor(Qt.PointingHandCursor))

        # Luego, asigna este método al evento
        self.profileSignOutButton.mousePressEvent = lambda event: self.on_sign_out(event, "logout")
        
        # Añadir el widget al layout principal
        self.options_content_layout.addWidget(self.profileSignOutButton, alignment=Qt.AlignCenter)

    def on_sign_out(self, event, view_name):
        if event.button() == Qt.LeftButton:  # Solo actuar en clic izquierdo
            sign_out_controller()
            self.restart_theme.emit()
            self.change_view(view_name)

    def on_icon_click(self, event, view_name):
        """Maneja el clic en un ícono, verificando si es clic izquierdo."""
        if event.button() == Qt.LeftButton:  # Solo actuar en clic izquierdo
            self.change_view(view_name)
        
    def change_view(self, view_name):
        """Cambia la vista y emite una señal con el nombre de la vista seleccionada."""
        self.viewChanged.emit(view_name)  # Emitir señal para que `MainWindow` cambie la vista

    def open_file_dialog(self, event):
        # Abrir el explorador de archivos
        file_path, _ = QFileDialog.getOpenFileName(
            self,  # Ventana principal
            "Seleccionar imagen",  # Título del cuadro de diálogo
            "",  # Directorio inicial
            "Imágenes (*.png *.jpg *.jpeg)"  # Filtro para imágenes
        )
        if file_path:  # Si se seleccionó un archivo
            print(f"Imagen seleccionada: {file_path}")
            save_configuration_controller(file_path)
            print("Emitiendo señal account_picture_update_signal")
            self.account_picture_update_signal.emit()

    def selection_changed(self, index):
        theme_option = self.themes.get(index, "Desconocido")
        update_theme_controller(theme_option)
        self.theme_changed.emit()