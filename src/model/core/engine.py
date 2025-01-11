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
            speak("Lo siento, no entendí lo que dijiste. Por favor, intenta de nuevo.")
        except sr.RequestError as e:
            print(f"Error con el servicio de reconocimiento: {e}")
            speak("Hubo un problema con el servicio de reconocimiento.")
        return ""

def start(self):
    self._stop_event = threading.Event()
    # Hablar al inicio
    speak("Hola, estoy lista para atenderte. Pregúntame lo que necesites.")
    
    while not self._stop_event.is_set():
        try:
            user_input = transcribe_audio_to_text()
            if user_input:
                    response = ""
                    if "hola" in user_input.lower():
                        response = "¡Hola! ¿Cómo podría ayudarte?"
                        speak(response)
                    elif "hora" in user_input.lower():
                        now = datetime.now()
                        response = f"La hora actual es {now.strftime('%H:%M:%S')}"
                        speak(response)
                    elif "adiós" in user_input.lower():
                        response = "¡Adiós! ¡Que tengas un buen día!"
                        speak(response)
                    elif "busca" in user_input.lower():
                        search_query = user_input.lower().replace("busca ", "")
                        search_url = f"https://www.google.com/search?q={search_query}"
                        webbrowser.open(search_url)
                        response = f"Buscando {search_query} en Google."
                        speak(response)
                        time.sleep(2)
                        speak("¿Es esto lo que buscabas?")
                        user_input = transcribe_audio_to_text()
                        if user_input == "sí":
                            break
                        else:
                            speak("Entonces que es lo que quieres buscar?")
                    else:
                        response = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
                        speak(response)
                    if "adiós" in user_input.lower():
                        break
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
            speak("Hubo un problema al procesar el audio, por favor intenta de nuevo.")

def stop(self):
    self._stop_event.set()