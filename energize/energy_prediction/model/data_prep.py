import numpy as np
import pandas as pd
import yaml

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

if __name__ == "__main__":

    with open("config.yaml") as ymlfile:
        cfg = yaml.load(ymlfile)

    data = pd.read_csv(cfg["fer2013_csv_filepath"])
    data = data_prep(data)
    data.to_pickle(cfg["processed_data_filepath"])


