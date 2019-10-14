import cv2
import face_recognition

class ReadExpressions:

    def __init__(self, output_fnc=None):
        self._output_fnc = output_fnc

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image', None)
        locations = kwargs.pop('locations', [])
        names = kwargs.pop('names', [])
        expressions = []
        self._output_fnc(image=image, locations=locations, names=names, expressions=expressions)