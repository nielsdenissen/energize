from energize.capture_video.capture_video import CaptureVideo
from energize.energy_prediction.energy_prediction import PredictEnergy
from energize.report_energy_levels.report_energy_level import ReportEnergyLevel
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

    re = ReportEnergyLevel(receiver=None)
    pe = PredictEnergy(receiver=re)
    cv = CaptureVideo(receiver=pe)

    cv.do_shizzle()