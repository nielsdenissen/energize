from energize.report_energy_levels import report_energy_level


def predict(image):
    '''
    Predicts the energy in the input image. 
    Output is a dict of the following format:

    {
        "energyScore": 5,
        "roomName": "L2"
    }
    '''
    return {
        "energyScore": 5,
        "roomName": "L2"
    }


def main(image, image_creation_datetime):
    '''
    Predicts the energy in a room and writes and calls the reporter to report this data
    Output is a dict of the following format:

    {
        "imageCreationDatetime": "2013-10-29T09:38:41.341Z",
        "energyScore": 5,
        "roomName": "L2"
    }
    '''
    print("-- RUNNING Energy Prediction")

    result = predict(image)
    result["imageCreationDatetime"] = image_creation_datetime
    report_energy_level.main(result)
