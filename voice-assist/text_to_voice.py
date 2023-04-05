import pyttsx3


def speak(something):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # Get list of available voices
    # 11 (hawking)
    # 17 (australian female) winner
    # 26 (femaale)
    # 32 (male)
    # 33 (femaale)
    engine.setProperty('voice', voices[17].id)  # Set voice to Karen's voice
    # Set a slower speaking rate
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-25)

    engine.say(something)
    engine.runAndWait()
