import pvporcupine
import pyaudio
import struct
import os
access_key = os.getenv("PICO_KEY")

# Get the directory path of the current Python file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the full path of the custom_wakewords directory
custom_wakewords_path = os.path.join(dir_path, 'custom_wakewords')

# Check the system type and set the keyword file path accordingly
system_type = os.uname().sysname
if system_type == 'Darwin':  # Mac
    keyword_path = os.path.join(custom_wakewords_path, 'Hey-Poppy_en_mac_v2_1_0.ppn')
elif system_type == 'Linux':  # Linux
    keyword_path = os.path.join(custom_wakewords_path, 'Hey-Poppy_en_linux_v2_1_0.ppn')
elif system_type == 'Linux':  # Raspberry Pi
    keyword_path = os.path.join(custom_wakewords_path, 'Hey-Poppy_en_raspberry-pi_v2_1_0.ppn')
else:
    raise ValueError(f"System type {system_type} not supported.")


def poppy():
    print('listening...')
    porcupine = None
    pa = None
    audio_stream = None
    try:
        # Available stock keywords
        # pvporcupine.KEYWORDS = {'grapefruit', 'picovoice', 'blueberry', 'hey google', 'hey siri', 'hey barista',
        # 'bumblebee', 'ok google', 'grasshopper', 'computer', 'americano', 'pico clock', 'alexa', 'porcupine',
        # 'jarvis', 'terminator'}
        # porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis", "grasshopper"])
        porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[keyword_path])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Hotword Detected\n")
                break

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
