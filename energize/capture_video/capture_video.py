import datetime
from energize.energy_prediction import energy_prediction


def main():
    print("-- RUNNING Capture Video")
    energy_prediction.main(datetime.datetime.now(), "empty_image")


if __name__ == "__main__":
    main()
