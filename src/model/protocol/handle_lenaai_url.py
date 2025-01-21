from view.auth.new_password import NewPassword

def handle_lenaai_url(url):
    """Procesa la URL y decide qué widget abrir"""
    print(f"URL recibida: {url}")
    if url.startswith("lenaai://reset_password"):
        # Extraer el token y pasar al widget adecuado
        token = url.split("token=")[-1]
        print(f"Token recibido: {token}")
        dialog = NewPassword(token)  # Suponiendo que 'NewPassword' puede aceptar un token como parámetro
        dialog.exec_()