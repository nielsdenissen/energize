from energize.capture_video.capture_video import capture_video
from energize.energy_prediction import energy_prediction
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Energize')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    args = vars(parser.parse_args())
    verbose = args['v']


    capture_video(energy_prediction.main)