import json
import numpy as np
import time

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def timer(dt, rprec=100):
    """Generator that yields every dt seconds

    Loops until at least dt seconds has passed since the last yield
    Sleeps every loop for dt/rprec seconds; releases the Global Interpreter Lock (GIL)
    for concurrent threads

    :param dt: Minimum number of seconds before next yield
    :param rprec: Relative precision of the number of seconds
        A higher value is more precise but more CPU intensive
    """
    dt = float(dt)
    sleep_length = dt / float(rprec)
    last_frame_time = time.time()
    while True:
        current_frame_time = time.time()
        while current_frame_time - last_frame_time < dt:
            time.sleep(sleep_length)
            current_frame_time = time.time()
        last_frame_time = current_frame_time
        yield