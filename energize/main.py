from energize.capture_video.capture_video import CaptureVideo
from energize.energy_prediction.energy_prediction import PredictEnergy
import argparse


class Stub:
    def do_shizzle(self, *args, **kwargs):
        print("====== Args ======")
        for a in args:
            print(type(a))
        print("===== KwArgs =====")
        for k, v in kwargs:
            print(k, type(v))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Energize')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    args = vars(parser.parse_args())
    verbose = args['v']


    pe = PredictEnergy(receiver=None)
    cv = CaptureVideo(receiver=pe)

    cv.do_shizzle()