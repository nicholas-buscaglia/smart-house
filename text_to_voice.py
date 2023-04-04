import pyttsx3

# 11 (hawking)
# 17 (australian female) winner
# 26 (femaale)
# 32 (male)
# 33 (femaale)


def speak(something):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # Get list of available voices
    engine.setProperty('voice', voices[17].id)  # Set voice to Karen's voice

    # Set a slower speaking rate
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-25)

    engine.say(something)

    engine.runAndWait()


# import pyttsx3
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice, voice.id)
#     engine.setProperty('voice', voice.id)
#     engine.say("Hello World!")
#     engine.runAndWait()
#     engine.stop()

    # Daniel
    # Fred (hawking)
    # Karen
    # Alex

