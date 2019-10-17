import pandas as pd
import numpy as np
import yaml
import os
import cv2
from tqdm.auto import tqdm

from energize.energy_prediction.model.FER_models import ConvolutionalNNDropout
from energize.energy_prediction.model.data_prep import get_training_data




if __name__ == "__main__":


    with open("config.yaml") as ymlfile:
        cfg = yaml.load(ymlfile)

    data = pd.read_pickle(cfg["processed_data_filepath"])

    train_images, train_labels, labels_map, class_weights = get_training_data(data)
    print(train_images.shape)
    image_shape = (48, 48)
    channels = 1

    model = ConvolutionalNNDropout(image_shape, labels_map, verbose=True, model_filepath=cfg["model_filepath"])
    model.fit(train_images, train_labels, validation_split=0.1, epochs = 20, class_weights = class_weights)
    model.model.save(cfg['model_filepath'])