import base64
from websocket import create_connection

ws = create_connection("ws://localhost:5000/media")
with open("./test/test.jpg", 'rb') as f:
    image = f.read()
    to_send = base64.b64encode(image)
    print(to_send[0:30])
    ws.send(to_send)

result =  ws.recv()
print("Received '%s'" % result)
ws.close()

