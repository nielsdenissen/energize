
import numpy as np

class EnergyPrediction:
    def __init__(self):
        pass

    def predict_energy(self, image, locations, names, faces, expressions):
        if len(expressions) == 0:
            return 0
        else:
            # scale to [-1;1]
            return np.mean(expressions) / 2
