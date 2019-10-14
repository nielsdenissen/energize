import cv2
import face_recognition

class FindFaces:

    def __init__(self, output_fnc=None, scale=1):
        self._output_fnc = output_fnc
        self.scale = 1

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image')
        scaled_image = cv2.resize(image, (0, 0), fx=self.scale, fy=self.scale)[:, :, ::-1]
        scaled_locations = face_recognition.face_locations(scaled_image)
        locations = [list(int(l / self.scale) for l in loc) for loc in scaled_locations]
        self._output_fnc(image=image, locations=locations)