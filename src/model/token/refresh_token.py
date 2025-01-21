from model.database.db_connection import connect_to_db
import os
import secrets
import json
from datetime import datetime, timedelta

def check_refresh_token():
    refresh_token = get_refresh_token_from_request()

    if refresh_token:
        user = verify_refresh_token_in_db(refresh_token)
        if user:
            auth_token, auth_token_expiration  = generate_new_auth_token()
            update_new_auth_token(auth_token, refresh_token, auth_token_expiration)
            logged_in = True
            return logged_in
        else:
            logged_in = False
            return logged_in
    else:
        logged_in = False
        return logged_in

def get_refresh_token_from_request():
    try:
        root_dir = os.getcwd()
        file_path = os.path.join(root_dir, 'config', 'session.json')

        # Abre y carga el archivo session.json
        with open(file_path, 'r') as f:
            session_data = json.load(f)
        
        # Verifica si 'refresh_token' está presente en los datos cargados
        if 'refresh_token' in session_data:
            return session_data['refresh_token']
        else:
            return None  # Devuelve None si no se encuentra el refresh_token
    except FileNotFoundError:
        # Si el archivo no existe, maneja el error adecuadamente
        print("El archivo session.json no fue encontrado.")
        return None
    except json.JSONDecodeError:
        # Si el archivo JSON no está bien formado, maneja el error
        print("Error al leer el archivo session.json.")
        return None

def verify_refresh_token_in_db(refresh_token):
    # Aquí conectas a la base de datos y verificas si el token existe y es válido
    connection = connect_to_db()  # Asume que tienes una función para conectar a la DB
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM auth_token WHERE refresh_token = %s", (refresh_token,))
    user = cursor.fetchone()
    return user

def generate_new_auth_token():
    # Generar auth_token y refresh_token de forma segura
    auth_token = secrets.token_urlsafe(32)  # Token de 32 caracteres al azar
    
    # Calcular las fechas de expiración
    auth_token_expiration = datetime.now() + timedelta(hours=1)  # Expira en 1 hora

    return auth_token, auth_token_expiration

def save_new_auth_token_to_session(auth_token):
    """Actualiza únicamente el auth_token en el archivo session.json."""

    try:
        root_dir = os.getcwd()
        print(f"Directorio actual: {root_dir}")
        file_path = os.path.join(root_dir, 'config', 'session.json')
        print(f"Actualizando auth_token en: {file_path}")

        if os.path.exists(file_path):
            # Carga los datos actuales del archivo
            with open(file_path, 'r') as json_file:
                session_data = json.load(json_file)

        # Actualiza únicamente el auth_token
        session_data['auth_token'] = auth_token

        with open(file_path, 'w') as json_file:
            json.dump(session_data, json_file, indent=4)
        print("auth_token actualizado correctamente en session.json.")
    except Exception as err:
        print(f"Error al guardar los tokens en session.json: {err}")

def update_new_auth_token(auth_token, refresh_token, auth_token_expiration):
    try:
        save_new_auth_token_to_session(auth_token)

        # Conectar a la base de datos
        connection = connect_to_db()
        cursor = connection.cursor()

        # Crear la consulta de inserción
        query = """
            UPDATE auth_token
            SET auth_token = %s, auth_token_expiration = %s
            WHERE refresh_token = %s;
        """
        values = (auth_token, auth_token_expiration, refresh_token)
        
        # Ejecutar la consulta
        cursor.execute(query, values)
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        print("Tokens insertados correctamente.")
    except Exception as err:
        print(f"Error: {err}")