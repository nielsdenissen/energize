class PipelineModule:

    def __init__(self, next=None):
        if next is not None and not isinstance(next, PipelineModule):
            raise ValueError("Expected argument next to be a PipelineModule or None")
        else:
            self.next = next

    def do_shizzle(self, **kwargs):
        pass



import cv2
from PIL import ImageGrab
import numpy as np

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

class ReportEnergyLevel(PipelineModule):

    def __init__(self):
        super().__init__(None)
        cv2.namedWindow("Energize", cv2.WINDOW_NORMAL)

    def do_shizzle(self, image=None, locations=[], names=[], expressions=[]):
        names = names + ["Unknown"]*(len(locations) - len(names))
        expressions = expressions + ["Unknown"]*(len(locations) - len(expressions))
        face_info = list(zip(locations, names, expressions))

        if image is not None:
            for loc, name, expr in face_info:
                top, right, bottom, left = loc
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow("Energize", image)
        cv2.waitKey(1)

    def cleanup(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def __del__(self):
        self.cleanup()

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Energize')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    parser.add_argument("--known_faces", nargs='?', type=str, default="")
    args = vars(parser.parse_args())
    verbose = args['v']
    known_faces = args['known_faces']

    repenelv = ReportEnergyLevel()
    #readexpr = ReadExpressions(output_fnc=repenelv.do_shizzle)
    #compface = CompareFaces(output_fnc=readexpr.do_shizzle, faces=known_faces, tolerance=0.7)
    #findface = FindFaces(output_fnc=compface.do_shizzle, scale=1.)
    capvideo = CaptureVideo(next=repenelv, source='camera')

    capvideo.do_shizzle()