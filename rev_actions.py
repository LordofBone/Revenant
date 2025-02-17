# !/user/bin/env python3

import calendar
import time
from dataclasses import dataclass
from time import sleep

import cv2 as cv
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray


@dataclass
class Actions:
    camera = PiCamera()
    camera.framerate = 24
    camera.rotation = 90
    rawCapture = PiRGBArray(camera)

    store_detects: bool = False

    # Toggle function for storing photos under /Captured
    def toggle_store_detects(self):
        self.store_detects = not self.store_detects
        print("Store detections on: {}".format(str(self.store_detects)))

    # Take a picture and show the result
    def snap_pic_and_show(self):
        print("Snapping picture...")
        self.camera.resolution = (640, 480)
        sleep(.5)
        self.camera.capture(self.rawCapture, format="bgr")
        output = self.rawCapture.array
        # Grab current datetime
        ts = calendar.timegm(time.gmtime())
        if self.store_detects:
            filename = 'Captured/{}.jpg'.format(str(ts))
            self.camera.capture(filename)
        cv.imshow('Revenant Vision', output)
        cv.waitKey(0)
        cv.destroyAllWindows()
        self.camera.close()

ActionAccess = Actions()
