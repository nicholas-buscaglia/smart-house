import wakeword
import whisper
import voice_to_text
import text_to_voice


def voice_assist():

    while True:

        wakeword.poppy()
        text_to_voice.speak("Greetings human...how may I assist you?")

        prompt = voice_to_text.get_prompt_string()
        if prompt != '':
            print(f'You:\n{prompt}')
            response = whisper.chat(prompt)
            text_to_voice.speak(response)


if __name__ == '__main__':
    voice_assist()
