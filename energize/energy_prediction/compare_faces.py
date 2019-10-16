import cv2
import face_recognition
import os
import numpy as np
from energize.pipeline.pipeline import PipelineModule
from face_recognition.api import _raw_face_landmarks, face_encoder

def face_encodings_large(face_image, known_face_locations=None, num_jitters=1):
    """
    Copy of face_recognition.face_encodings with a large model

    Given an image, return the 128-dimension face encoding for each face in the image.
    :param face_image: The image that contains one or more faces
    :param known_face_locations: Optional - the bounding boxes of each face if you already know them.
    :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)
    :return: A list of 128-dimensional face encodings (one for each face in the image)
    """
    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model="large")
    return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]

def encode_faces(directory, npoints='large', num_jitters=1):
    if os.path.isdir(directory):
        known_faces = {}
        maximum_number_of_pictures = 0
        for loc1 in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, loc1)):
                embeddings = []
                for loc2 in os.listdir(os.path.join(directory, loc1)):
                    if os.path.isfile(os.path.join(directory, loc1, loc2)):
                        try:
                            face = face_recognition.load_image_file(os.path.join(directory, loc1, loc2))
                            if npoints == 'large':
                                embedding = face_encodings_large(face, num_jitters=num_jitters)[0]
                            else:
                                embedding = face_recognition.face_encodings(face, num_jitters=num_jitters)[0]
                            embeddings.append(embedding)
                        except:
                            pass
                if len(embeddings) > 0:
                    known_faces[loc1] = embeddings
                    if len(embeddings) > maximum_number_of_pictures:
                        maximum_number_of_pictures = len(embeddings)
        names = [""] * len(known_faces)
        embeddings = np.infty * np.ones((len(known_faces), maximum_number_of_pictures, 128), dtype=float)
        for i, (name, lst) in enumerate(known_faces.items()):
            names[i] = name
            embeddings[i, :len(lst), :] = np.array(lst)
        if len(names) > 0:
            return names, embeddings
        else:
            raise RuntimeError("No faces encoded")
    else:
        raise ValueError("{} not a directory".format(directory))

class CompareFaces(PipelineModule):

    def __init__(self, next=None, faces=None, tolerance=0.6, npoints='large', num_jitters=1):
        super().__init__(next)
        self.tolerance = tolerance
        self.num_jitters = num_jitters
        if os.path.isdir(faces):
            self.npoints = npoints
            self.names, self.embeddings = encode_faces(faces, npoints=npoints, num_jitters=num_jitters)
        else:
            faces = np.load(faces)
            self.npoints = faces['npoints'] if 'npoints' in faces else 'small'
            self.names = faces['names']
            self.embeddings = faces['embeddings']
        print("Read {} names. Embeddings with shape {} in {} format".format(self.names, self.embeddings.shape, self.npoints))
        print(np.sum(np.isnan(self.embeddings)), "NaNs")

    def do_shizzle(self, **kwargs):
        image = kwargs.pop('image', None)
        locations = kwargs.pop('locations', [])
        if image is not None and len(locations) > 0:
            names = self.get_names(image, locations, self.num_jitters)
        else:
            names = []
        self.next.do_shizzle(image=image, locations=locations, names=names)

    def get_names(self, image, locations, num_jitters=1):
        names = ["Unknown"] * len(locations)
        if len(locations) > 0:
            try:
                if self.npoints == 'large':
                    faces = np.array(face_encodings_large(image, locations, num_jitters))
                else:
                    faces = np.array(face_recognition.face_encodings(image, locations, num_jitters))
                distances = np.linalg.norm(faces[:, np.newaxis, np.newaxis, :] - self.embeddings[np.newaxis, :, :, :], axis=3)
                distances[np.where(np.isnan(distances))] = np.infty
                #print(np.sum(np.isnan(self.embeddings)), self.embeddings.shape)
                #print(np.sum(np.isnan(faces)), faces.shape)
                #print(np.sum(np.isinf(distances)), distances.shape)
                #print(faces.shape, self.embeddings.shape, distances.shape)
                #print(distances, np.min(distances))
                idx = np.unravel_index(np.argmin(distances), distances.shape)
                while distances[idx] < self.tolerance:
                    names[idx[0]] = self.names[idx[1]]
                    distances[idx[0], :, :] = np.infty
                    distances[:, idx[1], :] = np.infty
                    idx = np.unravel_index(np.argmin(distances), distances.shape)
            except Exception as e:
                print(f"EXCEPTION in compare_faces: {e}")
        return names
