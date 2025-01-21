from model.database.db_connection import connect_to_db

def check_email_to_db(to_email):
    try:
        connection = connect_to_db()  # Llama a la función de conexión
        if connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM user WHERE email = %s", (to_email,))
            result = cursor.fetchone()

            if result:
                sent = True
                return sent
            else:
                sent = False
                return sent

    except Exception as e:
        print("Database Error", f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()