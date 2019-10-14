from energize.utils.utils import Stub
import cv2
import face_recognition

class PredictEnergy:

    def __init__(self, receiver=None, scale=1):
        self._receiver = receiver if receiver is not None else Stub()
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

    def do_shizzle(self, image):
        locations = self.find_faces(image)
        names = self.compare_faces(image, locations)
        expressions = self.read_expressions(image)
        self._receiver.do_shizzle(image=image,
                                  locations=locations,
                                  names=names,
                                  expressions=expressions)




