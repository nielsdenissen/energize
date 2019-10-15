import base64
import json
import logging
import random
import time

from flask import Flask
from flask_sockets import Sockets
from flask_cors import CORS, cross_origin


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

    while not ws.closed:
        energy = random.randrange(0, 100, 1)
        app.logger.info(f"Current energy level: {energy}")
        ws.send(json.dumps({"energy":energy}))
        time.sleep(5)

    # while not ws.closed:
    #     message = ws.receive()
    #     if message is None:
    #         app.logger.info("No message received...")
    #         continue

    #     app.logger.info(f"Message received!")
        
    #     # Cut out the base64 image info in start
    #     file_like = base64.b64decode(message[22:])

    #     with open(f"./pics_received/image{message_count}.jpg", 'wb') as f:
    #         f.write(file_like)

    #     message_count += 1

    app.logger.info("Connection closed. Received a total of {} messages".format(message_count))


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer((HTTP_SERVER_HOST, HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    app.logger.info(f"Server listening on: http://{HTTP_SERVER_HOST}:{HTTP_SERVER_PORT}")
    server.serve_forever()
