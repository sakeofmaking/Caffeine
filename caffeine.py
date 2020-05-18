#!/usr/bin/env python3

"""
Caffeine

Description: User sets how long before screensaver enabled. During screensaver, monitors mouse and keyboard events.
If event, exit screensaver (happens automatically). Lock computer. Hotkey enables screensaver

Author: Nic La
Last modified: May 2020
"""


import time
import threading
import keyboard
import mouse
import subprocess
import os
import ctypes


# Initialize Variables
ss_hotkey = 'alt + space'  # hotkey to enable screensaver
ss_flag = 0  # 1 if screensaver active
frequency = 5  # frequency of F15


# Press F15 every duration
# F15 does interrupt screensaver
def caffeine_thread():
    global ss_flag, frequency
    while ss_flag == 0:
        time.sleep(frequency * 60)
        if ss_flag == 0:
            keyboard.send('F15', do_press=True, do_release=True)
            print('F15')


# Enable screensaver
def ss_ena(ss):
    global ss_flag
    ss_flag = 1
    time.sleep(1)
    subprocess.call(r'C:\WINDOWS\System32\\' + ss)
    keyboard.hook(monitor_key)
    mouse.hook(monitor_mouse)


def monitor_key(key):
    global ss_flag
    ctypes.windll.user32.LockWorkStation()
    keyboard.unhook_all()
    ss_flag = 0


def monitor_mouse(move):
    global ss_flag
    ctypes.windll.user32.LockWorkStation()
    mouse.unhook_all()
    ss_flag = 0


# Main
if __name__ == "__main__":
    # Provide list of screensavers available
    ss_list = []
    ss_count = 1
    print('Select a screensaver:')
    for file in os.listdir(r'C:\WINDOWS\System32\\'):
        if file.endswith(".scr"):
            print('[{}] {}'.format(ss_count, file))
            ss_count += 1
            ss_list.append(file)

    # Select screen saver
    user_input = input('>>>')
    try:
        chosen_ss = ss_list[int(user_input) - 1]
    except ValueError:
        chosen_ss = 'Fliqlo.scr'
    keyboard.add_hotkey(ss_hotkey, ss_ena, args=[chosen_ss], suppress=True)  # add screensaver hotkey
    x = threading.Thread(target=caffeine_thread, daemon=True)
    x.start()  # start caffeine thread

    # Select duration
    # default duration 15 min
    print('Duration before screensaver active (min): ')
    user_input = input('>>>')
    if not user_input:
        user_input = 15
    # TODO: Add while loop that checks periodically (each min), updating time_elapsed, to see if duration of no
    # TODO: activity is exceeded. If exceeded, enable screensaver. If activity, reset duration



