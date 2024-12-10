import webbrowser
import os
import random
import re
import requests
from dotenv import load_dotenv

def process_message(self, message):
        # Diccionario de respuestas automáticas
        respuestas_bot = {
            ("hola", "buenas", "hi"): "¡Hola! ¿Cómo estás?",
            ("bien", "muy bien", "excelente"): "Me alegro de que todo vaya bien.",
            ("adiós", "bye", "hasta luego"): "¡Hasta luego! Espero verte pronto.",
            ("¿cómo estás?", "que tal estas?", "que tal", "cómo te encuentras"): "Estoy aquí para ayudarte. ¿En qué puedo asistirte?",
            ("gracias", "thank you"): "¡De nada! Siempre a tu servicio.",
        }

        programas_disponibles = {
            "calculadora": "calc",  # En Windows
            "bloc de notas": "notepad",  # En Windows
            "navegador": "https://www.google.com",  # Cambiar por el navegador instalado
            "explorador": "explorer",  # Explorador de archivos en Windows
            "word": "winword",  # Microsoft Word en Windows
            "excel": "excel",  # Abre Microsoft Excel
            "powerpoint": "powerpnt", # Abre Microsoft PowerPoint
        }

        adivinanzas = [
            {"pregunta": "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.", "respuesta": "La pera"},
            {"pregunta": "Tengo agujas, pero no pincho; paso el tiempo, pero no me quejo.", "respuesta": "El reloj"},
            {"pregunta": "Soy un rey y vivo en el mar. Todos me temen, pero no me pueden capturar.", "respuesta": "El tiburón"},
            {"pregunta": "Cuanto más lavo, más sucio está. ¿Qué es?", "respuesta": "El agua"},
            {"pregunta": "Vuela sin alas, silba sin boca. ¿Qué es?", "respuesta": "El viento"},
            {"pregunta": "Tiene cabeza, pero no cerebro; tiene boca, pero no habla. ¿Qué es?", "respuesta": "El ajo"},
            {"pregunta": "Oro parece, plata no es. ¿Qué es?", "respuesta": "El plátano"},
            {"pregunta": "Cuanto más grande es, menos se ve. ¿Qué es?", "respuesta": ("La oscuridad", "oscuridad")},
            {"pregunta": "No es ni humano ni animal, pero tiene corazón. ¿Qué es?", "respuesta": "La alcachofa"},
            {"pregunta": "Soy redondo y siempre estoy en el cielo, pero nunca me caigo. ¿Qué soy?", "respuesta": "El sol"}
        ]

        chistes = [
            "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
            "¿Qué le dice un jardinero a otro? ¡Qué planta!",
            "¿Qué le dice un árbol a otro? ¡Qué pasa, tronco!",
            "¿Qué le dice un pez a otro pez? ¡Nada!",
            "¿Qué le dice una iguana a su hermana gemela? ¡Iguanita!",
            "¿Qué le dice un huevo a otro huevo? ¡Huevo hermano!",
            "¿Por qué los pájaros no usan WhatsApp? Porque ya tienen Line.",
            "¿Qué le dice un semáforo a otro? ¡No me mires, que me pongo rojo!",
            "¿Qué le dice una impresora a otra? ¡Eres la hoja de mi vida!",
        ]

        # Comprobar si el mensaje comienza con "busca"
        if any(form in message for form in ["busca", "busques", "buscases", "buscar"]):
            # Dividir el mensaje en palabras y encontrar la posición de la forma del verbo
            palabras = message.split()
            try:
                # Encontrar el índice de cualquiera de las formas del verbo
                indice_busca = next(i for i, word in enumerate(palabras) if word in ["busca", "busques", "buscases", "buscar"])
                # Combinar las palabras después de la forma del verbo para formar la consulta
                query = " ".join(palabras[indice_busca + 1:]).strip()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    bot_response = f"Buscando en Google: {query}"
                else:
                    bot_response = "Por favor, especifica qué deseas buscar."
            except StopIteration:
                bot_response = "No entendí qué buscar. Por favor, intenta de nuevo."

        elif any(form in message for form in ["adivinanza", "adivinanzas", "acertijo", "acertijos"]):
            # Dividir el mensaje en palabras y encontrar la posición de la forma del verbo
            palabras = message.split()
            try:
                # Encontrar el índice de cualquiera de las formas del verbo
                indice_busca = next(i for i, word in enumerate(palabras) if word in ["adivinanza", "adivinanzas", "acertijo", "acertijos"])
                # Combinar las palabras después de la forma del verbo para formar la consulta
                self.adivinanza_actual = random.choice(adivinanzas)

                bot_response = f"Adivinanza: {self.adivinanza_actual['pregunta']}"
            except StopIteration:
                bot_response = "No entendí qué es lo que quieres. Por favor, intenta de nuevo."

        elif self.adivinanza_actual is not None:
            if any(message.lower() == respuesta.lower() for respuesta in (self.adivinanza_actual["respuesta"] if isinstance(self.adivinanza_actual["respuesta"], tuple) else [self.adivinanza_actual["respuesta"]])):
                bot_response = "¡Correcto! ¡Eres un genio!"
            else:
                bot_response = f"Incorrecto. La respuesta es: {self.adivinanza_actual['respuesta']}"

            self.adivinanza_actual = None

        elif any(form in message for form in ["chiste", "chistes"]):
            bot_response = random.choice(chistes)

        # Abrir programas
        elif any(form in message for form in ["abre"]):
            programa = message[5:].strip()  # Obtener el texto después de "abre"
            if programa in programas_disponibles:
                try:
                    os.startfile(programas_disponibles[programa]) 
                    bot_response = f"Abriendo {programa}..."
                except Exception as e:
                    bot_response = f"No se pudo abrir {programa}: {str(e)}"
            else:
                bot_response = f"No conozco el programa '{programa}'. Por favor, verifica el nombre."

        # Jugar cara o cruz
        elif any(form in message for form in ["cara o cruz"]):
            resultado = random.choice(["Cara", "Cruz"])
            bot_response = f"El resultado es: {resultado}."

        elif "piedra papel tijeras" in message:
            # Instrucciones para jugar
            bot_response = (
                "¡Vamos a jugar Piedra, Papel o Tijeras! Escribe 'piedra', 'papel' o 'tijeras' para hacer tu elección."
            )
            self.jugando_piedra_papel_tijeras = True

        elif self.jugando_piedra_papel_tijeras:
            if message in ["piedra", "papel", "tijeras"]:
                opciones = ["piedra", "papel", "tijeras"]
                eleccion_bot = random.choice(opciones)

                if message == eleccion_bot:
                    resultado = "¡Empate!"
                elif (message == "piedra" and eleccion_bot == "tijeras") or \
                     (message == "papel" and eleccion_bot == "piedra") or \
                     (message == "tijeras" and eleccion_bot == "papel"):
                    resultado = "¡Ganaste!"
                else:
                    resultado = "Perdiste."

                bot_response = (
                    f"Tú elegiste: {message.capitalize()}. Lena eligió: {eleccion_bot.capitalize()}. {resultado}"
                )
                self.jugando_piedra_papel_tijeras = False  # Termina el juego
            else:
                bot_response = "Por favor, elige entre 'piedra', 'papel' o 'tijeras'."

        elif any(form in message for form in ["nota de texto"]):
            # Extraer el contenido de la nota
            contenido_nota = message.lower().split("nota de texto", 1)[1].strip()
            if contenido_nota:
                documents_path = os.path.join(os.path.expanduser("~"))
                # Crear un archivo de texto
                file_path = os.path.join(documents_path, "LenaAI.txt")  # Cambia el nombre del archivo si es necesario
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(contenido_nota)

                # Abrir el archivo en el bloc de notas
                os.startfile(file_path)

                bot_response = f"Nota de texto creada. Abriendo el documento..."
            else:
                bot_response = "Por favor, escribe algo después de 'nota de texto' para crear la nota."

        elif re.search(r'\d+(\.\d+)?\s*[-+*/]\s*\d+(\.\d+)?', message):
            # Buscar la primera expresión matemática válida dentro del mensaje
            match = re.search(r'\d+(\.\d+)?\s*[-+*/]\s*\d+(\.\d+)?', message)
            if match:
                expresion = match.group()  # Extraer la expresión encontrada
                try:
                    resultado = eval(expresion)  # Evalúa la expresión matemática
                    bot_response = f"El resultado de {expresion} es {resultado}"
                except Exception as e:
                    bot_response = "Hubo un error al calcular la expresión."
            else:
                bot_response = "No encontré una expresión matemática válida en tu mensaje."

        elif re.search(r'clima\s+(?:de|en)?\s*(\w+)', message.lower()):
            match = re.search(r'clima\s+(?:de|en)?\s*(\w+)', message.lower())
            city = match.group(1)
            load_dotenv()
            api_key_climate = os.getenv('API_KEY_CLIMATE')

            def obtener_clima(city, api_key_climate):
                # URL base de la API de OpenWeatherMap para obtener el clima
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_climate}&units=metric&lang=es'
                
                # Hacer la solicitud GET
                response = requests.get(url)
                
                # Verificar si la solicitud fue exitosa
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extraer información relevante del JSON
                    temperatura = data['main']['temp']
                    descripcion = data['weather'][0]['description']
                    humedad = data['main']['humidity']
                    viento = data['wind']['speed']
                    
                    # Mostrar los resultados
                    climate = f"{temperatura}°C, {descripcion}, Humedad: {humedad}%, Viento: {viento} m/s"
                    print(f"Clima en {city.capitalize()}:")
                    print(f"Temperatura: {temperatura}°C")
                    print(f"Descripción: {descripcion}")
                    print(f"Humedad: {humedad}%")
                    print(f"Velocidad del viento: {viento} m/s")
                else:
                    print(f"No se pudo obtener información para {city}. Código de error: {response.status_code}")
                    climate = None
                
                return climate

            climate = obtener_clima(city, api_key_climate)

            if climate:
                bot_response = f"El clima en {city} es: {climate}"
            else:
                bot_response = f"No se pudo obtener el clima para {city}."

        else:
            # Buscar una respuesta automática en el diccionario
            bot_response = next(
                (respuestas_bot[key] for key in respuestas_bot if message in key),
                "Lo siento, no entiendo esa pregunta."
            )

        for keys, response in respuestas_bot.items():
            if message in keys:
                bot_response = response
                break
        
        return bot_response