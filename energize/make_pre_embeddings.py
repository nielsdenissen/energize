from energize.energy_prediction.compare_faces import CompareFaces
import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pre-embedding')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    parser.add_argument("--known_faces", nargs=1, type=str)
    parser.add_argument("-o", nargs=1, type=str)
    args = vars(parser.parse_args())
    verbose = args['v']
    known_faces = args['known_faces'][0]
    outfile = args['o'][0]

    cf = CompareFaces(output_fnc=None, faces=known_faces, tolerance=None)
    print(cf.names)
    print(cf.embeddings.shape)
    np.savez(outfile, names=np.array(cf.names), embeddings=cf.embeddings)
