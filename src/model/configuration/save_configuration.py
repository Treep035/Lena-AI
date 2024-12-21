from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request

# Método para guardar la imagen en MySQL
def save_image_to_db(file_path):
    try:
        # Leer el archivo de imagen en modo binario
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        # Conectar a la base de datos
        connection = connect_to_db()
        if connection is None:
            print("No se pudo conectar a la base de datos.")
            return

        cursor = connection.cursor()

        auth_token = get_auth_token_from_request()

        cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
        id_user = cursor.fetchone()

        # Consulta SQL para actualizar la imagen (ajusta el WHERE según corresponda)
        query = "UPDATE user SET profile_pic = %s WHERE id_user = %s"
        cursor.execute(query, (binary_data, id_user))

        # Confirmar los cambios
        connection.commit()
        print("Imagen guardada en la base de datos exitosamente.")

    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()