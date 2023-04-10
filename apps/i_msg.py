import os
import time
from pynput.keyboard import Key, Controller


def send_i_msg(who, what, when=None):
    # Open Messages app
    os.system("open -a Messages")
    time.sleep(3)

    # Create new message thread with Peter
    keyboard = Controller()
    keyboard.press(Key.cmd)
    keyboard.press('n')
    keyboard.release('n')
    keyboard.release(Key.cmd)
    time.sleep(2)
    keyboard.type(who)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # Type and send message
    def send_message():
        keyboard.type(f"{what} -sent from Nick's AI Assistant")
        time.sleep(2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    if when:
        # Calculate time to wait
        scheduled_time = time.strptime(when, '%I:%M %p')
        current_time = time.localtime()
        if scheduled_time < current_time:
            scheduled_time = time.struct_time((current_time.tm_year, current_time.tm_mon, current_time.tm_mday + 1,
                                               scheduled_time.tm_hour, scheduled_time.tm_min, 0, 0, 0, 0))
        wait_time = time.mktime(scheduled_time) - time.mktime(current_time)

        # Wait until scheduled time
        time.sleep(wait_time)

        # Send message
        send_message()

    else:
        # Send message immediately
        send_message()
