import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)

        print("User:", text)

        return text

    except:
        return None


def speak(text):
    engine.say(text)
    engine.runAndWait()