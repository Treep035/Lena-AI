import webbrowser
import os
import random
import re

def process_message(self, message):
        # Diccionario de respuestas automáticas
        respuestas_bot = {
            ("hola", "buenas", "hi"): "¡Hola! ¿Cómo estás?",
            ("bien", "muy bien", "excelente"): "Me alegro de que todo vaya bien.",
            ("adiós", "bye", "hasta luego"): "¡Hasta luego! Espero verte pronto.",
            ("¿cómo estás?", "que tal estas?", "cómo te encuentras"): "Estoy aquí para ayudarte. ¿En qué puedo asistirte?",
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

        elif message.startswith("abre"):
            programa = message[5:].strip()  # Obtener el texto después de "abre"
            if programa in programas_disponibles:
                try:
                    os.startfile(programas_disponibles[programa]) 
                    bot_response = f"Abriendo {programa}..."
                except Exception as e:
                    bot_response = f"No se pudo abrir {programa}: {str(e)}"
            else:
                bot_response = f"No conozco el programa '{programa}'. Por favor, verifica el nombre."

        elif message.startswith("cara o cruz"):
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

        elif message.lower().startswith("nota de texto"):
            # Extraer el contenido de la nota
            contenido_nota = message[13:].strip()  # Quita "nota de texto"
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