import cv2
from PIL import ImageGrab
import numpy as np
from energize.pipeline.pipeline import PipelineModule

class CaptureVideo(PipelineModule):

    def __init__(self, next=None, source='screen'):
        super().__init__(next)
        self.source = source

    def do_shizzle(self):
        if self.source == 'camera':
            source = cv2.VideoCapture(0)
            while True:
                _, im = source.read()
                self.next.do_shizzle(image=im)
        elif self.source == 'screen':
            while True:
                im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
                self.next.do_shizzle(image=im)
        else:
            raise NotImplementedError("Reading from file not yet supported")