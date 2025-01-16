import bcrypt
import re
from datetime import datetime
from model.database.db_connection import connect_to_db

from PyQt5.QtWidgets import (QMessageBox)

def validate_fields_register(self):
    username = self.text_username.text().strip()
    email = self.text_email.text().strip()
    password = self.text_password.text().strip()
    birthdate = self.date_birthdate.date().toString("yyyy-MM-dd")

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$'

    no_fields = False
    name_in_use = False
    invalid_regex_email = False
    email_in_use = False
    invalid_regex_password = False
    invalid_data_birthdate = False
    logged_in = False
    id_user = None

    connection = None
    cursor = None

    # Verifica que los campos no estén vacíos 
    # no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
    if not username or not email or not password:
        no_fields = True
        return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
    
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            
            # Consulta para obtener el password hasheado de la base de datos
            cursor.execute(f"SELECT username FROM user")
            result = [fila[0] for fila in cursor.fetchall()]

            if result:
                if username in result:
                    name_in_use = True
                    return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
                else:
                    name_in_use = False

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if not re.match(email_regex, email):
        invalid_regex_email = True
        return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
    
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()
            
            # Consulta para obtener el password hasheado de la base de datos
            cursor.execute(f"SELECT email FROM user")
            result = [fila[0] for fila in cursor.fetchall()]

            if result:
                if email in result:
                    email_in_use = True
                    return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
                else:
                    email_in_use = False

    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    if not re.match(password_regex, password):
        invalid_regex_password = True
        return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
    
    birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))

    if age < 18:
        invalid_data_birthdate = True
        return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
    connection = None
    cursor = None
        
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()

            theme_mode = "default"
            language = "eng"
                
            query = "INSERT INTO user (username, email, password, birthdate, theme_mode, language) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password, birthdate, theme_mode, language))
            connection.commit()

            query = "SELECT id_user FROM user WHERE email = %s"
            cursor.execute(query, (email,))
            
            id_user = cursor.fetchone()[0]
        
        logged_in = True
        return no_fields, name_in_use, invalid_regex_email, email_in_use, invalid_regex_password, invalid_data_birthdate, logged_in, id_user
    except Exception as e:
        print(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()