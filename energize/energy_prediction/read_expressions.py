import cv2
from energize.pipeline.pipeline import PipelineModule

class ReadExpressions(PipelineModule):

    def __init__(self, next=None, model=None):
        super().__init__(next)
        self.model = model

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image', None)
        locations = kwargs.pop('locations', [])
        names = kwargs.pop('names', [])
        if image is not None and len(locations) > 0:
            expressions = self.get_expressions(image, locations)
        else:
            expressions = []
        self.next.do_shizzle(image=image, locations=locations, names=names, expressions=expressions)

    def get_expressions(self, image, locations):
        faces = self._get_faces(image, locations)
        gray_faces = [cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) for face in faces]
        return self.model.predict_from_faces(gray_faces)

    def _get_faces(self, image, face_locations):
        faces = []
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            faces.append(face_image)
        return faces
