import wakeword
import whisper
import voice_to_text
import text_to_voice


def voice_assist():
    while True:
        wakeword.poppy()
        convo = 'new'
        text_to_voice.speak("Greetings human...how may I assist you?")

        while True:
            prompt = voice_to_text.get_prompt_string()
            if prompt != '':
                response = whisper.chat(prompt, convo)
                text_to_voice.speak(response)
                convo = 'continue'
            else:
                break


if __name__ == '__main__':
    voice_assist()
