import sys
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
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon
from PyQt5.QtCore import Qt, QEvent, QDate

# from src.main import open_login

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
        pixmap = QPixmap("./lenaicon.ico").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Cargar y escalar la imagen
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lena AI")
        self.setGeometry(100, 100, 450, 725)
        self.setFixedSize(450, 725)
        self.setWindowIcon(QIcon('../resources/images/lenaicon.ico'))


        # Eliminar la barra de título predeterminada
        self.setWindowFlags(Qt.FramelessWindowHint)

        
        print("Register")

        # Crear y establecer la barra de título personalizada
        self.title_bar = TitleBar()
        print("TitleBar")

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Configurar el widget central
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #233240;")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.layout)

        self.layout.addWidget(self.title_bar)  # Añadir la barra de título

        # Crear un layout para los otros widgets
        self.main_content_layout = QVBoxLayout()
        self.main_content_layout.setContentsMargins(75, 10, 75, 125)  # Márgenes para el contenido

        # Agregar otros widgets al nuevo layout
        self.label = QLabel()
        self.label.setPixmap(QPixmap("./lena.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ajusta la ruta y el tamaño según sea necesario
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("margin-top: 30px;")

        self.welcome_label = QLabel("Create an account")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color: white; font-size: 35px; margin-bottom:10px;")  # Ajusta el estilo según tu preferencia

        self.text_username = QLineEdit()
        self.text_username.setPlaceholderText("Username...")
        self.text_username.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px;")
        self.text_username.setFixedSize(300, 50)

        self.text_email = QLineEdit()
        self.text_email.setPlaceholderText("Email...")
        self.text_email.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px;")
        self.text_email.setFixedSize(300, 50)

        self.text_password = QLineEdit()
        self.text_password.setPlaceholderText("Password...")
        self.text_password.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 1px;")
        self.text_password.setEchoMode(QLineEdit.Password)
        self.text_password.setFixedSize(300, 50)

        self.date_birthdate = QDateEdit()
        self.date_birthdate.setStyleSheet("color: white; border-radius: 10px; border: 1px solid #ccc; padding: 3px;")
        self.date_birthdate.setFixedSize(300, 40)
        self.date_birthdate.setCalendarPopup(True)
        self.date_birthdate.setDate(QDate.currentDate())

        self.button = QPushButton("Register")
        self.button.setStyleSheet(""" 
            background-color: #2C3E50; 
            color: white; 
            padding: 10px; 
            border: 1px solid #ccc;
            border-radius: 10px; 
            font-size: 16px;
        """)
        self.button.setCursor(Qt.PointingHandCursor)  # Cambiar el cursor a puntero
        self.button.clicked.connect(self.validate_fields)

        self.already_account_label = QLabel("<a href='#'>Do you already have an account?</a>")
        self.already_account_label.setStyleSheet("color: #1ABC9C; font-size: 12px;")
        self.already_account_label.setAlignment(Qt.AlignCenter)
        self.already_account_label.setFixedSize(185, 20)
        self.already_account_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.already_account_label.linkActivated.connect(self.open_login_window)  # Conectar el enlace a la función
        
        # Añadir widgets al layout principal
        self.main_content_layout.addWidget(self.label)
        self.main_content_layout.addWidget(self.welcome_label)
        self.main_content_layout.addWidget(self.text_username)
        self.main_content_layout.addWidget(self.text_email)
        self.main_content_layout.addWidget(self.text_password)
        self.main_content_layout.addWidget(self.date_birthdate)
        self.main_content_layout.addWidget(self.button)
        self.main_content_layout.addWidget(self.already_account_label)

        # Añadir el layout de contenido principal al layout de la ventana
        self.layout.addLayout(self.main_content_layout)

    def validate_fields(self):
        username = self.text_username.text().strip()
        email = self.text_email.text().strip()
        password = self.text_password.text().strip()
        birthdate = self.date_birthdate.date()

        # Verifica que los campos no estén vacíos
        if not username or not email or not password:
            QMessageBox.warning(self, "Lena AI", "Please fill in all fields.")
            return

        # Si todo es válido
        QMessageBox.information(self, "Success", "All fields are valid!")

    # def open_login_window(self):
    #     open_login()
    #     self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
