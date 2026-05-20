import speech_recognition as sr
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Speed
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Tina: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None

    except sr.RequestError:
        speak("Speech service is unavailable.")
        return None