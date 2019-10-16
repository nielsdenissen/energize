import base64
from websocket import create_connection
import cv2

source = cv2.VideoCapture(0)
ws = create_connection("ws://localhost:5000/media")

for _ in range(10):
    ret, image = source.read()
    # to_send = base64.b64encode(image)
    to_send = base64.b64encode(cv2.imencode('.jpg', image)[1])
    ws.send(to_send)
    result = ws.recv()
    print("Received '%s'" % result)

ws.close()
source.close()

