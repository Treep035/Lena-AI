import json
import os
import secrets
import bcrypt
from datetime import datetime, timedelta

from model.database.db_connection import connect_to_db

def check_auth_token():
    # Recupera el auth_token (puede ser de los encabezados o de las cookies)
    auth_token = get_auth_token_from_request()  # Implementa este método según cómo manejes los tokens

    if auth_token:
        # Verifica si el auth_token existe en la base de datos
        user = verify_token_in_db(auth_token)  # Método para verificar el token en la base de datos
        if user:
            # Si el token es válido, mostrar la vista principal
            logged_in = True
            return logged_in
        else:
            # Si el token no es válido, mostrar el formulario de login
            logged_in = False
            return logged_in
    else:
        # Si no existe el token, mostrar el formulario de login
        logged_in = False
        return logged_in

def get_auth_token_from_request():
    try:
        root_dir = os.getcwd()
        file_path = os.path.join(root_dir, 'config', 'session.json')

        # Abre y carga el archivo session.json
        with open(file_path, 'r') as f:
            session_data = json.load(f)
        
        # Verifica si 'auth_token' está presente en los datos cargados
        if 'auth_token' in session_data:
            return session_data['auth_token']
        else:
            return None  # Devuelve None si no se encuentra el auth_token
    except FileNotFoundError:
        # Si el archivo no existe, maneja el error adecuadamente
        print("El archivo session.json no fue encontrado.")
        return None
    except json.JSONDecodeError:
        # Si el archivo JSON no está bien formado, maneja el error
        print("Error al leer el archivo session.json.")
        return None

def verify_token_in_db(auth_token):
    # Aquí conectas a la base de datos y verificas si el token existe y es válido
    connection = connect_to_db()  # Asume que tienes una función para conectar a la DB
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM auth_token WHERE auth_token = %s", (auth_token,))
    user = cursor.fetchone()
    return user  # Si el token existe, retornará el usuario, de lo contrario None

def generate_tokens():
    # Generar auth_token y refresh_token de forma segura
    auth_token = secrets.token_urlsafe(32)  # Token de 32 caracteres al azar
    refresh_token = secrets.token_urlsafe(64)  # Token de 64 caracteres al azar
    
    # Calcular las fechas de expiración
    auth_token_expiration = datetime.now() + timedelta(hours=1)  # Expira en 1 hora
    refresh_token_expiration = datetime.now() + timedelta(days=90)  # Expira en 3 meses

    return auth_token, refresh_token, auth_token_expiration, refresh_token_expiration

def save_tokens_to_session(auth_token, refresh_token):
    """Guarda los tokens en el archivo session.json"""
    session_data = {
        'auth_token': auth_token,
        'refresh_token': refresh_token,
    }

    try:
        root_dir = os.getcwd()
        print(f"Directorio actual: {root_dir}")
        file_path = os.path.join(root_dir, 'config', 'session.json')
        print(f"Guardando tokens en: {file_path}")

        with open(file_path, 'w') as json_file:
            json.dump(session_data, json_file, indent=4)
        print("Tokens guardados en session.json correctamente.")
    except Exception as err:
        print(f"Error al guardar los tokens en session.json: {err}")

def insert_tokens(id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration):
    try:
        save_tokens_to_session(auth_token, refresh_token)

        # Conectar a la base de datos
        connection = connect_to_db()
        cursor = connection.cursor()

        # Crear la consulta de inserción
        query = """
            INSERT INTO auth_token (id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (id_user, auth_token, refresh_token, auth_token_expiration, refresh_token_expiration)
        
        # Ejecutar la consulta
        cursor.execute(query, values)
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        print("Tokens insertados correctamente.")
    except Exception as err:
        print(f"Error: {err}")
    