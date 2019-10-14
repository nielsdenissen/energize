import cv2
from PIL import ImageGrab
import numpy as np
from energize.utils.utils import Stub, timer

class CaptureVideo:

    def __init__(self, receiver=None, source='screen'):
        self._receiver = receiver if receiver is not None else Stub()
        self.source = source

    def do_shizzle(self):
        if self.source == 'camera':
            source = cv2.VideoCapture(0)
            while True:
                _, im = source.read()
                self._receiver.do_shizzle(im)
        elif self.source == 'screen':
            while True:
                im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
                self._receiver.do_shizzle(im)
        else:
            raise NotImplementedError("Reading from file not yet supported")