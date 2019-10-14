from energize.capture_video.capture_video import CaptureVideo
from energize.energy_prediction.energy_prediction import PredictEnergy
from energize.report_energy_levels.report_energy_level import ReportEnergyLevel
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Energize')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    args = vars(parser.parse_args())
    verbose = args['v']

    re = ReportEnergyLevel()
    pe = PredictEnergy(output_fnc=re.do_shizzle, scale=1)
    cv = CaptureVideo(output_fnc=pe.do_shizzle, source='camera')

    cv.do_shizzle()