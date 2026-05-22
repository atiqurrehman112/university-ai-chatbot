from voice_assistant import listen, speak

text = listen()

if text:
    speak("You said " + text)
else:
    speak("Sorry I could not hear you")