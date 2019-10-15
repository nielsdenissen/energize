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

    report_energy_level = ReportEnergyLevel()
    #read_expressions = ReadExpressions(next=report_energy_level)
    compare_faces = CompareFaces(next=report_energy_level, faces=known_faces, tolerance=0.7)
    find_faces = FindFaces(next=compare_faces, scale=1.)
    capture_video = CaptureVideo(next=find_faces, source='camera')

    capture_video.do_shizzle()