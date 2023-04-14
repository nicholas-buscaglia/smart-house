import wakeword
import whisper
import voice_to_text
import text_to_voice
import sys
import os

# get the directory of the current module (primary directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
# construct the path to the secondary directory
apps_dir = os.path.join(current_dir, 'apps')
# add the secondary directory to the Python path
sys.path.append(apps_dir)
from apps import i_msg
from apps import mail
from apps import weather
from apps import time
from apps import reminders

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
                        'text': i_msg.send_i_msg,
                        'email': mail.send_email,
                        'date': time.get_current_date,
                        'time': time.get_current_time,
                        'weather': weather.get_local_weather,
                        'reminder': reminders.create_reminder
                    }
                    response = keyword_functions[app_keyword](prompt)
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
