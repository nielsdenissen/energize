import cv2
from PIL import ImageGrab
import numpy as np

class CaptureVideo:

    def __init__(self):
        pass

    def do_shizzl(self, receiver):
        if not hasattr(receiver, "do_shizzle") or not hasattr(receiver.do_shizzle, "__call__"):
            raise RuntimeError("Receiver {} not callable with do_shizzle method".format(receiver.__name__))
        while True:
            im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
            receiver.do_shizzl(im)