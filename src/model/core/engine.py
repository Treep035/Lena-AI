import pyaudio
import wave
import json
import pyttsx3
from vosk import Model, KaldiRecognizer
from datetime import datetime

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

# Función para hablar al inicio
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Cargar el modelo de Vosk (asegúrate de tener el modelo descargado en tu máquina)
model = Model("C:/Users/treep/OneDrive/Escritorio/MP13/Lena AI/src/model/core/vosk-model-es-0.42")  # Reemplaza con la ruta a tu modelo
recognizer = KaldiRecognizer(model, 16000)

def transcribe_audio_to_text():
    # Abrir el micrófono para capturar audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4000)
    print("Escuchando...")
    
    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            text = result_json.get("text", "")
            if text:
                print(f"Texto detectado: {text}")
                return text

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
    else:
        response = "Lo siento, no entendí eso. ¿Puedes intentar de nuevo?"
    return response

if __name__ == "__main__":
    # Hablar al inicio
    speak("Hola, estoy listo para escucharte.")
    print("si")
    
    user_input = transcribe_audio_to_text()
    if user_input:
        response = generate_response(user_input)
        print(f"IA: {response}")
        speak(response)  # Responder también con voz
