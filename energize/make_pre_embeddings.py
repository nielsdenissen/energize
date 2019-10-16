from energize.energy_prediction.compare_faces import encode_faces
import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pre-embedding')
    parser.add_argument("-v", action="store_true", help="Set verbosity")
    parser.add_argument("--known_faces", nargs=1, type=str)
    parser.add_argument("-o", nargs=1, type=str)
    parser.add_argument("-p", nargs='?', type=str, default='large')
    parser.add_argument("-j", nargs='?', type=int, default=1)
    args = vars(parser.parse_args())
    verbose = args['v']
    known_faces = args['known_faces'][0]
    outfile = args['o'][0]
    npoints = args['p']
    num_jitters = args['j']

    names, embeddings = encode_faces(known_faces, npoints=npoints, num_jitters=num_jitters)
    print(names)
    print(embeddings.shape)
    np.savez(outfile, npoints=npoints, num_jitters=num_jitters, names=np.array(names), embeddings=embeddings)
