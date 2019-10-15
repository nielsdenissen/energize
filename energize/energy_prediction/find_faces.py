import cv2
import face_recognition
from energize.pipeline.pipeline import PipelineModule


class FindFaces(PipelineModule):

    def __init__(self, next=None, scale=1):
        super().__init__(next)
        self.scale = 1

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image')
        scaled_image = cv2.resize(image, (0, 0), fx=self.scale, fy=self.scale)[:, :, ::-1]
        scaled_locations = face_recognition.face_locations(scaled_image)
        locations = [list(int(l / self.scale) for l in loc) for loc in scaled_locations]
        self.next.do_shizzle(image=image, locations=locations)