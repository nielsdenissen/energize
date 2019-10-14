from energize.capture_video.capture_video import CaptureVideo
from energize.energy_prediction.find_faces import FindFaces
from energize.energy_prediction.compare_faces import CompareFaces
from energize.energy_prediction.read_expressions import ReadExpressions
from energize.report_energy_levels.report_energy_level import ReportEnergyLevel
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Energize')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    parser.add_argument("--known_faces", nargs='?', type=str, default="")
    args = vars(parser.parse_args())
    verbose = args['v']
    known_faces = args['known_faces']

    repenelv = ReportEnergyLevel()
    readexpr = ReadExpressions(output_fnc=repenelv.do_shizzle)
    compface = CompareFaces(output_fnc=readexpr.do_shizzle, faces=known_faces, tolerance=0.6)
    findface = FindFaces(output_fnc=compface.do_shizzle, scale=1.)
    capvideo = CaptureVideo(output_fnc=findface.do_shizzle, source='camera')

    capvideo.do_shizzle()