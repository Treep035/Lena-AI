import pymysql
from pymysql import MySQLError
import os

from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request

def sign_out():
    connection = connect_to_db()
    auth_token = get_auth_token_from_request()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM auth_token WHERE auth_token = %s"
            cursor.execute(query, (auth_token,))
            connection.commit()
    except MySQLError as e:
        print(f"Error al actualizar el token: {e}")
        return None
    session_file_path = os.path.expanduser("config/session.json")  # Cambia esta ruta según tu caso
    
    try:
        # Verificar si el archivo existe
        if os.path.exists(session_file_path):
            os.remove(session_file_path)
            print(f"Archivo {session_file_path} eliminado exitosamente.")
        else:
            print(f"El archivo {session_file_path} no existe.")
    except Exception as e:
        print(f"Ocurrió un error al intentar eliminar el archivo: {e}")
