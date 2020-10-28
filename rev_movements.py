# !/user/bin/env python3

# This is where movements are called and sent to serial writes to go to the rev low-level systems (Arduino)
# All movements and low level actions are handled here

from dataclasses import dataclass
from threading import Timer
from time import sleep

from rev_serial_interfacing import SerialAccess


@dataclass
class Movement:
    # The moving bool is set for a certain time after a movement command and when the lower-level systems are moving
    # the rev (to prevent multiple conflicting move calls at once)
    moving: bool = False

    # Call for opening the mouth servo
    def open_mouth(self):
        if not self.moving:
            SerialAccess.write_serial("open_mouth")
            self.movement_lock()

    # Call for closing the mouth servo
    def close_mouth(self):
        if not self.moving:
            SerialAccess.write_serial("close_mouth")
            self.movement_lock()

    # Call for moving the mouth servo a set number of times
    def chatter_mouth(self, chat_times):
        for i in range(chat_times):
            if not self.moving:
                SerialAccess.write_serial("close_mouth")
                sleep(.5)
                SerialAccess.write_serial("open_mouth")
                # self.movement_lock()
                sleep(.5)

    # Toggle the Red LED
    def red_eye(self):
        SerialAccess.write_serial("red_eye_toggle")

    # Toggle the Blue LED
    def blue_eye(self):
        SerialAccess.write_serial("blue_eye_toggle")

    # Activate the 'rocket launcher' RGB LED ring
    def rocket_launch(self):
        SerialAccess.write_serial("fire_shoulder_rocket")

    # Locks movement for 3 seconds, preventing conflicting multiple movement calls
    def movement_lock(self):
        self.moving = True
        # will call the movement unlock function after 3 seconds, preventing 'double' movement commands from happening
        t = Timer(3.0, self.movement_unlock)
        t.start()

    # Unlocks movements
    def movement_unlock(self):
        self.moving = False


# Instantiate the movement class so that other modules can import and use
MovementAccess = Movement()
