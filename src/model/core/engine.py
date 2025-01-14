import threading
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import webbrowser
import os

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
                if "busca" in user_input.lower():
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
                
                elif "hora" in user_input.lower():
                    now = datetime.now()
                    response = f"La hora actual es {now.strftime('%H:%M:%S')}"
                    speak(response)

                elif any(form in user_input.lower() for form in ["hola", "buenos días", "buenas tardes", "buenas noches", "buenas"]):
                    response = "¡Hola! ¿Cómo podría ayudarte?"
                    speak(response)

                elif any(palabra in user_input.lower() for palabra in palabras_cancelation):
                    if "adiós" in user_input.lower():
                        response = "¡Adiós! ¡Que tengas un buen día!"
                        speak(response)
                    stop(self)

                elif "abre" in user_input.lower():
                    open_finished = False
                    while not open_finished:
                        programa = user_input[5:].lower().strip()  # Obtener el texto después de "abre"
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
                else:
                    response = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
                    speak(response)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
            speak("Hubo un problema al procesar el audio, por favor intenta de nuevo.")