import datetime
from energize.energy_prediction import energy_prediction
import cv2
from PIL import ImageGrab
import numpy as np


def capture_video():
    print("-- RUNNING Capture Video")
    while True:
        im = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)
        energy_prediction.main(im, datetime.datetime.now())


if __name__ == "__main__":
    capture_video()
