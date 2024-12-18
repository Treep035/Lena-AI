import bcrypt
from model.database.db_connection import connect_to_db

def validate_fields_login(self):
    email = self.text_email.text().strip()
    password = self.text_password.text().strip()

    # Verifica que los campos no estén vacíos
    if not email or not password:
        no_fields = True
        invalid_fields = False
        logged_in = False
        id_user = "0"
        return no_fields, invalid_fields, logged_in, id_user
    
    connection = None
    cursor = None

    logged_in = False  # Inicializar en False
    no_fields = False
    invalid_fields = False
    id_user = None

    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            
            # Consulta para obtener el password hasheado de la base de datos
            query = "SELECT password FROM user WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()  # Obtener el primer resultado de la consulta

            if result:
                # Si el resultado existe, verifica que las contraseñas coincidan
                stored_hashed_password = result[0]  # El password almacenado en la base de datos
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    # Las contraseñas coinciden
                    logged_in = True
                    query = "SELECT id_user FROM user WHERE email = %s"
                    cursor.execute(query, (email,))
                    id_user = cursor.fetchone()
                else:
                    # Las contraseñas no coinciden
                    invalid_fields = True
            else:
                # No se encontró el email en la base de datos
                invalid_fields = True

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return no_fields, invalid_fields, logged_in, id_user