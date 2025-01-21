from model.database.db_connection import connect_to_db

def save_token_to_db(to_email, recover_password_token, recover_password_token_expiration):
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()

            cursor.execute("UPDATE user SET recover_password_token = %s, recover_password_token_expiration = %s WHERE email = %s", (recover_password_token, recover_password_token_expiration, to_email))

            connection.commit()

    except Exception as e:
        print("Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()