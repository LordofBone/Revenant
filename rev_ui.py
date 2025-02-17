# !/user/bin/env python3

# This is for user control of the Revenant

import qprompt

from rev_actions import ActionAccess
from rev_console_logger import ConsoleAccess
from rev_movements import MovementAccess

# setup menu library
menu = qprompt.Menu()


# Toggles the logging of debug printouts
def enable_logging():
    ConsoleAccess.console_print_enable = not ConsoleAccess.console_print_enable
    print("Console Logging: {}".format(str(ConsoleAccess.console_print_enable)))


# Function that asks for an integer from the user to move the mouth a number of times
def mouth_mover():
    times = qprompt.ask_int()
    MovementAccess.chatter_mouth(times)


# Menu setup and display
try:
    menu.add("1", "Open Mouth", MovementAccess.open_mouth)
    menu.add("2", "Close Mouth", MovementAccess.close_mouth)
    menu.add("3", "Chatter Mouth", mouth_mover)
    menu.add("4", "Take Picture", ActionAccess.snap_pic_and_show)
    menu.add("5", "Store Cam Pics Toggle", ActionAccess.toggle_store_detects)
    menu.add("6", "Red Eye Toggle", MovementAccess.red_eye)
    menu.add("7", "Blue Eye Toggle", MovementAccess.blue_eye)
    menu.add("8", "Fire Rockets", MovementAccess.rocket_launch)
    menu.add("9", "Toggle Console Printing", enable_logging)
    menu.main(loop=True)
except KeyboardInterrupt:
    exit()
