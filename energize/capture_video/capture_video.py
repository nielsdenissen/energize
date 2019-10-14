import datetime
from energize.energy_prediction import energy_prediction


def main():
    print("-- RUNNING Capture Video")
    # TODO: replace empty_image with actual image (representation by opencv probably)
    energy_prediction.main("empty_image", datetime.datetime.now())


if __name__ == "__main__":
    main()
