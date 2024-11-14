import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from db_connection import connect_to_db, close_connection

# Interfaz gráfica de PyQt5
class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Conexión a Base de Datos')
        self.setGeometry(100, 100, 300, 200)

        # Layout
        self.layout = QVBoxLayout()

        # Etiqueta de resultado
        self.label = QLabel('Haz clic en el botón para conectar a la base de datos', self)
        self.layout.addWidget(self.label)

        # Botón
        self.button = QPushButton('Conectar', self)
        self.button.clicked.connect(self.on_button_click)
        self.layout.addWidget(self.button)

        # Configurar el layout de la ventana
        self.setLayout(self.layout)

    def on_button_click(self):
        print("Botón clicado, intentando conectar a la base de datos...")
        # Llamar a la función de conexión a la base de datos
        connection = connect_to_db()
       
        if connection and connection.is_connected():
            print("Conexión exitosa, mostrando mensaje en la etiqueta.")
            self.label.setText('Conexión exitosa a la base de datos')
            close_connection(connection)  # Cerrar la conexión al finalizar
        else:
            print("Error: no se pudo conectar a la base de datos.")
            self.label.setText('Error al conectar a la base de datos')

# Crear la aplicación y mostrar la ventana
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())