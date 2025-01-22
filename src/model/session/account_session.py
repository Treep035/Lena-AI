from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request
from datetime import datetime

def account_session(self):
    try:
        conn = connect_to_db()  # Cambiar por la ruta real de la base de datos
        cursor = conn.cursor()

        auth_token = get_auth_token_from_request()
        if auth_token is None:
            cursor.close()
            conn.close()
            return

        cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
        id_user = cursor.fetchone()

        if id_user is None:
            print("Token inválido: No se encontró el usuario asociado.")
            cursor.close()
            conn.close()
            return

        session_started_at = datetime.now()
        cursor.execute("INSERT INTO session (id_user, session_started_at) VALUES (%s, %s)", (id_user, session_started_at))

        conn.commit()
    except Exception as e:
        print(f"Error durante la operación: {e}")
    finally:
        # Cerrar el cursor y la conexión incluso si ocurre un error
        if cursor:
            cursor.close()
        if conn:
            conn.close()