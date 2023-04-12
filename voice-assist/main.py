import threading
import wakeword
import whisper
import voice_to_text
import text_to_voice
import apps
import os
# Required Environment Variables:
# PICO_KEY              # wakeword          # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
# OPENAI_API_KEY        # whisper           # https://platform.openai.com/account/api-keys
# ASSEMBLYAI_API_KEY    # voice_to_text     # https://www.assemblyai.com/


def stock_apps(input_string):
    keywords = ['text', 'email', 'weather', 'date', 'time', 'reminder']
    for keyword in keywords:
        if keyword in input_string:
            return keyword
    return False


def voice_assist():
    while True:
        wakeword.poppy()
        convo = 'new'
        text_to_voice.speak("Greetings human...how may I assist you?")

        while True:
            prompt = voice_to_text.get_prompt_string()
            if prompt != '':
                app_keyword = stock_apps(prompt)
                if app_keyword:
                    keyword_functions = {
                        'text': apps.i_msg.send_i_msg,
                        'email': apps.mail.send_email,
                        'weather': apps.weather.get_local_weather,
                        'time': apps.time.get_current_time,
                        'date': apps.time.get_current_date,
                        'reminder': apps.reminders.create_reminder
                    }
                    response = keyword_functions[app_keyword]()
                else:
                    response = whisper.chat(prompt, convo)
                    convo = 'continue'
                text_to_voice.speak(response)
            else:
                break


if __name__ == '__main__':
    try:
        voice_assist()
    except Exception as e:
        print(str(e))
        text_to_voice.speak("An error occurred. Please check something and try again.")
