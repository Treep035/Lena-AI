from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request
from datetime import datetime

def save_message(message):
    try:
        connection = connect_to_db()
        if connection is None:
            print("No se pudo conectar a la base de datos.")
            return

        cursor = connection.cursor()

        auth_token = get_auth_token_from_request()

        cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
        id_user = cursor.fetchone()

        cursor.execute(f"SELECT username FROM user WHERE id_user = %s", (id_user,))
        sender = cursor.fetchone()

        message_sent_at = datetime.now()

        # Consulta SQL para actualizar la imagen (ajusta el WHERE según corresponda)
        query = "INSERT INTO message (id_user, message, sender, message_sent_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_user, message, sender, message_sent_at))

        # Confirmar los cambios
        connection.commit()
        print("Mensaje guardado exitosamente.")

    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()