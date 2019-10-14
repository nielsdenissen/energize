import cv2
from PIL import ImageGrab
import numpy as np

class CaptureVideo:

    def __init__(self, output_fnc=None, source='screen'):
        self._output_fnc = output_fnc
        self.source = source

    def do_shizzle(self):
        if self._output_fnc is None:
            raise ValueError("output_fnc cannot be None")
        if self.source == 'camera':
            source = cv2.VideoCapture(0)
            while True:
                _, im = source.read()
                self._output_fnc(image=im)
        elif self.source == 'screen':
            while True:
                im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
                self._output_fnc(image=im)
        else:
            raise NotImplementedError("Reading from file not yet supported")