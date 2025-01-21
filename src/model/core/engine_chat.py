import webbrowser
import wikipedia
import os
import random
import re
import requests
from dotenv import load_dotenv
from unidecode import unidecode
from datetime import datetime

def process_message(self, original_message):
        message = unidecode(original_message).lower()
        # Diccionario de respuestas automáticas
        respuestas_bot = {
            ("adios", "bye", "hasta luego"): "¡Hasta luego! Espero verte pronto.",
            ("bien", "muy bien", "excelente"): "Me alegro de que todo vaya bien.",
            ("cómo estas", "que tal estas", "que tal", "como te encuentras"): "Estoy aquí para ayudarte. ¿En qué puedo asistirte?",
            ("gracias", "thank you"): "¡De nada! Siempre a tu servicio.",
            ("que haces", "azul"): "Hola, aquí esperando para ayudarte.",
            ("que puedes hacer",): "Puedo responder preguntas, ayudarte con tareas, recomendar cosas o simplemente charlar contigo. ¡Tú dime!",
            ("eres humano",): "No, soy una inteligencia artificial, pero puedo hacer muchas cosas para ayudarte como si fuera un asistente humano.",
            ("tienes emociones",): "No tengo emociones como los humanos, pero estoy diseñado para responder de manera amigable y útil.",
            ("cual es el sentido de la vida",): "Esa es una gran pregunta. Algunos dicen que es encontrar la felicidad; otros, ayudar a los demás. ¿Tú qué piensas?",
            ("recuerdame algo mañana",): "No puedo recordar cosas automáticamente, pero te sugiero usar una aplicación de recordatorios. ¡Puedo ayudarte a configurarla si quieres!",
            ("como estas hecho",): "Estoy hecho de líneas de código y algoritmos diseñados para entenderte y ayudarte.",
            ("me puedes enseñar algo",): "¡Claro! ¿Qué te gustaría aprender? Puedo explicarte cosas de tecnología, idiomas, matemáticas y mucho más.",
            ("cuentame algo interesante",): "¿Sabías que los pulpos tienen tres corazones? Dos bombean sangre a las branquias y uno al resto del cuerpo.",
            ("estoy aburrido",): "¿Qué te parece si jugamos a algo, te cuento un dato curioso o vemos una idea para un nuevo proyecto?",
            ("me siento triste",): "Lo siento mucho. A veces hablar con alguien o hacer algo que te guste puede ayudarte. Estoy aquí si necesitas apoyo.",
            ("que puedo hacer para ser mas productivo",): "Intenta organizar tus tareas por prioridad, usar una técnica como Pomodoro y asegurarte de tomar descansos.",
            ("dame un consejo",): "Nunca dejes de aprender, incluso de los errores. Cada experiencia puede ayudarte a crecer.",
            ("que significa",): "Déjame buscarlo para darte la mejor definición.",
            ("recomiendame algo para comer",): "¿Qué tal una pizza casera o unos tacos? ¡Siempre son una buena idea!",
            ("te gusta",): "No tengo gustos como los humanos, pero puedo decirte por qué a la gente le encanta eso.",
            ("que hago si me siento estresado",): "Intenta respirar profundamente, salir a caminar o escuchar música relajante.",
            ("cuentame una historia",): "Había una vez un pequeño robot que quería aprender todo sobre los humanos.",
            ("cual es tu color favorito",): "No tengo ojos para ver colores, pero el azul suele ser muy popular.",
            ("puedes darme ideas para un proyecto",): "Por supuesto, ¿qué te parece un blog personal, una app sencilla o algo relacionado con tus intereses?",
        }

        programas_disponibles = {
            "calculadora": "calc",  # En Windows
            "bloc de notas": "notepad",  # En Windows
            "navegador": "https://www.google.com",  # Cambiar por el navegador instalado
            "explorador": "explorer",  # Explorador de archivos en Windows
            "word": "winword",  # Microsoft Word en Windows
            "excel": "excel",  # Abre Microsoft Excel
            "powerpoint": "powerpnt", # Abre Microsoft PowerPoint
            "onenote": "onenote",  # Abre Microsoft OneNote
            "outlook": "outlook",  # Abre Microsoft Outlook
            "paint": "mspaint",  # Abre Paint en Windows
            "panel de control": "control",  # Abre el Panel de Control en Windows
            "cmd": "cmd",  # Abre el Símbolo del Sistema en Windows
            "powershell": "powershell",  # Abre PowerShell en Windows

            # Herramientas del sistema
            "administrador de tareas": "taskmgr",
            "panel de control": "control",
            "símbolo del sistema": "cmd",
            "powershell": "powershell",
            "herramientas del sistema": "msconfig",
            "información del sistema": "msinfo32",
            "registro de windows": "regedit",

            # Aplicaciones de oficina
            "onenote": "onenote",
            "microsoft access": "msaccess",
            "libreoffice writer": "soffice --writer",
            "libreoffice calc": "soffice --calc",
            "google docs": "https://docs.google.com",

            # Aplicaciones de navegación e internet
            "mozilla firefox": "firefox",
            "microsoft edge": "msedge",
            "google chrome": "chrome",
            "opera": "opera",
            "skype": "skype",
            "discord": "discord",
            "zoom": "zoom",
            "teams": "teams",

            # Aplicaciones multimedia
            "reproductor de música": "wmplayer",
            "vlc media player": "vlc",
            "spotify": "spotify",
            "audacity": "audacity",
            "galería de fotos": "ms-photos:",
            "editor de video": "moviemaker",

            # Aplicaciones de diseño y edición
            "paint": "mspaint",
            "photoshop": "photoshop",
            "gimp": "gimp",
            "inkscape": "inkscape",
            "coreldraw": "coreldraw",

            # Herramientas de desarrollo
            "visual studio code": "code",
            "intellij idea": "idea",
            "eclipse": "eclipse",
            "pycharm": "pycharm",
            "xampp": "xampp-control",
            "git bash": "git-bash",

            # Aplicaciones para juegos
            "steam": "steam",
            "epic games launcher": "epicgameslauncher",
            "blizzard battle.net": "battle.net",
            "riot client": "riotclient",

            # Herramientas de comunicación y productividad
            "slack": "slack",
            "notion": "notion",
            "trello": "trello",
            "asana": "asana",

            # Utilidades adicionales
            "bloc de dibujos": "inkscape",
            "control remoto": "teamviewer",
            "compresor de archivos": "winrar",
            "administrador de descargas": "idman"
        }

        adivinanzas = [
            {"pregunta": "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.", "respuesta": "la pera"},
            {"pregunta": "Tengo agujas, pero no pincho; paso el tiempo, pero no me quejo.", "respuesta": "el reloj"},
            {"pregunta": "Soy un rey y vivo en el mar. Todos me temen, pero no me pueden capturar.", "respuesta": "el tiburon"},
            {"pregunta": "Cuanto más lavo, más sucio está. ¿Qué es?", "respuesta": "el agua"},
            {"pregunta": "Vuela sin alas, silba sin boca. ¿Qué es?", "respuesta": "el viento"},
            {"pregunta": "Tiene cabeza, pero no cerebro; tiene boca, pero no habla. ¿Qué es?", "respuesta": "el ajo"},
            {"pregunta": "Oro parece, plata no es. ¿Qué es?", "respuesta": "el platano"},
            {"pregunta": "Cuanto más grande es, menos se ve. ¿Qué es?", "respuesta": "la oscuridad"},
            {"pregunta": "No es ni humano ni animal, pero tiene corazón. ¿Qué es?", "respuesta": "la alcachofa"},
            {"pregunta": "Soy redondo y siempre estoy en el cielo, pero nunca me caigo. ¿Qué soy?", "respuesta": "el sol"}
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
        if any(form in message for form in ["busca", "busques", "buscases", "buscar", "buscame"]):
            # Dividir el mensaje en palabras y encontrar la posición de la forma del verbo
            palabras = message.split()
            try:
                # Encontrar el índice de cualquiera de las formas del verbo
                indice_busca = next(i for i, word in enumerate(palabras) if word in ["busca", "busques", "buscases", "buscar", "buscame"])
                # Combinar las palabras después de la forma del verbo para formar la consulta
                query = " ".join(palabras[indice_busca + 1:]).strip()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    bot_response = f"Buscando en Google: {query}"
                else:
                    bot_response = "Por favor, especifica qué deseas buscar."
            except StopIteration:
                bot_response = "No entendí qué buscar. Por favor, intenta de nuevo."

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

        elif any(form in message for form in ["explica", "que es", "quien es", "definicion de", "definicion", "definir", "que significa"]):
            consulta = re.sub(r"(explica|que es|quien es|definicion de|definicion|definir|que significa)", "", message, flags=re.IGNORECASE).strip()
            try:
                wikipedia.set_lang("es")  # Establece el idioma a español
                # Busca el término en Wikipedia
                resultados = wikipedia.search(consulta)
                if resultados:
                    # Obtén el resumen del primer resultado
                    resumen = wikipedia.summary(resultados[0], sentences=2)  # Resumen de 3 frases
                    resumen_limpio = re.sub(r'\[\d+\]', '', resumen)
                    bot_response = f"{resumen_limpio}"
                else:
                    bot_response = "No encontré información sobre eso en Wikipedia."
            except wikipedia.exceptions.DisambiguationError as e:
                bot_response = f"La consulta es ambigua. Quizás quisiste decir: {', '.join(e.options[:5])}."
            except wikipedia.exceptions.PageError:
                bot_response = "No se encontró una página relacionada en Wikipedia."
            except Exception as e:
                bot_response = f"Hubo un error al buscar en Wikipedia: {str(e)}"

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

        elif any(form in message for form in ["nota de texto"]):
            # Extraer el contenido de la nota
            contenido_nota = message.lower().split("nota de texto", 1)[1].strip()
            if contenido_nota:
                documents_path = os.path.join(os.path.expanduser("~"))
                # Crear un archivo de texto
                file_path = os.path.join(documents_path, "nota_de_texto_LenaAI.txt")  # Cambia el nombre del archivo si es necesario
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(contenido_nota)

                # Abrir el archivo en el bloc de notas
                os.startfile(file_path)

                bot_response = f"Nota de texto creada. Abriendo el documento..."
            else:
                bot_response = "Por favor, escribe algo después de 'nota de texto' para crear la nota."

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
                    f"Tú elegiste: {message.capitalize()}. Yo eligí: {eleccion_bot.capitalize()}. {resultado}"
                )
                self.jugando_piedra_papel_tijeras = False  # Termina el juego
            else:
                self.jugando_piedra_papel_tijeras = False

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

        elif re.search(r"\bhora\b", message.lower()):
            now = datetime.now()
            bot_response = f"Son las {now.strftime('%H:%M:%S')}"

        elif any(form in message.lower() for form in ["hola", "buenos días", "buenas tardes", "buenas noches", "buenas"]):
            bot_response = "¡Hola! ¿Cómo podría ayudarte?"

        else:
            # Buscar una respuesta automática en el diccionario
            message = message.lower()
            message = ''.join(c for c in message if c.isalnum() or c.isspace())  # Eliminar caracteres especiales
            bot_response = next(
                (respuestas_bot[key] for key in respuestas_bot if message in key),
                "Lo siento, no entiendo esa pregunta."
            )

        for keys, response in respuestas_bot.items():
            if message in keys:
                bot_response = response
                break

        return bot_response