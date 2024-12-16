from model.database.db_connection import connect_to_db
import os
from PyQt5.QtGui import QPixmap, QImage
from io import BytesIO
from PIL import Image

from model.token.auth_token import get_auth_token_from_request

def account_picture_load():
        # Ruta predeterminada para la imagen
        default_image_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "images", "profile", "white", "profile.png")
        user_image_path = default_image_path

        # Conexión a la base de datos
        conn = connect_to_db()  # Cambiar por la ruta real de la base de datos
        cursor = conn.cursor()

        auth_token = get_auth_token_from_request()
        if auth_token is None:
            cursor.close()
            conn.close()
            return user_image_path

        cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
        id_user = cursor.fetchone()

        if id_user is None:
            cursor.close()
            conn.close()
            return user_image_path

        # Ahora, obtener la imagen actualizada de la base de datos
        cursor.execute("SELECT profile_pic FROM user WHERE id_user = %s", (id_user,))
        result = cursor.fetchone()

        # Verificar si hay una imagen almacenada
        if result and result[0]:
            # Si hay una imagen de perfil, guardarla temporalmente y usarla
            img_data = result[0]  # Los datos binarios de la imagen
            img = Image.open(BytesIO(img_data))  # Abrimos la imagen desde el flujo de bytes

            # Convertir la imagen PIL a QImage
            img = img.convert("RGBA")  # Convertir a un formato adecuado para QImage
            data = img.tobytes()  # Obtener los bytes de la imagen

            # Crear el QImage
            qimage = QImage(data, img.width, img.height, img.width * 4, QImage.Format_RGBA8888)

            # Crear el QPixmap desde QImage
            user_image_path = QPixmap.fromImage(qimage)

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()
        return user_image_path

def account_username_load():
        # Conexión a la base de datos
        conn = connect_to_db()  # Cambiar por la ruta real de la base de datos
        cursor = conn.cursor()

        auth_token = get_auth_token_from_request()

        cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
        id_user = cursor.fetchone()

        cursor.execute("SELECT username FROM user WHERE id_user = %s", (id_user,))
        result = cursor.fetchone()

        # Verificar si hay un nombre de usuario almacenado
        if result and result[0]:
            username = result[0]

        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()
        return username