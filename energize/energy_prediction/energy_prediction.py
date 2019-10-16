import cv2
import numpy as np
from energize.energy_prediction.read_expressions import ReadExpressions
from energize.energy_prediction.compare_faces import CompareFaces
from energize.energy_prediction.find_faces import FindFaces
from energize.energy_prediction.model.FER_models import ConvolutionalNNDropout

labels_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
model = ConvolutionalNNDropout((48, 48), labels_map, verbose=True, model_filepath="model/model.h5")

read_expressions = ReadExpressions(model=model)
compare_faces = CompareFaces(faces="/Users/nielsdenissen/Downloads/known_faces2.npz", tolerance=0.7)
find_faces = FindFaces(scale=1)

def predict_energy(img):
    image = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), -1)
    locations = find_faces.find_faces(image)
    names = compare_faces.get_names(image=image, locations=locations)
    expressions = read_expressions.get_expressions(image=image, locations=locations)
    out = {"energy":42}
    out['faces'] = [{"name":n, "location":l, "expression":e} for n, l, e in zip(names, locations, expressions)]
    return out
