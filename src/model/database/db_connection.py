import pymysql
from pymysql import MySQLError

def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            database='lenaai',
            user='root',
            password='root'
        )
        print("Conexión exitosa a la base de datos")
        return connection  # Devuelve la conexión para usarla más adelante
    except MySQLError as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def close_connection(connection):
    if connection and connection.open:
        connection.close()
        print("Conexión cerrada")

def get_user_name(connection, user_id):
    try:
        with connection.cursor() as cursor:
            query = "SELECT name FROM user WHERE id_user = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()  # Obtener una fila del resultado
            if result:
                return result[0]  # Retornar el nombre si se encuentra
            else:
                return None  # Si no se encuentra el usuario
    except MySQLError as e:
        print(f"Error al obtener el nombre: {e}")
        return None

if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        user_name = get_user_name(connection, 1)  # Prueba con el id de usuario 1
        if user_name:
            print(f"Nombre del usuario: {user_name}")
        else:
            print("Usuario no encontrado")
        close_connection(connection)
