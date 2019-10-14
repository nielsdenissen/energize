

class PredictEnergy:

    def find_faces(self, image=None):

        return "I found your face"

    def compare_faces(self, image=None):

        return "I compared your face"

    def read_expressions(self, image=None):

        return "You make sad face"

    def do_shizzle(self, image, receiver=None):

        print("-- RUNNING Energy Prediction")
        locations = PredictEnergy.find_faces(image)
        names = PredictEnergy.compare_faces(image)
        expressions = PredictEnergy.read_expressions(image)
        receiver.do_shizzle(image, locations, names, expressions)




