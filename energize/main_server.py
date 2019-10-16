import base64
import json
import logging
import os
import cv2
import numpy as np

from flask import Flask
from flask_sockets import Sockets
from flask_cors import CORS, cross_origin

import configparser
import argparse

from energize.energy_prediction.find_faces import FindFaces
from energize.energy_prediction.compare_faces import CompareFaces
from energize.energy_prediction.read_expressions import ReadExpressions
from energize.energy_prediction.model.FER_models import ConvolutionalNNDropout

PREDICTOR = lambda x: {"energy": 42}

app = Flask(__name__)
sockets = Sockets(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

HTTP_SERVER_PORT = 5000
HTTP_SERVER_HOST = "0.0.0.0"


@cross_origin(origin="*")
@sockets.route('/media')
def echo(ws):
    app.logger.info("Connection accepted")
    message_count = 0

    # while not ws.closed:
    #     energy = random.randrange(0, 100, 1)
    #     app.logger.info(f"Current energy level: {energy}")
    #     ws.send(json.dumps({"energy":energy}))
    #     time.sleep(5)

    while not ws.closed:
        message = ws.receive()
        if message is None:
            app.logger.info("No message received...")
            continue

        app.logger.info("Message received!")

        # Cut out the image header in start
        if "," in message:
            message = message.split(',')[1]
        
        file_like = base64.b64decode(message)
        #result = energy_prediction.predict_energy(file_like)

        image = cv2.imdecode(np.fromstring(file_like, dtype=np.uint8), -1)
        result = PREDICTOR(image)
        print(result)
        ws.send(json.dumps(result))

        #with open(f"./pics_received/image{message_count}.jpg", 'wb') as f:
        #    f.write(file_like)

        message_count += 1

    app.logger.info("Connection closed. Received a total of {} messages".format(message_count))



def build_predictor(scale, known_faces, tolerance, model):
    """Builds the energy predictor function from given
    configurables

    :param scale: scale image down or up before face extraction
        down scaling speeds up but looses pixels
    :param known_faces: location of a file with known faces
        Either a npz file with pre-trained embeddings, or a directory
        with subdirectories of images per persons.
        Note that pre-trained embeddings is much faster
    :param tolerance: maximum distance between embeddings to consider
        a match in face comparison
    :param model: facial expression recognition model
    :return: function that returns an energy json given an image
    """
    find_faces = FindFaces(scale=scale)
    compare_faces = CompareFaces(faces=known_faces, tolerance=tolerance)
    read_expressions = ReadExpressions(model=model)
    def predict(image):
        locations = find_faces.find_faces(image)
        names = compare_faces.get_names(image, locations)
        faces = read_expressions.get_faces(image, locations)
        expressions = read_expressions.get_expressions(faces)
        expressions = expressions + ["Unknown"]*(len(locations) - len(expressions))
        prediction = {}
        prediction['energy'] = 42
        prediction['faces'] = [{"name": n, "location": l, "expression": e} for n, l, e in zip(names, locations, expressions)]
        prediction['image size'] = (image.shape[0], image.shape[1])
        return prediction
    return predict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, nargs=1, default="config.ini", help="Config file")
    args = parser.parse_args()

    # ----- Read config file -----
    config_file = args.file
    if os.path.isfile(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
    else:
        raise RuntimeError("No config file parsed")

    scale = float(config['DEFAULT'].get("scale", 1.))
    known_faces = config['DEFAULT'].get("known faces")
    tolerance = float(config['DEFAULT'].get("tolerance", 0.6))
    model = config['DEFAULT'].get("model")
    labels_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    model = ConvolutionalNNDropout((48, 48), labels_map, verbose=True,
                                   model_filepath=model)

    PREDICTOR = build_predictor(scale=scale, known_faces=known_faces, tolerance=tolerance, model=model)

    app.logger.setLevel(logging.DEBUG)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer((HTTP_SERVER_HOST, HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    app.logger.info(f"Server listening on: http://{HTTP_SERVER_HOST}:{HTTP_SERVER_PORT}")
    server.serve_forever()
