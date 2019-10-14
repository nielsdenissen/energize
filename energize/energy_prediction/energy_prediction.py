import cv2
import face_recognition

class PredictEnergy:

    def __init__(self, output_fnc=None, scale=1):
        self._output_fnc = output_fnc
        self.scale = 1

    def find_faces(self, image):
        scaled_image = cv2.resize(image, (0, 0), fx=self.scale, fy=self.scale)[:, :, ::-1]
        scaled_locations = face_recognition.face_locations(scaled_image)
        locations = [list(int(l / self.scale) for l in loc) for loc in scaled_locations]
        return locations

    def compare_faces(self, image, locations):

        return []

    def read_expressions(self, image):

        return []

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image')
        locations = self.find_faces(image)
        names = self.compare_faces(image, locations)
        expressions = self.read_expressions(image)
        self._output_fnc(image=image, locations=locations, names=names, expressions=expressions)




