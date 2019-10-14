import cv2
from PIL import ImageGrab
import numpy as np
from energize.utils.utils import Stub

class CaptureVideo:

    def __init__(self, receiver=None):
        self._receiver = receiver if receiver is not None else Stub()

    def do_shizzle(self):
        while True:
            im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
            self._receiver.do_shizzle(im)