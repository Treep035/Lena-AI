import threading
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import webbrowser
import wikipedia
import os
import re
import requests
from dotenv import load_dotenv
import random
from googletrans import Translator, LANGUAGES
from controller.stop_animation_controller import StopAnimationSignal
import asyncio

# Función para hablar usando gTTS
def speak(text):
    try:
        tts = gTTS(text=text, lang='es')
        audio_file = "temp_audio.mp3"  # Archivo temporal
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)  # Eliminar el archivo después de reproducir
    except Exception as e:
        print(f"Error al generar la voz: {e}")

# Función para transcribir el audio a texto
def transcribe_audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Ajustar para ruido ambiental
        print("Escuchando...")  # Mover el print aquí
        close = False
        while close == False:
            try:
                audio = recognizer.listen(source)  # Capturar el audio
                # Convertir el audio a texto usando Google Web Speech API
                text = recognizer.recognize_google(audio, language="es-ES")
                print(f"Texto detectado: {text}")
                close = True
                return text
            except sr.UnknownValueError:
                print("No se pudo entender el audio.")
            except sr.RequestError as e:
                print(f"Error con el servicio de reconocimiento: {e}")
                speak("Hubo un problema con el servicio de reconocimiento.")
                return ""

def stop(self):
    self._stop_event.set()

def start(self):

    respuestas_bot = {
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

    palabras_cancelation = [
        "adiós", "nada", "no", "cancelar", "detener", 
        "salir", "cerrar", "terminar", "finalizar", 
        "acabar", "terminado", "finalizado", "stop", "exit",
        "cancel", "end", "finish", "finished", "bye", "nothing",
    ]
    palabras_afirmation = [
        "sí", "claro", "correcto", "correctamente", "por supuesto",
        "definitivamente", "exactamente", "afirmativo", "vale", 
        "de acuerdo", "seguro", "perfecto", "obvio", "así es", 
        "cierto", "sin duda", "naturalmente", "confirmado",
        "en efecto", "está bien", "es cierto", "evidentemente",
        "ya lo creo", "tienes razón", "ok", "okay", "yeah", 
        "yes", "of course", "sure", "definitely", "absolutely", 
        "that’s right", "correct", "exactly", "fine", "all right",
        "agreed", "indeed", "confirmed", "roger that", "affirmative"
    ]
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
    
    adivinanzas = [
        {"pregunta": "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.", "respuesta": "La pera"},
        {"pregunta": "Tengo agujas, pero no pincho; paso el tiempo, pero no me quejo.", "respuesta": "El reloj"},
        {"pregunta": "Soy un rey y vivo en el mar. Todos me temen, pero no me pueden capturar.", "respuesta": "El tiburón"},
        {"pregunta": "Cuanto más lavo, más sucio está. ¿Qué es?", "respuesta": "El agua"},
        {"pregunta": "Vuela sin alas, silba sin boca. ¿Qué es?", "respuesta": "El viento"},
        {"pregunta": "Tiene cabeza, pero no cerebro; tiene boca, pero no habla. ¿Qué es?", "respuesta": "El ajo"},
        {"pregunta": "Oro parece, plata no es. ¿Qué es?", "respuesta": "El plátano"},
        {"pregunta": "Cuanto más grande es, menos se ve. ¿Qué es?", "respuesta": "La oscuridad"},
        {"pregunta": "No es ni humano ni animal, pero tiene corazón. ¿Qué es?", "respuesta": "La alcachofa"},
        {"pregunta": "Soy redondo y siempre estoy en el cielo, pero nunca me caigo. ¿Qué soy?", "respuesta": "El sol"}
    ]

    language_keywords = {v.lower(): k for k, v in LANGUAGES.items()}  # LANGUAGES viene de googletrans

    language_aliases = {
    "inglés": "english",
    "español": "spanish",
    "catalán": "catalan",
    "francés": "french",
    "alemán": "german",
    "italiano": "italian",
    "portugués": "portuguese (portugal, brazil)",
    "chino": "chinese",
    "japonés": "japanese",
    "ruso": "russian",
}
    
    divisas = {
    "dólar": "USD",
    "euro": "EUR",
    "libra": "GBP",
    "yen": "JPY",
    "yuan": "CNY",
    "peso": "MXN",
    }
    
    palabras_a_numeros = {
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
}

    self._stop_event = threading.Event()
    # Hablar al inicio
    if not self.already_started:
        speak("Hola, estoy lista para atenderte. Pregúntame lo que necesites.")
    else:
        speak("¿En qué puedo ayudarte ahora?")
    print("Hilo iniciado.")
    while not self._stop_event.is_set():
        print("Hilo trabajando...")
        try:
            user_input = transcribe_audio_to_text()
            if user_input:
                response = ""

                if any(form in user_input.lower() for form in ["reproduce", "reproducir", "reprodúceme", "música", "músicas", "canción",
                                                                "canciones", "escuchar", "pon", "ponme", "poner"]):
                    reproduce_finished = False
                    while not reproduce_finished:
                        match = re.search(r"(reprodúceme(?: la)?|reproduce(?: la)?|reproducir(?: la)?|poner(?: la)?|músicas(?: de)?|música(?: de)?|canciones(?: de)?|canción(?: de)?|escuchar(?: la)?|pon(?:me)?(?: la)?)\s+(?:canciones(?: de)?|canción(?: de)?|músicas(?: de)?|música(?: de)?\s)?(.*)", user_input.lower())

                        if match and match.group(2):  # Si se encuentra una coincidencia y hay palabras después de la clave
                            search_query = match.group(2).strip()  # Extraer la parte que viene después de la palabra clave
                        else:  # Si el usuario no menciona nada después de la palabra clave
                            speak("¿Qué canción o artista quieres escuchar?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                reproduce_finished = True
                                stop(self)
                            search_query = user_input.lower().strip()

                        load_dotenv()
                        api_key_youtube = os.getenv('API_KEY_YOUTUBE')

                        def get_youtube_video_url(query, api_key_youtube):
                            # Hacer la búsqueda en YouTube
                            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={api_key_youtube}"
                            response = requests.get(url).json()
                            
                            # Obtener el primer resultado (ID del video)
                            if 'items' in response and len(response['items']) > 0:
                                for item in response['items']:
                                    # Verifica si el item es un video
                                    if item['id']['kind'] == 'youtube#video':
                                        try:
                                            # Obtén el videoId
                                            video_id = item['id'].get('videoId')
                                            if video_id:
                                                return f"https://www.youtube.com/watch?v={video_id}"
                                        except KeyError as e:
                                            print(f"Error de clave en la respuesta de la API: {e}")
                                            return None
                                print("No se encontró un video válido.")
                                return None
                            else:
                                print("No se encontraron resultados en YouTube.")
                                return None
                        
                        video_url = get_youtube_video_url(search_query, api_key_youtube)

                        if video_url:
                            webbrowser.open(video_url)
                            speak(f"Reproduciendo {search_query} en YouTube.")
                            reproduce_finished = True
                            stop(self)
                        else:
                            speak(f"No he encontrado resultados para {search_query}.")
                            time.sleep(1)
                            speak("¿Necesitas algo más?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                speak("¿Qué más necesitas?")
                                user_input = transcribe_audio_to_text()
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                reproduce_finished = True
                                stop(self)
                            else:
                                reproduce_finished_2 = False
                                while not reproduce_finished_2:
                                    speak("¿No te entendí, ¿Necesitas algo más?")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        reproduce_finished_2 = True
                                        speak("¿Qué más necesitas?")
                                        user_input = transcribe_audio_to_text()
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        reproduce_finished_2 = True
                                        reproduce_finished = True
                                        stop(self)
                                    else:
                                        pass

                elif any(form in user_input.lower() for form in ["encuentra en google", "encuéntrame en google", "busca en google", "buscar en google", "búscame en google", "encuentra en internet", "encuéntrame en internet", "busca en internet", "buscar en internet", "búscame en internet", "busca", "buscar", "búscame", "encuentra", "encuéntrame"]):
                    search_finished = False
                    while not search_finished:
                        match = re.search(r"(encuentra en google|encuéntrame en google|busca en google|buscar en google|búscame en google|encuentra en internet|encuéntrame en internet|busca en internet|buscar en internet|búscame en internet|busca|buscar|búscame|encuentra|encuéntrame)\s+(.*)", user_input.lower())
                        if match and match.group(2):  # Si hay un texto para traducir
                            search_query = match.group(2).strip()
                        else:
                            pass
                        search_url = f"https://www.google.com/search?q={search_query}"
                        webbrowser.open(search_url)
                        response = f"Buscando {search_query} en Google."
                        speak(response)
                        time.sleep(2)
                        search_finished_2 = False
                        while not search_finished_2:
                            speak("¿Es esto lo que buscabas?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                speak("¡Perfecto!, si necesitas algo más, dímelo")
                                search_finished = True
                                search_finished_2 = True
                                stop(self)
                            elif user_input == "no":
                                speak("Entonces que es lo que quieres buscar?")
                                user_input = transcribe_audio_to_text()
                                if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    search_finished = True
                                    stop(self)
                                else:
                                    search_query = user_input.lower().replace("busca ", "")
                                    search_url = f"https://www.google.com/search?q={search_query}"
                                    webbrowser.open(search_url)
                                    response = f"Buscando {search_query} en Google."
                                    speak(response)
                                    time.sleep(2)
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                search_finished = True
                                search_finished_2 = True
                                stop(self)
                
                elif any(form in user_input.lower() for form in ["abre", "ábreme", "abrir", "abre el programa", "ábreme el programa", "abrir el programa", "abre la app", "ábreme la app", "abrir la app", "abre la aplicación", "ábreme la aplicación", "abrir la aplicación", "abre programa", "ábreme programa", "abrir programa", "abre app", "ábreme app", "abrir app", "abre aplicación", "ábreme aplicación", "abrir aplicación"]):
                    open_finished = False
                    while not open_finished:
                        match = re.search(r"(abre el programa|ábreme el programa|abrir el programa|abre la app|ábreme la app|abrir la app|abre la aplicación|ábreme la aplicación|abrir la aplicación|abre programa|ábreme programa|abrir programa|abre app|ábreme app|abrir app|abre aplicación|ábreme aplicación|abrir aplicación|abre|ábreme|abrir)\s+(.*)", user_input.lower())
                        if match and match.group(2):  # Si hay un texto para traducir
                                programa = match.group(2).strip()
                        else:
                            pass
                        if programa in programas_disponibles:
                            try:
                                os.startfile(programas_disponibles[programa]) 
                                speak(f"Abriendo {programa}...")
                                speak("¿Es esto lo que querías abrir?")
                                user_input = transcribe_audio_to_text()
                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    speak("¡Perfecto!, si necesitas algo más, dímelo")
                                    open_finished = True
                                    stop(self)
                                else:
                                    speak("Entonces que es lo que quieres abrir?")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        open_finished = True
                                        stop(self)
                            except Exception as e:
                                speak(f"No se pudo abrir {programa}: {str(e)}")
                                open_finished = True
                                stop(self)
                        else:
                            speak(f"No conozco el programa '{programa}'. ¿A cual te refieres?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                open_finished = True
                                stop(self)

                # Crear un diccionario para mapear palabras clave a códigos de idioma

                elif any(form in user_input.lower() for form in ["traduce", "traducir", "traducción", "traductor", "traduce esto", "traduce lo siguiente", "tradúce la palabra", "tradúce la frase", "tradúce la oración", "traduce la siguiente frase", "traduce la siguiente oración", "traduce la siguiente palabra", "tradúceme", "tradúceme esto", "tradúceme lo siguiente", "tradúceme la frase", "tradúceme la oración", "tradúceme la palabra", "tradúceme la siguiente frase", "tradúceme la siguiente oración", "tradúceme la siguiente palabra"]):
                        match = re.search(r"(traduce esto|traduce lo siguiente|tradúce la palabra|tradúce la frase|tradúce la oración|traduce la siguiente frase|traduce la siguiente oración|traduce la siguiente palabra|tradúceme esto|tradúceme lo siguiente|tradúceme la frase|tradúceme la oración|tradúceme la palabra|tradúceme la siguiente frase|tradúceme la siguiente oración|tradúceme la siguiente palabra|traduce|traducir|traducción|traductor|tradúceme)\s+(.*)", user_input.lower())

                        if match and match.group(2):  # Si hay un texto para traducir
                            user_input = match.group(2).strip()
                        else:
                            speak("¿Qué texto quieres traducir?")
                            user_input = transcribe_audio_to_text()
                        translate_finished = False
                        while not translate_finished:
                            match = re.search(r"(traduce esto|traduce lo siguiente|tradúce la palabra|tradúce la frase|tradúce la oración|traduce la siguiente frase|traduce la siguiente oración|traduce la siguiente palabra|tradúceme esto|tradúceme lo siguiente|tradúceme la frase|tradúceme la oración|tradúceme la palabra|tradúceme la siguiente frase|tradúceme la siguiente oración|tradúceme la siguiente palabra|traduce|traducir|traducción|traductor|tradúceme)\s+(.*)", user_input.lower())

                            if match and match.group(2):  # Si hay un texto para traducir
                                user_input = match.group(2).strip()
                            else:
                                pass

                            text_to_translate = user_input.strip()
                            # Preguntar por el idioma objetivo
                            speak("¿A qué idioma quieres traducir?")
                            # for lang_code, lang_name in LANGUAGES.items():
                                # print(f"{lang_code}: {lang_name}")
                            user_input = transcribe_audio_to_text()
                            translate_finished_2 = False
                            while not translate_finished_2:
                                # Normalizar y buscar idioma
                                idioma_objetivo = None
                                user_input = user_input.lower().strip()

                                # Buscar en alias
                                for alias, english_name in language_aliases.items():
                                    if alias in user_input:
                                        idioma_objetivo = english_name
                                        break
                                else:
                                    idioma_objetivo = user_input  # Si no hay alias, usamos el texto original

                                target_language = language_keywords.get(idioma_objetivo, None)

                                def run_translation_in_thread(text_to_translate, target_language):
                                    async def translate_text(text_to_translate, target_language):
                                        translator = Translator()
                                        try:
                                            translated = await translator.translate(text_to_translate, dest=target_language)
                                            speak(f"La traducción es: {translated.text}")
                                            print(f"La traducción es: {translated.text}")
                                        except Exception as e:
                                            speak("Hubo un error al traducir. Inténtalo de nuevo.")
                                            print(f"Error: {e}")

                                    def start_translation_loop():
                                        loop = asyncio.new_event_loop()
                                        asyncio.set_event_loop(loop)

                                        try:
                                            loop.run_until_complete(translate_text(text_to_translate, target_language))
                                        except Exception as e:
                                            print(f"Error al ejecutar la tarea asíncrona: {e}")
                                        finally:
                                            loop.close()

                                    thread = threading.Thread(target=start_translation_loop)
                                    thread.start()
                                    thread.join()
                                
                                if target_language:
                                    run_translation_in_thread(text_to_translate, target_language)
                                    # Preguntar si quiere traducir algo más
                                    speak("¿Quieres traducir algo más?")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        speak("Dime que quieres traducir.")
                                        user_input = transcribe_audio_to_text()
                                        translate_finished_2 = True
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        translate_finished_2 = True
                                        translate_finished = True
                                        stop(self)
                                    else:
                                        translate_finished_3 = False
                                        while not translate_finished_3:
                                            speak("No entendí. ¿Quieres traducir algo más?")
                                            user_input = transcribe_audio_to_text()
                                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                                speak("Dime el texto que quieres traducir.")
                                                user_input = transcribe_audio_to_text()
                                                translate_finished_3 = True
                                                translate_finished_2 = True
                                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                                translate_finished_3 = True
                                                translate_finished_2 = True
                                                translate_finished = True
                                                stop(self)
                                            else:
                                                pass
                                else:
                                    speak(f"No entendí el idioma '{idioma_objetivo}'. Vuelve a decirlo, por favor.")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        translate_finished_2 = True
                                        translate_finished = True
                                        stop(self)

                elif any(form in user_input.lower() for form in ["explica", "qué es", "quién es", "definición de", "definición", "definir", "qué significa"]):
                    wikipedia_finished = False
                    while not wikipedia_finished:
                        consulta = re.sub(r"(explica|qué es|quién es|definición de|definición|definir|qué significa)", "", user_input, flags=re.IGNORECASE).strip()
                        try:
                            wikipedia.set_lang("es")  # Establece el idioma a español
                            # Busca el término en Wikipedia
                            resultados = wikipedia.search(consulta)
                            if resultados:
                                # Obtén el resumen del primer resultado
                                resumen = wikipedia.summary(resultados[0], sentences=1)  # Resumen de 3 frases
                                resumen_limpio = re.sub(r'\[\d+\]', '', resumen)
                                speak(f"Segun Wikipedia: {resumen_limpio}")
                                time.sleep(1)
                                speak("¿Tienes alguna consulta más?")
                                user_input = transcribe_audio_to_text()
                                wikipedia_finished_2 = False
                                while not wikipedia_finished_2:
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        wikipedia_finished_2 = True
                                        speak("¿Qué más quieres saber?")
                                        user_input = transcribe_audio_to_text()
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        wikipedia_finished_2 = True
                                        wikipedia_finished = True
                                        stop(self)
                                    else:
                                        wikipedia_finished_3 = False
                                        while not wikipedia_finished_3:
                                            speak("¿No te entendí, ¿tienes alguna consulta más?")
                                            user_input = transcribe_audio_to_text()
                                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                                wikipedia_finished_3 = True
                                                wikipedia_finished_2 = True
                                                speak("¿Qué más quieres saber?")
                                                user_input = transcribe_audio_to_text()
                                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                                wikipedia_finished_3 = True
                                                wikipedia_finished_2 = True
                                                wikipedia_finished = True
                                                stop(self)
                                            else:
                                                pass
                            else:
                                speak("No encontré información sobre eso en Wikipedia.")
                                time.sleep(1)
                                speak("¿Tienes alguna consulta más?")
                                user_input = transcribe_audio_to_text()
                                wikipedia_finished_4 = False
                                while not wikipedia_finished_4:
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        wikipedia_finished_4 = True
                                        speak("¿Qué más quieres saber?")
                                        user_input = transcribe_audio_to_text()
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        wikipedia_finished_4 = True
                                        wikipedia_finished = True
                                        stop(self)
                                    else:
                                        wikipedia_finished_5 = False
                                        while not wikipedia_finished_5:
                                            speak("¿No te entendí, ¿tienes alguna consulta más?")
                                            user_input = transcribe_audio_to_text()
                                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                                wikipedia_finished_5 = True
                                                wikipedia_finished_4 = True
                                                speak("¿Qué más quieres saber?")
                                                user_input = transcribe_audio_to_text()
                                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                                wikipedia_finished_5 = True
                                                wikipedia_finished_4 = True
                                                wikipedia_finished = True
                                                stop(self)
                                            else:
                                                pass
                        except wikipedia.exceptions.DisambiguationError as e:
                            speak(f"La consulta es ambigua. Quizás quisiste decir: {', '.join(e.options[:5])}.")
                        except wikipedia.exceptions.PageError:
                            speak("No se encontró una página relacionada en Wikipedia.")
                        except Exception as e:
                            speak(f"Hubo un error al buscar en Wikipedia: {str(e)}")
                            print(f"Error al buscar en Wikipedia: {str(e)}")

                elif re.search(r'clima\s+(?:de|en)?\s*(\w+)', user_input.lower()):
                    match = re.search(r'clima\s+(?:de|en)?\s*(\w+)', user_input.lower())
                    city = match.group(1)
                    climate_finished = False
                    while not climate_finished:
                        
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
                                climate = f"{temperatura}°C, {descripcion}, humedad del {humedad}% y viento de {viento} m/s"
                                # speak(f"Clima en {city.capitalize()}:")
                                # speak(f"Temperatura: {temperatura}°C")
                                # speak(f"Descripción: {descripcion}")
                                # speak(f"Humedad: {humedad}%")
                                # speak(f"Velocidad del viento: {viento} m/s")
                            else:
                                speak(f"No se pudo obtener información para {city}.")
                                climate = None
                            
                            return climate

                        climate = obtener_clima(city, api_key_climate)

                        if climate:
                            speak(f"El clima en {city} es: {climate}")
                            time.sleep(1)
                            speak("¿Quieres saber el clima de otra ciudad?")
                            user_input = transcribe_audio_to_text()
                            climate_finished_2 = False
                            while not climate_finished_2:
                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    speak("¿De qué ciudad?")
                                    climate_finished_2 = True
                                    user_input = transcribe_audio_to_text()
                                    city = user_input.strip()
                                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    climate_finished_2 = True
                                    climate_finished = True
                                    stop(self)
                                else:
                                    climate_finished_3 = False
                                    while not climate_finished_3:
                                        speak("¿No te entendí, ¿quieres saber el clima de otra ciudad?")
                                        user_input = transcribe_audio_to_text()
                                        if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                            speak("¿De qué ciudad?")
                                            climate_finished_3 = True
                                            climate_finished_2 = True
                                            user_input = transcribe_audio_to_text()
                                            city = user_input.strip()
                                        elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                            climate_finished_3 = True
                                            climate_finished_2 = True
                                            climate_finished = True
                                            stop(self)
                                        else:
                                            pass
                        else:
                            speak(f"No se pudo obtener el clima para {city}. A que ciudad te refieres?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                climate_finished = True
                                stop(self)

                # Código de integración con el flujo de la conversación
                elif any(form in user_input for form in ["convertir divisa", "divisa", "divisas", "cambio de moneda", "cambio de divisas", "convertir"]):
                    match = re.search(r"(convertir divisa|divisa|divisas|cambio de moneda|cambio de divisas|convertir)\s+(.*)", user_input.lower())
                    
                    if match and match.group(2):  # Si hay un texto después de la palabra clave
                        user_input = match.group(2).strip()
                        def extraer_divisas(user_input):
                            divisa_entrada, divisa_salida = None, None

                            partes = user_input.split(" a ")  # Asumiendo que el formato es algo como "usd a eur"
                            print(partes)

                            if len(partes) == 2:
                                divisa_entrada = partes[0].strip()
                                divisa_salida = partes[1].strip()
                                
                                divisa_entrada_siglas = None
                                divisa_salida_siglas = None

                                for nombre_divisa, codigo_divisa in divisas.items():
                                    print(f"Comprobando si '{nombre_divisa}' está en '{divisa_entrada}' o '{divisa_salida}'")
                                    
                                    # Si encontramos una divisa en la entrada, asignamos su código
                                    if nombre_divisa in divisa_entrada:
                                        if divisa_entrada_siglas is None:
                                            divisa_entrada_siglas = codigo_divisa
                                            print(f"Divisa de entrada encontrada: {divisa_entrada_siglas}")
                                        else:
                                            pass  # Si ya se ha asignado la divisa de entrada, no hacemos nada

                                    # Si encontramos una divisa en la salida, asignamos su código
                                    if nombre_divisa in divisa_salida:
                                        if divisa_salida_siglas is None:
                                            divisa_salida_siglas = codigo_divisa
                                            print(f"Divisa de salida encontrada: {divisa_salida_siglas}")
                                        else:
                                            pass  # Si ya se ha asignado la divisa de salida, no hacemos nada
                            
                            if divisa_entrada_siglas and divisa_salida_siglas:
                                return divisa_entrada_siglas, divisa_salida_siglas
                            return None, None
                        
                        divisa_entrada_siglas, divisa_salida_siglas = extraer_divisas(user_input)  # Llamamos a la función que extrae las divisas
                        print (divisa_entrada_siglas, divisa_salida_siglas)
                        if divisa_entrada_siglas and divisa_salida_siglas:
                            speak(f"¡Perfecto! ¿Cuál es la cantidad?")
                            user_input = transcribe_audio_to_text()
                            def convertir_a_num(user_input):
                                print("depuracion")
                                if user_input.isnumeric():
                                    return int(user_input)
                                elif user_input.lower() in palabras_a_numeros:
                                    return palabras_a_numeros[user_input.lower()]
                                else:
                                    return None
                            cantidad = convertir_a_num(user_input)
                            if cantidad is not None:
                                cantidad = float(cantidad)
                                def realizar_conversion(divisa_entrada, divisa_salida_siglas, cantidad):
                                    def obtener_tasa_de_cambio(divisa_entrada, divisa_salida_siglas):
                                        load_dotenv()
                                        api_key_exchange = os.getenv('API_KEY_EXCHANGE')
                                        BASE_URL = f"https://v6.exchangerate-api.com/v6/{api_key_exchange}/latest/{divisa_entrada}"
                                        url = BASE_URL  # URL con la divisa base
                                        print(f"Divisa de entrada: {divisa_entrada}")
                                        print(f"Divisa de salida: {divisa_salida_siglas}")
                                        print(url)
                                        try:
                                            response = requests.get(url)
                                            data = response.json()
                                            
                                            if data['result'] == 'success':
                                                tasa = data['conversion_rates'].get(divisa_salida_siglas)
                                                if tasa:
                                                    return tasa
                                                else:
                                                    speak("No se encontró la tasa de cambio para la divisa de salida.")
                                                    return None
                                            else:
                                                speak("Hubo un problema al obtener la tasa de cambio.")
                                                return None
                                        except Exception as e:
                                            speak("Hubo un error al consultar la API de tasas de cambio.")
                                            print(f"Error: {e}")
                                            return None
                                    tasa = obtener_tasa_de_cambio(divisa_entrada, divisa_salida_siglas)
                                    if tasa:
                                        resultado = cantidad * tasa
                                        resultado_formateado = "{:,.2f}".format(resultado).replace(',', ' ').replace('.', ',')
                                        return resultado_formateado
                                    else:
                                        return "Tasa de cambio no disponible."
                                resultado_formateado = realizar_conversion(divisa_entrada_siglas, divisa_salida_siglas, cantidad)
                                speak(f"{cantidad} {divisa_entrada_siglas} son {resultado_formateado} {divisa_salida_siglas}.")
                                speak("¿Cuál es tu siguiente consulta?")
                            else:
                                speak("No entendí la cantidad. Por favor, indícamelo mejor la próxima vez.")
                                speak("¿Cuál es tu siguiente consulta?")
                        else:
                            speak("No pude identificar las divisas que deseas convertir. ¿Puedes repetirlo?")
                    else:
                        speak("¿Qué divisa quieres convertir?")

                elif any(form in user_input for form in ["adivinanza", "adivinanzas", "acertijo", "acertijos"]):
                    try:
                        adivinanza_finished = False
                        while not adivinanza_finished:
                            adivinanza_actual = random.choice(adivinanzas)
                            speak(adivinanza_actual["pregunta"])
                            user_input = transcribe_audio_to_text()
                            if user_input.lower() == adivinanza_actual["respuesta"].lower():
                                speak("¡Correcto, enhorabuena!")
                                time.sleep(1)
                                speak("¿Quieres intentar otra adivinanza?")
                                user_input = transcribe_audio_to_text()
                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    adivinanza_finished = False
                                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    adivinanza_finished = True
                                    stop(self)
                                else:
                                    adivinanza_finished_2 = False
                                    while not adivinanza_finished_2:
                                        speak("¿No te entendí, ¿quieres intentar otra adivinanza?")
                                        user_input = transcribe_audio_to_text()
                                        if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                            adivinanza_finished_2 = True
                                        elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                            adivinanza_finished_2 = True
                                            adivinanza_finished = True
                                            stop(self)
                                        else:
                                            pass
                            else:
                                speak(f"Incorrecto. La respuesta correcta era {adivinanza_actual['respuesta']}.")
                                time.sleep(1)
                                speak("¿Quieres intentar otra adivinanza?")
                                user_input = transcribe_audio_to_text()
                                adivinanza_finished_3 = False
                                while not adivinanza_finished_3:
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        adivinanza_finished_3 = True
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        adivinanza_finished_3 = True
                                        adivinanza_finished = True
                                        stop(self)
                                    else:
                                        adivinanza_finished_4 = False
                                        while not adivinanza_finished_4:
                                            speak("¿No te entendí, ¿quieres intentar otra adivinanza?")
                                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                                adivinanza_finished_4 = True
                                                adivinanza_finished_3 = True
                                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                                adivinanza_finished_4 = True
                                                adivinanza_finished_3 = True
                                                adivinanza_finished = True
                                                stop(self)
                                            else:
                                                pass
                    except Exception as e:
                        speak("Lo siento, no te puedo contar una adivinanza en este momento.")

                elif any(form in user_input for form in ["chiste", "chistes"]):
                    try:
                        chiste_finished = False
                        while not chiste_finished:
                            response = random.choice(chistes)
                            speak(response)
                            time.sleep(0.5)
                            speak("¿Quieres escuchar otro chiste?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                chiste_finished = False
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                chiste_finished = True
                                stop(self)
                            else:
                                chiste_finished_2 = False
                                while not chiste_finished_2:
                                    speak("¿No te entendí, ¿quieres escuchar otro chiste?")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        chiste_finished_2 = True
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        chiste_finished_2 = True
                                        chiste_finished = True
                                        stop(self)
                                    else:
                                        pass
                    except Exception as e:
                        speak("Lo siento, no te puedo contar un chiste en este momento.")

                elif any(form in user_input for form in ["nota de voz", "grabar nota", "grabar nota de voz", "audio", "grabar audio"]):
                    audio_finished = False
                    while not audio_finished:
                        speak("¿Título de la grabación?")
                        user_input = transcribe_audio_to_text()
                        title = user_input
                        speak("Empieza a grabar tu nota de voz. Ya puedes hablar.")
                        recognizer = sr.Recognizer()
                        with sr.Microphone() as source:
                            audio = recognizer.listen(source)

                        documents_path = os.path.join(os.path.expanduser("~"))
                        file_path = os.path.join(documents_path, f"{title}.wav")
                        with open(file_path, "wb") as f:
                            f.write(audio.get_wav_data())
                        speak(f"Nota de voz guardada como {file_path}.")
                        speak ("¿Quieres grabar otra nota de voz?")
                        user_input = transcribe_audio_to_text()
                        audio_finished_2 = False
                        while not audio_finished_2:
                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                audio_finished_2 = True
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                audio_finished_2 = True
                                audio_finished = True
                                stop(self)
                            else:
                                audio_finished_3 = False
                                while not audio_finished_3:
                                    speak("¿No te entendí, ¿quieres grabar otra nota de voz?")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        audio_finished_3 = True
                                        audio_finished_2 = True
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        audio_finished_3 = True
                                        audio_finished_2 = True
                                        audio_finished = True
                                        stop(self)
                                    else:
                                        pass

                elif any(form in user_input for form in ["cara o cruz"]):
                    resultado = random.choice(["Cara", "Cruz"])
                    speak(f"Ha salido {resultado}.")
                    speak("¿Necesitas algo más?")
                    user_input = transcribe_audio_to_text()
                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                        speak("¿Qué más necesitas?")
                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                        stop(self)
                    else:
                        cara_o_cruz_finished = False
                        while not cara_o_cruz_finished:
                            speak("¿No te entendí, ¿Necesitas algo más?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                cara_o_cruz_finished = True
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                cara_o_cruz_finished = True
                                stop(self)
                            else:
                                pass

                elif any(form in user_input for form in ["piedra papel tijeras", "piedra papel tijera"]):
                    playing_piedra_papel_tijeras = True
                    while playing_piedra_papel_tijeras:
                        opciones = ["piedra", "papel", "tijeras"]
                        resultado = random.choice(opciones)
                        speak("Juguemos, a la de tres elige: Piedra, Papel o Tijeras.")
                        time.sleep(0.5)
                        speak("Uno")
                        time.sleep(0.5)
                        speak("Dos")
                        time.sleep(0.5)
                        speak("Tres")
                        user_input = transcribe_audio_to_text()

                        if "tijera" in user_input.lower():
                            user_input = "tijeras"

                        if user_input.lower() in opciones:
                            if user_input.lower() == resultado.lower():
                                speak(f"¡Empate! Yo elegí {resultado}")
                            elif (user_input.lower() == "piedra" and resultado.lower() == "tijeras") or (user_input.lower() == "papel" and resultado.lower() == "piedra") or (user_input.lower() == "tijeras" and resultado.lower() == "papel"):
                                speak(f"¡Ganaste! Yo elegí {resultado}")
                            else:
                                speak(f"¡Perdiste! Yo elegí {resultado}")
                            playing_piedra_papel_tijeras_2 = True
                            while playing_piedra_papel_tijeras_2:
                                speak("¿Quieres jugar otra vez?")
                                user_input = transcribe_audio_to_text()
                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    playing_piedra_papel_tijeras_2 = False
                                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    playing_piedra_papel_tijeras_2 = False
                                    playing_piedra_papel_tijeras = False
                                    stop(self)
                                else:
                                    playing_piedra_papel_tijeras_3 = True
                                    while playing_piedra_papel_tijeras_3:
                                        speak("¿No te entendí, ¿quieres jugar otra vez?")
                                        user_input = transcribe_audio_to_text()
                                        if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                            playing_piedra_papel_tijeras_3 = False
                                            playing_piedra_papel_tijeras_2 = False
                                        elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                            playing_piedra_papel_tijeras_3 = False
                                            playing_piedra_papel_tijeras_2 = False
                                            playing_piedra_papel_tijeras = False
                                            stop(self)
                                        else:
                                            pass
                        else:
                            playing_piedra_papel_tijeras_4 = True
                            while playing_piedra_papel_tijeras_4:
                                speak("No entendí que dijiste. ¿Quieres jugar piedra papel tijeras?")
                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    playing_piedra_papel_tijeras_4 = False
                                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    playing_piedra_papel_tijeras_4 = False
                                    playing_piedra_papel_tijeras = False
                                    stop(self)
                                else:
                                    pass

                elif any(form in user_input for form in ["número oculto", "jugar número oculto", "jugar adivinar número oculto", "adivinar número oculto", "adivinar número"]):
                    numero_oculto = random.randint(1, 100)
                    speak("Voy a pensar en un número del 1 al 100. Adivina cuál es.")
                    intentos = 0
                    numero_oculto_finished = False
                    while not numero_oculto_finished:
                        while intentos <= 9:
                            if intentos < 9:
                                speak(f"Te quedan {10 - intentos} intentos.")
                            else:
                                speak(f"Te queda un intento.")
                            user_input = transcribe_audio_to_text()
                            def convertir_a_numero(user_input):
                                if user_input.isnumeric():
                                    return int(user_input)
                                elif user_input.lower() in palabras_a_numeros:
                                    return palabras_a_numeros[user_input.lower()]
                                else:
                                    return None
                            numero = convertir_a_numero(user_input)
                            if numero is not None:
                                if numero == numero_oculto:
                                    speak("¡Correcto! ¡Has adivinado el número!")
                                    numero_oculto_finished_2 = False
                                    while not numero_oculto_finished_2:
                                        speak("¿Quieres jugar otra vez?")
                                        user_input = transcribe_audio_to_text()
                                        if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                            numero_oculto = random.randint(1, 100)
                                            speak("Voy a pensar en un número del 1 al 100. Adivina cuál es.")
                                            intentos = 0
                                            numero_oculto_finished_2 = True
                                        elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                            numero_oculto_finished_2 = True
                                            numero_oculto_finished = True
                                            stop(self)
                                        else:
                                            numero_oculto_finished_3 = False
                                            while not numero_oculto_finished_3:
                                                speak("¿No te entendí, ¿quieres jugar otra vez?")
                                                user_input = transcribe_audio_to_text()
                                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                                    numero_oculto = random.randint(1, 100)
                                                    speak("Voy a pensar en un número del 1 al 100. Adivina cuál es.")
                                                    intentos = 0
                                                    numero_oculto_finished_3 = True
                                                    numero_oculto_finished_2 = True
                                                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                                    numero_oculto_finished_3 = True
                                                    numero_oculto_finished_2 = True
                                                    numero_oculto_finished = True
                                                    stop(self)
                                                else:
                                                    pass
                                elif numero < 1 or numero > 100:
                                    speak("El número debe estar entre 1 y 100.")
                                elif numero < numero_oculto:
                                    speak(f"El número es mayor que {numero}.")
                                    intentos += 1
                                else:
                                    speak(f"El número es menor que {numero}.")
                                    intentos += 1
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                intentos = 11
                                numero_oculto_finished = True
                                stop(self)
                            else:
                                speak("No entendí. ¿Qué número crees que es?")
                        if intentos == 10:
                            speak(f"Lo siento, no has adivinado el número. El número era {numero_oculto}.")
                            numero_oculto_finished_4 = False
                            while not numero_oculto_finished_4:
                                speak("¿Quieres jugar otra vez?")
                                user_input = transcribe_audio_to_text()
                                if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    numero_oculto = random.randint(1, 100)
                                    speak("Voy a pensar en un número del 1 al 100. Adivina cuál es.")
                                    intentos = 0
                                    numero_oculto_finished_4 = True
                                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    numero_oculto_finished_4 = True
                                    numero_oculto_finished = True
                                    stop(self)
                                else:
                                    numero_oculto_finished_5 = False
                                    while not numero_oculto_finished_5:
                                        speak("¿No te entendí, ¿quieres jugar otra vez?")
                                        user_input = transcribe_audio_to_text()
                                        if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                            numero_oculto = random.randint(1, 100)
                                            speak("Voy a pensar en un número del 1 al 100. Adivina cuál es.")
                                            intentos = 0
                                            numero_oculto_finished_5 = True
                                            numero_oculto_finished_4 = True
                                        elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                            numero_oculto_finished_5 = True
                                            numero_oculto_finished_4 = True
                                            numero_oculto_finished = True
                                            stop(self)
                                        else:
                                            pass

                elif re.search(r'\d+(\.\d+)?\s*[-+*/]\s*\d+(\.\d+)?', user_input):
                    math_finished = False
                    while not math_finished:                        
                        match = re.search(r'\d+(\.\d+)?\s*[-+*/]\s*\d+(\.\d+)?', user_input)
                        if match:
                            expresion = match.group()  # Extraer la expresión encontrada
                            expresion_to_read = expresion.replace("+", "más").replace("-", "menos").replace("*", "por").replace("/", "entre")
                            try:
                                resultado = eval(expresion)  # Evalúa la expresión matemática
                                speak(f"El resultado de {expresion_to_read} es {resultado}")
                                math_finished_2 = False
                                while not math_finished_2:
                                    speak("¿Quieres hacer otra operación matemática?")
                                    user_input = transcribe_audio_to_text()
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        math_finished_2 = True
                                        user_input = transcribe_audio_to_text()
                                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                        math_finished_2 = True
                                        math_finished = True
                                        stop(self)
                                    else:
                                        math_finished_3 = False
                                        while not math_finished_3:
                                            speak("No entendí lo que dijiste. ¿Quieres hacer otra operación matemática?")
                                            user_input = transcribe_audio_to_text()
                                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                                math_finished_3 = True
                                                math_finished_2 = True
                                                user_input = transcribe_audio_to_text()
                                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                                math_finished_3 = True
                                                math_finished_2 = True
                                                math_finished = True
                                                stop(self)
                                            else:
                                                pass
                            except Exception as e:
                                speak("Hubo un error al calcular la expresión.")
                        else:
                            math_finished_4 = False
                            while math_finished_4:
                                speak("No entendí lo que dijiste. ¿Quieres volverlo a intentar?")
                                user_input = transcribe_audio_to_text()
                                if any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                    math_finished = True
                                    math_finished_4 = True
                                    stop(self)
                                elif any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                    math_finished_4 = True
                                    user_input = transcribe_audio_to_text()
                                else:
                                    pass

                elif re.search(r"\bhora\b", user_input.lower()):
                    now = datetime.now()
                    response = f"Son las {now.strftime('%H:%M:%S')}"
                    speak(response)
                    speak("¿Necesitas algo más?")
                    user_input = transcribe_audio_to_text()
                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                        speak("¿Qué más necesitas?")
                    elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                        stop(self)
                    else:
                        hora_finished = False
                        while not hora_finished:
                            speak("¿No te entendí, ¿Necesitas algo más?")
                            user_input = transcribe_audio_to_text()
                            if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                hora_finished = True
                            elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                hora_finished = True
                                stop(self)
                            else:
                                pass

                elif any(form in user_input.lower() for form in ["hola", "buenos días", "buenas tardes", "buenas noches", "buenas"]):
                    response = "¡Hola! ¿Cómo podría ayudarte?"
                    speak(response)

                elif any(user_input.lower().strip() == frase for frases in respuestas_bot.keys() for frase in frases):
                    for frases, respuesta in respuestas_bot.items():
                        if user_input.lower().strip() in frases:
                            speak(respuesta)
                            break

                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                    if "adiós" in user_input.lower():
                        response = "¡Adiós! ¡Que tengas un buen día!"
                        speak(response)
                    stop(self)

                else:
                    response = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
                    speak(response)
        except Exception as e:
            print(f"Error: {e}")
            speak("Hubo un problema al procesar el audio, por favor intenta de nuevo.")
    print("Hilo finalizando...")
    self.started = False
    StopAnimationSignal_Class = StopAnimationSignal.get_instance()
    StopAnimationSignal_Class.stop_animation_signal.emit()