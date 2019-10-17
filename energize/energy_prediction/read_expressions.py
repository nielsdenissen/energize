import cv2
import numpy as np
import random
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

    def get_faces(self, image, face_locations):
        faces = []
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]
            faces.append(face_image)
        return faces

    def get_expressions(self, faces):
        energies = ["Unknown"]*len(faces)
        if len(faces) > 0:
            try:
                gray_faces = [cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) for face in faces]
                expressions = self.model.predict_from_faces(gray_faces)
                energies = self._compute_newtonian_energy(expressions)
            except Exception as e:
                print(f"EXCEPTION in get_expressions: {e}")
        return energies

    def _compute_newtonian_energy(self, expressions):
        energies = []

        for expression in expressions:
            newtonian_constant = random.choice([-1, 0, 1])
            energy = max(expression) * (np.argmax(expression) - 1) + newtonian_constant
            energies.append(int(round(energy, 0)))

        return energies
