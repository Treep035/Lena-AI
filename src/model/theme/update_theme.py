from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request

def update_theme(theme_option):
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
    
    cursor.execute("UPDATE user SET theme_mode = %s WHERE id_user = %s", (theme_option, id_user))

    conn.commit()

    cursor.close()
    conn.close()