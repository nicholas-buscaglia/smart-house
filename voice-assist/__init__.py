main_module = __import__('voice-assist.main', fromlist=['*'])
wakeword_module = __import__('voice-assist.wakeword', fromlist=['*'])
whisper_module = __import__('voice-assist.whisper', fromlist=['*'])
voice_to_text_module = __import__('voice-assist.voice-to-text', fromlist=['*'])
text_to_voice_module = __import__('voice-assist.text-to-voice', fromlist=['*'])

main = main_module.main
jarvis = wakeword_module.jarvis
chat = whisper_module.chat
get_prompt_string = voice_to_text_module.get_prompt_string
speak = text_to_voice_module.speak

if __name__ == '__main__':
    main()
