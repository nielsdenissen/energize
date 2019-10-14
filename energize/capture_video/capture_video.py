from energize.energy_prediction import energy_prediction
from energize.utils import utils
import datetime
import cv2
from PIL import ImageGrab
import numpy as np
import json


def capture_video(conn):
    print("-- RUNNING Capture Video")
    while True:
        im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
        conn(im)


if __name__ == "__main__":
    capture_video(energy_prediction.main)
