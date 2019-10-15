import pandas as pd
import numpy as np
import yaml
import os
import cv2
from tqdm.auto import tqdm

from energize.energy_prediction.model.FER_models import TransferLearningNN
from energize.energy_prediction.model.data_prep import get_training_data




if __name__ == "__main__":


    with open("config.yaml") as ymlfile:
        cfg = yaml.load(ymlfile)

    data = pd.read_pickle(cfg["processed_data_filepath"])

    train_images, train_labels, labels_map = get_training_data(data, convert_to_RGB=True)
    image_shape = (48, 48)
    channels = 1

    # train_images = train_images[:100]
    # train_labels = train_labels[:100]

    model = TransferLearningNN(image_shape, emotion_map = labels_map, verbose=True, model_filepath=cfg["transfer_learning_model_filepath"])
    model.fit(train_images, train_labels, validation_split=0.1, epochs = 1)
    model.model.save(cfg['transfer_learning_model_filepath'])

