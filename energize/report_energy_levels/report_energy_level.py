import cv2
from energize.utils.utils import Stub

class ReportEnergyLevel:

    def __init__(self, receiver):
        self._receiver = receiver if receiver is not None else Stub()
        cv2.namedWindow("Energize", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Energize", 100, 1200)

    def do_shizzle(self, **kwargs):
        image = kwargs.pop("image", None)
        locations = list(kwargs.pop("locations", []))
        names = list(kwargs.pop("names", []))
        expressions = list(kwargs.pop("expressions", []))

        names = names + ["Unknown"]*(len(locations) - len(names))
        expressions = expressions + ["Unknown"]*(len(locations) - len(expressions))
        face_info = list(zip(locations, names, expressions))

        if image is not None:
            for loc, name, expr in face_info:
                top, right, bottom, left = loc
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow("Energize", image)

    def cleanup(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def __del__(self):
        self.cleanup()