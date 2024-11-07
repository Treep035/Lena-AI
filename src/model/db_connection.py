import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='lenaai',
            user='root',
            password='root'
        )

        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection  # Devuelve la conexión para usarla más adelante

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")