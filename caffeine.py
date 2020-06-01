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
duration = 0  # duration before enable screensaver
chosen_duration = 0  # user picked duration


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


# Monitor keyboard events
def monitor_key(key):
    global ss_flag, duration, chosen_duration
    # Lock on screensaver exit
    if ss_flag == 1:
        ctypes.windll.user32.LockWorkStation()
        ss_flag = 0
    # Reset duration on keyboard key
    duration = int(chosen_duration) * 60


# Monitor mouse events
def monitor_mouse(move):
    global ss_flag, duration, chosen_duration
    # Lock on screensaver exit
    if ss_flag == 1:
        ctypes.windll.user32.LockWorkStation()
        ss_flag = 0
    # Reset duration on mouse move
    duration = int(chosen_duration) * 60


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

    # Select duration
    # default duration 15 min
    print('Duration before screensaver active (min): ')
    chosen_duration = input('>>>')
    if not chosen_duration:
        chosen_duration = 15  # because F15 frequency < duration, duration = infinity

    # Start monitoring
    keyboard.add_hotkey(ss_hotkey, ss_ena, args=[chosen_ss], suppress=True)  # add screensaver hotkey
    x = threading.Thread(target=caffeine_thread, daemon=True)
    x.start()  # start caffeine thread
    keyboard.hook(monitor_key, suppress=False)
    mouse.hook(monitor_mouse)

    # Monitor duration
    duration = int(chosen_duration) * 60
    while duration > 0:
        time.sleep(1)
        print('duration = {}'.format(duration))
        duration -= 1
        if duration == 0:
            ss_ena(chosen_ss)  # enable screensaver
            duration = int(chosen_duration) * 60
