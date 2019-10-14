from energize.utils.utils import Stub

class PredictEnergy:

    def __init__(self, receiver=None):
        self._receiver = receiver if receiver is not None else Stub()

    def find_faces(self, image=None):

        return []

    def compare_faces(self, image=None):

        return []

    def read_expressions(self, image=None):

        return []

    def do_shizzle(self, image):

        print("-- RUNNING Energy Prediction")
        locations = PredictEnergy.find_faces(image)
        names = PredictEnergy.compare_faces(image)
        expressions = PredictEnergy.read_expressions(image)
        self._receiver.do_shizzle(image=image,
                                  locations=locations,
                                  names=names,
                                  expressions=expressions)




