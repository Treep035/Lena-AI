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
        recognizer.energy_threshold = 4000
        recognizer.dynamic_energy_adjustment = True
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)  # Ajustar para ruido ambiental
        try:
            audio = recognizer.listen(source)  # Capturar el audio
            # Convertir el audio a texto usando Google Web Speech API
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f"Texto detectado: {text}")
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            speak("Lo siento, no entendí lo que dijiste.")
        except sr.RequestError as e:
            print(f"Error con el servicio de reconocimiento: {e}")
            speak("Hubo un problema con el servicio de reconocimiento.")
        return ""

def stop(self):
    self._stop_event.set()
    self.started = False

def start(self):
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
            {"pregunta": "Cuanto más grande es, menos se ve. ¿Qué es?", "respuesta": ("La oscuridad", "oscuridad")},
            {"pregunta": "No es ni humano ni animal, pero tiene corazón. ¿Qué es?", "respuesta": "La alcachofa"},
            {"pregunta": "Soy redondo y siempre estoy en el cielo, pero nunca me caigo. ¿Qué soy?", "respuesta": "El sol"}
        ]


    self._stop_event = threading.Event()
    # Hablar al inicio
    if not self.already_started:
        speak("Hola, estoy lista para atenderte. Pregúntame lo que necesites.")
    else:
        speak("¿En qué puedo ayudarte ahora?")
    while not self._stop_event.is_set():
        try:
            user_input = transcribe_audio_to_text()
            if user_input:
                response = ""

                if any(form in user_input.lower() for form in ["reproduce", "musica", "cancion", "canciones", "escuchar", "pon", "ponme", "poner"]):
                    speak("¿Qué canción o artista quieres escuchar?")
                    user_input = transcribe_audio_to_text()
                    search_query = user_input.lower().replace("reproduce ", "").replace("música de ", "").replace("musica de ", "")
                    search_url = f"https://www.youtube.com/results?search_query={search_query}"
                    webbrowser.open(search_url)
                    response = f"Reproduciendo música de {search_query} en YouTube."
                    speak(response)

                elif "busca" in user_input.lower():
                    search_finished = False
                    while not search_finished:
                        search_query = user_input.lower().replace("busca ", "")
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
                
                elif "abre" in user_input.lower():
                    open_finished = False
                    while not open_finished:
                        programa = user_input.lower().replace("abre ", "")  # Obtener el texto después de "abre"
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

                elif any(form in user_input.lower() for form in ["explica", "que es", "quien es", "definicion de", "definicion", "definir","que significa"]):
                    wikipedia_finished = False
                    while not wikipedia_finished:
                        consulta = re.sub(r"(explica|que es|quien es|definicion de|definicion|definir|que significa)", "", user_input, flags=re.IGNORECASE).strip()
                        try:
                            wikipedia.set_lang("es")  # Establece el idioma a español
                            # Busca el término en Wikipedia
                            resultados = wikipedia.search(consulta)
                            if resultados:
                                # Obtén el resumen del primer resultado
                                resumen = wikipedia.summary(resultados[0], sentences=2)  # Resumen de 3 frases
                                resumen_limpio = re.sub(r'\[\d+\]', '', resumen)
                                speak(f"Segun Wikipedia: {resumen_limpio}")
                                time.sleep(1)
                                speak("¿Tienes alguna consulta más?")
                                user_input = transcribe_audio_to_text()
                                while not wikipedia_finished_2:
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        wikipedia_finished_2 = True
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
                                while not wikipedia_finished_4:
                                    if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                        wikipedia_finished_4 = True
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

                elif re.search(r'clima\s+(?:de|en)?\s*(\w+)', user_input.lower()):
                    climate_finished = False
                    while not climate_finished:
                        match = re.search(r'clima\s+(?:de|en)?\s*(\w+)', user_input.lower())
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
                                    climate_finished_2 = True
                                    user_input = transcribe_audio_to_text()
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
                                            climate_finished_3 = True
                                            climate_finished_2 = True
                                            user_input = transcribe_audio_to_text()
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

                elif any(form in user_input for form in ["adivinanza", "adivinanzas", "acertijo", "acertijos"]):
                    try:
                        adivinanza_finished = False
                        while not adivinanza_finished:
                            adivinanza_actual = random.choice(adivinanzas)
                            speak(adivinanza_actual["pregunta"])
                            user_input = transcribe_audio_to_text()
                            if user_input.lower() == adivinanza_actual["respuesta"].lower():
                                speak("¡Correcto! ¿Quieres intentar otra adivinanza?")
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
                                        if any(palabra in user_input.lower() for palabra in palabras_afirmation):
                                            adivinanza_finished_2 = True
                                        elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                                            adivinanza_finished_2 = True
                                            adivinanza_finished = True
                                            stop(self)
                                        else:
                                            pass
                            else:
                                speak(f"Incorrecto. La respuesta correcta era {adivinanza_actual['respuesta']} ¿Quieres intentar otra adivinanza?")
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
                        speak("Lo siento, no pude encontrar una adivinanza en este momento.")

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
                        speak("¿Qué quieres grabar en la nota de voz?")
                        user_input = transcribe_audio_to_text()
                        documents_path = os.path.join(os.path.expanduser("~"))
                        file_path = os.path.join(documents_path, "nota_de_voz.mp3")
                        with open(file_path, "wb") as f:
                            f.write(user_input.get_wav_data())
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

                elif any(form in user_input for form in ["piedra papel tijeras"]):
                    playing_piedra_papel_tijeras = True
                    while playing_piedra_papel_tijeras:
                        opciones = ["piedra", "papel", "tijeras"]
                        resultado = random.choice(opciones)
                        speak("A la de tres elige: Piedra, Papel o Tijeras.")
                        time.sleep(0.5)
                        speak("Uno")
                        time.sleep(0.5)
                        speak("Dos")
                        time.sleep(0.5)
                        speak("Tres")
                        user_input = transcribe_audio_to_text()
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

                if re.search(r"\bhora\b", user_input.lower()):
                    now = datetime.now()
                    response = f"Son las {now.strftime('%H:%M:%S')}"
                    speak(response)

                elif any(form in user_input.lower() for form in ["hola", "buenos días", "buenas tardes", "buenas noches", "buenas"]):
                    response = "¡Hola! ¿Cómo podría ayudarte?"
                    speak(response)

                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                    if "adiós" in user_input.lower():
                        response = "¡Adiós! ¡Que tengas un buen día!"
                        speak(response)
                    stop(self)

                else:
                    response = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
                    speak(response)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
            speak("Hubo un problema al procesar el audio, por favor intenta de nuevo.")