import cv2
import slack
import os


class ReportEnergyLevel:

    def __init__(self, output_fnc=None):
        cv2.namedWindow("Energize", cv2.WINDOW_NORMAL)

    def do_shizzle(self, **kwargs):
        image = kwargs.pop("image", None)
        locations = list(kwargs.pop("locations", []))
        names = list(kwargs.pop("names", []))
        expressions = list(kwargs.pop("expressions", []))

        names = names + ["Unknown"]*(len(locations) - len(names))
        expressions = expressionspip + ["Unknown"]*(len(locations) - len(expressions))
        face_info = list(zip(locations, names, expressions))

        if image is not None:
            for loc, name, expr in face_info:
                top, right, bottom, left = loc
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow("Energize", image)
        cv2.waitKey(1)

    def cleanup(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def __del__(self):
        self.cleanup()

    def send_slack_message(self, data):
        client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        channel_id = os.environ['ENERGIZE_CHANNEL_ID']  # Energize channel
        client.chat_postMessage(channel=channel_id, text=data)

    def lookup_user_id(self, name):
        client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        member_list = client.users_list().data
        for user in member_list['members']:
            if name.lower() in user['name']:
                return user['id']

