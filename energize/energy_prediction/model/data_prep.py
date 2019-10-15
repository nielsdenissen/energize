import numpy as np
import pandas as pd
import yaml
from tqdm.auto import tqdm
import cv2

def data_prep(data):
    """

    :param data: data downloaded from Kaggle FER competition. it is a pandas dataframe with the following columns:
        'emotion': Integer label from 0-6. 0 = Angry, 1 = Disgust, 2 = Fear, 3 = Happy, 4 = Sad, 5 = Surprise, 6 = Neutral
        'pixels': a string containing the pixel values (separated by a whitespace)
        'Usage': Indicating whether the dataset belogns to train/test
    :return: modified data, where every row of 'pixels' now contains a numpy array of integers (pixels).
        Additionally, it contains an extra column 'emotion_energy', which indicates whether an emotion is either negative, neutral
        or positive.
    """
    data['pixels'] = data['pixels'].apply(lambda x: np.array(x.split()).astype(int))

    emotion_map = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
    label_conversion = {0: "Negative", 1: "Negative", 2: "Negative", 3: "Positive", 4: "Negative", 5: "Positive",
                        6: "Neutral"}

    data['emotion_energy'] = data['emotion'].map(label_conversion)
    data['emotion'] = data['emotion'].map(emotion_map)

    return data


def get_training_data(data, target_size = None, convert_to_RGB = False):
    """

    :param data: processed data (pd.DataFrame) as a result of data_prep.py
    :param channels: number of image channels (1 for grayscale images)
    :param resize: Tuple (new_image_size[0], new_image_size[1])
    :param convert_to_RGB:Boolean. If True, we convert the grayscale image to RGB by making 3 copies of the gray image.
    :return:
        images: np.array of shape (num_samples, image_size[0], image_size[1], channels)
        labels: np.array of shape (num_samples, num_categories)
        labels_map: dictionary which maps the index of 'labels' to a string (emotion)

    """

    images = np.stack(data['pixels'].values)
    images = images.reshape((-1, 48, 48, 1)).astype(np.float32)
    if target_size is not None:
        print("Resizing images.")
        num_images = images.shape[0]
        resized_images = np.zeros([num_images, target_size[0], target_size[1]]).astype(np.float32)

        for i in tqdm(range(images.shape[0])):
            resized_images[i] = cv2.resize(images[i].squeeze(), (target_size[0], target_size[1]), interpolation = cv2.INTER_CUBIC)
        images = resized_images

    if convert_to_RGB:
        images = np.repeat(images, 3, -1)

    labels = pd.get_dummies(data['emotion_energy'])

    labels_map = labels.columns.tolist()
    labels_map = {k:labels_map[k] for k in range(len(labels_map))}

    labels = pd.get_dummies(labels).values

    return images, labels, labels_map

if __name__ == "__main__":

    with open("config.yaml") as ymlfile:
        cfg = yaml.load(ymlfile)

    data = pd.read_csv(cfg["fer2013_csv_filepath"])
    data = data_prep(data)
    data.to_pickle(cfg["processed_data_filepath"])


