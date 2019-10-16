import slack
import os


def lookup_user_id(name):
    client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    member_list = client.users_list().data
    for user in member_list['members']:
        if name.lower() in user['name']:
            return user['id']

def format_name_for_slack(name):
    return "<@{}>".format(name)

def send_slack_message(text):
    client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    channel_id = os.environ['ENERGIZE_CHANNEL_ID']  # Energize channel
    client.chat_postMessage(channel=channel_id, text=text)

def meeting_start_notification(predictions):
    user_ids = []
    for attendees in predictions['faces']:
        user_ids.append(format_name_for_slack(lookup_user_id(attendees['name'].split()[0])))

    name_energy_pair = []
    for i, attendees in enumerate(predictions['faces']):
        name_energy_pair.append("*{}* has the expression: *{}*".
                                format(user_ids[i], predictions['faces'][i]['expression']))

    message = "The following people have been spotted in a meeting room {} and the current energy level is: *{}*"\
        .format(
            " ".join(name_energy_pair),
            predictions['energy']
        )
    send_slack_message(message)
