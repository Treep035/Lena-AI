import bcrypt
import re
from model.database.db_connection import connect_to_db
from model.token.auth_token import get_auth_token_from_request

def validate_fields_change_name(self):
    actual_name_input = self.actual_name_input.text().strip()
    modified_name_input = self.modified_name_input.text().strip()
    confirm_modified_name_input = self.confirm_modified_name_input.text().strip()
    
    no_fields = False
    not_actual_name = False
    invalid_fields = False
    name_in_use = False
    same_name = False
    
    # Verifica que los campos no estén vacíos
    if not actual_name_input or not modified_name_input or not confirm_modified_name_input:
        no_fields = True
        return no_fields, not_actual_name, invalid_fields, name_in_use, same_name
    
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            auth_token = get_auth_token_from_request()
            
            # Consulta para obtener el password hasheado de la base de datos
            cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
            id_user = cursor.fetchone()

            cursor.execute("SELECT username FROM user WHERE id_user = %s", (id_user,))
            result = cursor.fetchone()

            if result:
                # Si el resultado existe, verifica que las contraseñas coincidan
                stored_username = result[0]  # El password almacenado en la base de datos
                
                if actual_name_input != stored_username:
                    not_actual_name = True
                    return no_fields, not_actual_name, invalid_fields, name_in_use, same_name
                    # Las contraseñas coinciden
                else:
                    not_actual_name = False

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Verifica que la nueva contraseña y la confirmación coincidan
    if modified_name_input != confirm_modified_name_input:
        invalid_fields = True
        return no_fields, not_actual_name, invalid_fields, name_in_use, same_name
    
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            auth_token = get_auth_token_from_request()
            
            # Consulta para obtener el password hasheado de la base de datos
            cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
            id_user = cursor.fetchone()

            cursor.execute("SELECT username FROM user WHERE id_user = %s", (id_user,))
            result = cursor.fetchone()

            if result:
                # Si el resultado existe, verifica que las contraseñas coincidan
                stored_username = result[0]  # El password almacenado en la base de datos
                
                if modified_name_input != stored_username:
                    same_name = False
                else:
                    same_name = True
                    return no_fields, not_actual_name, invalid_fields, name_in_use, same_name

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    ##################
    
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            auth_token = get_auth_token_from_request()
            
            # Consulta para obtener el password hasheado de la base de datos
            cursor.execute(f"SELECT username FROM user")
            result = [fila[0] for fila in cursor.fetchall()]

            if result:
                if modified_name_input in result:
                    name_in_use = True
                    return no_fields, not_actual_name, invalid_fields, name_in_use, same_name
                else:
                    name_in_use = False

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    ##################

    if not no_fields and not not_actual_name and not invalid_fields and not name_in_use and not same_name:
        try:
            connection = connect_to_db()  # Llama a la función de conexión
            if connection:
                cursor = connection.cursor()
                auth_token = get_auth_token_from_request()
                # Consulta para obtener el password hasheado de la base de datos
                cursor.execute(f"SELECT id_user FROM auth_token WHERE auth_token = %s", (auth_token,))
                id_user = cursor.fetchone()

                cursor.execute(
                "UPDATE user SET username = %s WHERE id_user = %s",
                (modified_name_input, id_user)
                )
                connection.commit()
        except Exception as e:
            print(self, "Database Error", f"An error occurred: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        return no_fields, not_actual_name, invalid_fields, name_in_use, same_name