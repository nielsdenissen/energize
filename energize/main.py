from energize.capture_video.capture_video import CaptureVideo
from energize.energy_prediction.find_faces import FindFaces
from energize.energy_prediction.compare_faces import CompareFaces
from energize.energy_prediction.model.FER_models import ConvolutionalNNDropout
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

<<<<<<< HEAD
    # TODO save the full model somewhere, with the attributes
    labels_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    model = ConvolutionalNNDropout((48, 48), labels_map, verbose=True, model_filepath="energize/energize_prediction/model/model.h5")

    report_energy_level = ReportEnergyLevel()
    read_expressions = ReadExpressions(next=report_energy_level, model=model)
    compare_faces = CompareFaces(next=report_energy_level, faces=known_faces, tolerance=0.7)
    find_faces = FindFaces(next=read_expressions, scale=1.)
    capture_video = CaptureVideo(next=find_faces, source='camera')

=======
    report_energy_level = ReportEnergyLevel()
    read_expressions = ReadExpressions(next=report_energy_level)
    compare_faces = CompareFaces(next=report_energy_level, faces=known_faces, tolerance=0.7)
    find_faces = FindFaces(next=read_expressions, scale=1.)
    capture_video = CaptureVideo(next=find_faces, source='camera')

>>>>>>> 5efeba4... Add meeting start notification
    capture_video.do_shizzle()