import bcrypt
import re
from model.database.db_connection import connect_to_db

def validate_fields_recover_password(self):
    new_password = self.text_new_password.text().strip()
    confirm_new_password = self.text_confirm_new_password.text().strip()
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$'
    
    no_fields = False
    invalid_token = False
    invalid_fields = False
    invalid_regex = False
    same_password = False
    
    # Verifica que los campos no estén vacíos
    if not new_password or not confirm_new_password:
        no_fields = True
        return no_fields, invalid_token, invalid_fields, invalid_regex, same_password
    
    try: # invalid token
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            
            # Consulta para obtener el password hasheado de la base de datos
            cursor.execute("SELECT * FROM user WHERE recover_password_token = %s", (self.token,))
            result = cursor.fetchone()

            if result:
                invalid_token = False
            else:
                invalid_token = True
                return no_fields, invalid_token, invalid_fields, invalid_regex, same_password

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Verifica que la nueva contraseña y la confirmación coincidan
    if new_password != confirm_new_password:
        invalid_fields = True
        return no_fields, invalid_token, invalid_fields, invalid_regex, same_password
    
    if not re.match(password_regex, new_password):
        invalid_regex = True
        return no_fields, invalid_token, invalid_fields, invalid_regex, same_password
    
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()

            cursor.execute("SELECT password FROM user WHERE recover_password_token = %s", (self.token,))
            result = cursor.fetchone()

            if result:
                # Si el resultado existe, verifica que las contraseñas coincidan
                stored_hashed_password = result[0]  # El password almacenado en la base de datos
                
                if bcrypt.checkpw(new_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    same_password = True
                    return no_fields, invalid_token, invalid_fields, invalid_regex, same_password
                else:
                    same_password = False

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if not no_fields and not invalid_token and not invalid_fields and not invalid_regex and not same_password:
        try:
            connection = connect_to_db()  # Llama a la función de conexión
            if connection:
                cursor = connection.cursor()
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                # Consulta para obtener el password hasheado de la base de datos

                cursor.execute(
                "UPDATE user SET password = %s WHERE recover_password_token = %s",
                (hashed_password, self.token)
                )

                cursor.execute(
                "UPDATE user SET recover_password_token = NULL, recover_password_token_expiration = NULL WHERE recover_password_token = %s",
                (self.token,)
                )
                connection.commit()
        except Exception as e:
            print(self, "Database Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return no_fields, invalid_token, invalid_fields, invalid_regex, same_password