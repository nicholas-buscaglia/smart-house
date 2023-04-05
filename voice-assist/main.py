import wakeword
import whisper
import voice_to_text
import text_to_voice
# Required Environment Variables:
# PICO_KEY              # wakeword          # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
# OPENAI_API_KEY        # whisper           # https://platform.openai.com/account/api-keys
# ASSEMBLYAI_API_KEY    # voice_to_text     # https://www.assemblyai.com/


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
