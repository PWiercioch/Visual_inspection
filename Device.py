import cv2
from copy import copy
import sys


# Abstarct class
class Device:
    def __init__(self, factor):
        self.shrink_factor = factor

    def display(self):
        # TODO - not here
        self.img = cv2.resize(self.img, (0, 0), fx=self.shrink_factor, fy=self.shrink_factor)
        cv2.imshow('Visual window', self.img)

    def close():
        cv2.destroyAllWindows()
        print('Quitting program')
        # sys.exit()


class Webcam(Device):
    def __init__(self, factor):
        Device.__init__(self, factor)
        self.video = cv2.VideoCapture(0)
        self.wait_time = 1

    def get_image(self):
        check, self.img = self.video.read()
        return self.img

    def close_condition(self, key):
        return key == ord('q')

    def close(self):
        self.video.release()
        Device.close(self)


class Smartphone(Webcam):
    def __init__(self, factor, camera_addr):
        Webcam.__init__(self, factor)
        self.video.open(camera_addr)


class Image(Device):
    def __init__(self, factor, path):
        Device.__init__(self, factor)
        self._original = cv2.imread(path, cv2.IMREAD_COLOR)
        self.wait_time = 0

    def get_image(self):
        self.img = self._original.copy()
        return self.img

    def close_condition(self, key):
        return True
