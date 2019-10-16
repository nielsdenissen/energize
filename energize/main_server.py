import base64
import json
import logging
import os
import cv2
import numpy as np

from flask import Flask
from flask_sockets import Sockets
from flask_cors import CORS, cross_origin

import argparse

from energize.energy_prediction.build_predictor import build_predictor

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

        app.logger.info(f"Message received: {message_count}")

        try:
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

        except Exception as e:
            app.logger.error("ERROR: %s", e)
            continue
        
        message_count += 1
        

    app.logger.info("Connection closed. Received a total of {} messages".format(message_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, nargs=1, default="config.ini", help="Config file")
    args = parser.parse_args()

    PREDICTOR = build_predictor(args.file)

    app.logger.setLevel(logging.DEBUG)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer((HTTP_SERVER_HOST, HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    app.logger.info(f"Server listening on: http://{HTTP_SERVER_HOST}:{HTTP_SERVER_PORT}")
    server.serve_forever()
