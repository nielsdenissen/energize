
import numpy as np

class EnergyPrediction:
    def __init__(self):
        pass

    def predict_energy(self, image, locations, names, faces, expressions):
        return np.mean(expressions)
