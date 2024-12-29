from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request

def get_theme():
    theme = "default"
    conn = connect_to_db()  # Cambiar por la ruta real de la base de datos
    cursor = conn.cursor()

    auth_token = get_auth_token_from_request()
    if auth_token is None:
        cursor.close()
        conn.close()
        return theme

    cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
    id_user = cursor.fetchone()

    if id_user is None:
            cursor.close()
            conn.close()
            return theme
    
    cursor.execute("SELECT theme_mode FROM user WHERE id_user = %s", (id_user,))
    theme_row = cursor.fetchone()

    if theme_row is not None:
        theme = theme_row[0]

    cursor.close()
    conn.close()
    return theme