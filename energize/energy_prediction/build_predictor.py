from energize.energy_prediction.energy_prediction import EnergyPrediction
from energize.energy_prediction.find_faces import FindFaces
from energize.energy_prediction.compare_faces import CompareFaces
from energize.energy_prediction.read_expressions import ReadExpressions
#from energize.energy_prediction.energy_prediction import predict_energy
from energize.energy_prediction.model.FER_models import ConvolutionalNNDropout
import configparser
import os
import numpy as np


def build_predictor(config_file):
    """Builds the energy predictor function from given config file

    :return: function that returns an energy json given an image
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    scale = float(config['DEFAULT'].get("scale", 1.))
    known_faces = config['DEFAULT'].get("known faces")
    tolerance = float(config['DEFAULT'].get("tolerance", 0.6))
    num_jitters = int(config['DEFAULT'].get("num_jitters", 1))
    model = config['DEFAULT'].get("model")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(dir_path, model)

    print(model_path)

    labels_map = {0: -1, 1: 0, 2: 1}
    model = ConvolutionalNNDropout((48, 48), labels_map, verbose=True, model_filepath=model_path)

    find_faces = FindFaces(scale=scale)
    compare_faces = CompareFaces(faces=known_faces, tolerance=tolerance)
    read_expressions = ReadExpressions(model=model)
    energy_prediction = EnergyPrediction()

    def predict(image):
        locations = find_faces.find_faces(image)
        names = compare_faces.get_names(image, locations, num_jitters)
        faces = read_expressions.get_faces(image, locations)
        expressions = read_expressions.get_expressions(faces)
        expressions = expressions + ["Unknown"]*(len(locations) - len(expressions))

        out = {'energy': energy_prediction.predict_energy(image, locations, names, faces, expressions)}

        if 'image_size' not in out:
            out['image_size'] = (image.shape[0], image.shape[1])
        if 'faces' not in out:
            out['faces'] = [{"name": n, "location": l, "expression": e} for n, l, e in zip(names, locations, expressions)]
        if 'energy' not in out:
            out['energy'] = 42

        return out
    return predict
