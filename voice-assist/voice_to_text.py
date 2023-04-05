import websockets
import pyaudio
import asyncio
import base64
import json
import os
auth_key = os.getenv("ASSEMBLYAI_API_KEY")

# Assign Globals
kill_count, kill, result = 0, False, ''
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')
for i in range(num_devices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    if device_info['maxInputChannels'] > 0:
        if 'Snowball' in device_info['name']:
            input_device_index = i
            break


def get_prompt_string():
    global kill_count, kill, result
    kill_count, kill, result = 0, False, ''
    # p = pyaudio.PyAudio()
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    # starts recording
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
        input_device_index=input_device_index
    )
    # the AssemblyAI endpoint to hit
    URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

    async def send_receive():
        # print(f'Connecting websocket to url ${URL}')
        async with websockets.connect(
                URL,
                extra_headers=(("Authorization", auth_key),),
                ping_interval=5,
                ping_timeout=20
        ) as _ws:
            await asyncio.sleep(0.1)
            # print("Receiving SessionBegins ...")
            session_begins = await _ws.recv()
            print(session_begins)
            # print("Sending messages ...")

            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedOK:
                        # print("Connection closed")
                        break
                    except Exception as e:
                        print(e)
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)

                return True

            async def receive():
                global kill_count, kill, result
                print('\nlistening...')

                while True:
                    try:
                        result_str = await _ws.recv()
                        result_str = json.loads(result_str)['text'].lower()
                        if result_str == '' or result_str.isspace():
                            kill_count += 1
                            # Assign arbitrary termination period
                            if kill_count >= 11:
                                print('silence kill')
                                kill = True
                                break
                                # sys.exit(0)
                        else:
                            if result_str[-1] == '.':
                                result += result_str
                                if 'end prompt' in result_str or 'end of prompt' in result_str or 'and prompt' in result_str:
                                    result = result.replace('end of prompt', '').replace('end prompt', '').replace('and prompt', '')
                                    print('prompt kill')
                                    # print(f'result: {result}')
                                    kill = True
                                    break
                                    # sys.exit(0)
                    except websockets.exceptions.ConnectionClosedError as e:
                        # print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        # print(e)
                        assert False, "Not a websocket 4008 error"
                await _ws.close()  # Close the WebSocket connection

                return False

            send_task = asyncio.create_task(send())
            receive_task = asyncio.create_task(receive())
            done, pending = await asyncio.wait(
                [send_task, receive_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
    asyncio.run(send_receive())

    if result != '':
        print(f'You: {result}')

    return result
