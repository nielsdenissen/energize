import pandas as pd
import numpy as np
import yaml
import os
import cv2
from tqdm.auto import tqdm

from FER_models import ConvolutionalNNDropout

def get_training_data(data, channels = 1, resize = None):
    """

    :param data: processed data (pd.DataFrame) as a result of data_prep.py
    :param channels: number of image channels (1 for grayscale images)
    :param resize: Tuple (new_image_size[0], new_image_size[1])
    :return:
        images: np.array of shape (num_samples, image_size[0], image_size[1], channels)
        labels: np.array of shape (num_samples, num_categories)
        labels_map: dictionary which maps the index of 'labels' to a string (emotion)

    """

    images = np.stack(data['pixels'].values)
    images = images.reshape((-1, 48, 48, channels)).astype(np.float32)
    if channels == 1 and resize is not None:
        print("Resizing images.")
        num_images = images.shape[0]
        resized_images = np.zeros([num_images, resize[0], resize[1]]).astype(np.float32)

        for i in tqdm(range(images.shape[0])):
            resized_images[i] = cv2.resize(images[i].squeeze(), (resize[0], resize[1]), interpolation = cv2.INTER_CUBIC)

    labels = pd.get_dummies(data['emotion_energy'])

    labels_map = labels.columns.tolist()
    labels_map = {k:labels_map[k] for k in range(len(labels_map))}

    labels = pd.get_dummies(labels).values

    return images, labels, labels_map


if __name__ == "__main__":


    with open("config.yaml") as ymlfile:
        cfg = yaml.load(ymlfile)

    data = pd.read_pickle(cfg["processed_data_filepath"])

    train_images, train_labels, labels_map = get_training_data(data)

    image_shape = (48, 48)
    channels = 1

    model = ConvolutionalNNDropout(image_shape, channels, labels_map, verbose=True, model_filepath=cfg["model_filepath"])
    model.fit(train_images, train_labels, validation_split=0.1, epochs = 1)
    model.model.save(cfg['model_filepath'])

