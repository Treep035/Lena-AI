import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        print("Intentando conectar a la base de datos...")
        connection = mysql.connector.connect(
            host='localhost',
            database='lenaai',
            user='root',
            password='root'
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
        else:
            print("Error: La conexión no se estableció correctamente.")
        return connection  # Devuelve la conexión para usarla más adelante
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Conexión cerrada.")

def get_user_name(connection, user_id):
    try:
        cursor = connection.cursor()
        query = "SELECT name FROM user WHERE id_user = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()  # Obtener una fila del resultado
        if result:
            return result[0]  # Retornar el nombre si se encuentra
        else:
            return None  # Si no se encuentra el usuario

    except Error as e:
        print(f"Error al obtener el nombre: {e}")
        return None

if __name__ == "__main__":
    connect_to_db()