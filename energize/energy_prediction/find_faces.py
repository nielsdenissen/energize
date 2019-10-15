import cv2
import face_recognition
from energize.pipeline.pipeline import PipelineModule
import numpy as np


#class FindFaces:
#
#    def __init__(self, output_fnc=None, scale=1):
#        self._output_fnc = output_fnc
#        self.scale = 1
#
#    def do_shizzle(self, **kwargs):
#        image = kwargs.pop('image')
#        scaled_image = cv2.resize(image, (0, 0), fx=self.scale, fy=self.scale)[:, :, ::-1]
#        scaled_locations = face_recognition.face_locations(scaled_image)
#        locations = [list(int(l / self.scale) for l in loc) for loc in scaled_locations]
#        self._output_fnc(image=image, locations=locations)

class FindFaces(PipelineModule):

    def __init__(self, next=None):
        super().__init__(next)
        self.scale = 1

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image')
        #TODO: Check if image is 8bit gray
        if image.max() <= 1 :
            # Ugly way to check if image is not in right format
            image = (image*255).astype('uint8')

        image = image.astype('uint8')
        locations = face_recognition.face_locations(image)
        faces = []
        for face_location in locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            faces.append(face_image)

        self.next.do_shizzle(faces=faces)

        return faces

