import cv2
import face_recognition
import os
import numpy as np
from energize.pipeline.pipeline import PipelineModule


class CompareFaces(PipelineModule):

    def __init__(self, next=None, faces=None, tolerance=0.6):
        super().__init__(next)
        self.tolerance = tolerance
        if os.path.isdir(faces):
            known_faces = {}
            maximum_number_of_pictures = 0
            for loc1 in os.listdir(faces):
                if os.path.isdir(os.path.join(faces, loc1)):
                    embeddings = []
                    for loc2 in os.listdir(os.path.join(faces, loc1)):
                        if os.path.isfile(os.path.join(faces, loc1, loc2)):
                            try:
                                face = face_recognition.load_image_file(os.path.join(faces, loc1, loc2))
                                embedding = face_recognition.face_encodings(face, num_jitters=1)[0]
                                embeddings.append(embedding)
                            except:
                                pass
                    if len(embeddings) > 0:
                        known_faces[loc1] = embeddings
                        if len(embeddings) > maximum_number_of_pictures:
                            maximum_number_of_pictures = len(embeddings)
            self.names = [""] * len(known_faces)
            self.embeddings = np.NaN * np.ones((len(known_faces), maximum_number_of_pictures, 128), dtype=float)
            for i, (name, lst) in enumerate(known_faces.items()):
                self.names[i] = name
                self.embeddings[i, :len(lst), :] = np.array(lst)
        else:
            faces = np.load(faces)
            self.names = faces['names']
            self.embeddings = faces['embeddings']
        print("Read {} names. Embeddings with shape {}".format(self.names, self.embeddings.shape))

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image', None)
        locations = kwargs.pop('locations', [])
        if image is not None and len(locations) > 0:
            names = self.get_names(image, locations)
        else:
            names = []
        self.next.do_shizzle(image=image, locations=locations, names=names)

    def get_names(self, image, locations):
        try:
            faces = np.array(face_recognition.face_encodings(image, locations, num_jitters=1))
            distances = np.linalg.norm(faces[:, np.newaxis, np.newaxis, :] - self.embeddings[np.newaxis, :, :, :], axis=3)
            names = ["Unknown"] * len(locations)
            idx = np.unravel_index(np.nanargmin(distances), distances.shape)
            while distances[idx] < self.tolerance:
                names[idx[0]] = self.names[idx[1]]
                distances[idx[0], :, :] = np.NaN
                distances[:, idx[1], :] = np.NaN
                idx = np.unravel_index(np.nanargmin(distances), distances.shape)
        except ValueError:
            pass
        return names