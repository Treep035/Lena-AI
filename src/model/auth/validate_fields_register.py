import bcrypt
import re
import datetime
from model.database.db_connection import connect_to_db

from PyQt5.QtWidgets import (QMessageBox)

def validate_fields_register(self):
    username = self.text_username.text().strip()
    email = self.text_email.text().strip()
    password = self.text_password.text().strip()
    birthdate = self.date_birthdate.date().toString("yyyy-MM-dd")

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$'

    # Verifica que los campos no estén vacíos
    if not username or not email or not password:
        QMessageBox.warning(self, "Lena AI", "Please fill in all fields.")
        return
    
    if not re.match(email_regex, email):
        QMessageBox.warning(self, "Lena AI", "Email must be valid.")
        return
    
    if not re.match(password_regex, password):
        QMessageBox.warning(self, "Lena AI", "Password must be at least 8 characters long, contain at least one uppercase letter, and at least one special character.")
        return
    
    birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))

    if age < 18:
        QMessageBox.warning(self, "Lena AI", "You must be at least 18 years old to register.")
        return
    
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
            
        QMessageBox.information(self, "Success", "Registration successful!")
    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    # Si todo es válido
    QMessageBox.information(self, "Success", "All fields are valid!")