import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

# Función para hablar al inicio
def speak(text):
    engine.say(text)
    engine.runAndWait()

def transcribe_audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")

        recognizer.timeout = 10
        recognizer.energy_threshold = 500

        try:
            audio = recognizer.listen(source, timeout=5)  # Añadir un timeout para evitar quedarse esperando demasiado
            text = recognizer.recognize_sphinx(audio, language="es")  # Usar pocketsphinx para el reconocimiento offline
            print(f"Texto detectado: {text}")
            return text
        except sr.UnknownValueError:
            raise ValueError("No se pudo entender lo que dijiste.")  # Lanzar un error si no se entiende el audio
        except sr.RequestError as e:
            raise ConnectionError(f"Error con el servicio de reconocimiento de voz: {e}")  # Lanzar un error si hay un problema
        except Exception as e:
            raise e  # Para capturar cualquier otro tipo de error que pueda ocurrir

def generate_response(prompt):
    # Procesar la entrada con if-elif
    response = ""
    if "hola" in prompt.lower():
        response = "¡Hola! ¿Cómo puedo ayudarte?"
    elif "hora" in prompt.lower():
        now = datetime.now()
        response = f"La hora actual es {now.strftime('%H:%M:%S')}"
    elif "adiós" in prompt.lower():
        response = "¡Adiós! ¡Que tengas un buen día!"
    elif "busca" in prompt.lower():
        search_query = prompt.lower().replace("busca ", "")
        search_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(search_url)  # Abrir la búsqueda en el navegador
        response = f"Buscando resultados para: {search_query}"
    else:
        response = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
    return response

if __name__ == "__main__":
    # Hablar al inicio
    speak("Hola, estoy listo para escucharte.")
    
    while True:
        try:
            user_input = transcribe_audio_to_text()
            if user_input:
                response = generate_response(user_input)
                response = ""
                print(f"IA: {response}")
                speak(response)  # Responder también con voz
                if "adiós" in user_input.lower():
                    break
        except Exception as e:
            print(f"Error: {e}")
            speak("Hubo un problema al procesar el audio, por favor intenta de nuevo.")
