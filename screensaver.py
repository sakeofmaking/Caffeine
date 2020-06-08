"""
Screen Saver

Description: My work computer has screen saver disabled. I don't know why. I do know I can replicate it
myself. User selects screen saver and duration before screen saver active. If no mouse events, screen
saver is enabled. Upon screen saver exit, the computer is locked

Author: Nic La
Last modified: Jun 2020
"""


import os
import subprocess
import pyautogui
import time
import ctypes


ss_flag = False  # True if screen saver enabled
lock_flag = False  # True if program is to lock computer
duration = 1  # duration of inactivity before screen saver active


# enable screen saver function
def ss_ena(ss):
    global ss_flag
    ss_flag = True
    # subprocess.call(r'C:\WINDOWS\System32\\' + ss)
    print(ss)


if __name__ == '__main__':
    # Provide list of screen savers available
    ss_list = []
    ss_count = 1
    print('Select a screen saver:')
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
        chosen_ss = ss_list[1]

    # Select duration
    print('Select duration in min:')
    duration = input('>>>')
    if not duration.isnumeric():
        duration = 5

    # Monitor duration of inactivity
    while True:
        duration_sec = int(duration) * 60
        while duration_sec > 0:
            initial_x, initial_y = pyautogui.position()
            time.sleep(1)
            new_x, new_y = pyautogui.position()
            if not ss_flag and not lock_flag and (new_x == initial_x or new_y == initial_y):
                duration_sec -= 1
            elif ss_flag and not lock_flag and new_x != initial_x and new_y != initial_y:
                ss_flag = False
                lock_flag = True
                ctypes.windll.user32.LockWorkStation()
            else:
                duration_sec = int(duration) * 60
                lock_flag = False
            print(duration_sec)
        ss_ena(chosen_ss)


