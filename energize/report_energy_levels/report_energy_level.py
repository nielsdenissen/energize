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


def translate_energy_levels(energy):
    if 0 > energy >= -0.5:
        return "Probably talking about Value"
    elif energy < -0.5:
        return "Bolke is probably in the room"
    elif 0 <= energy <= 0.5:
        return "Probably talking about Software Engineering"
    else:
        return "Talking about Data Engineering"


def translate_expressions(expression):
    if expression == -1:
        return "Probably has a pebble in their shoe"
    elif expression == 0:
        return "Member of the Borg"
    else:
        return "Is on Drugs"


def meeting_start_notification(predictions):
    user_ids = []
    for attendees in predictions['faces']:
        user_ids.append(format_name_for_slack(lookup_user_id(attendees['name'].split()[0])))

    name_energy_pair = []
    for i, attendees in enumerate(predictions['faces']):
        name_energy_pair.append("*{}* has the expression: *{}*".
                                format(user_ids[i], translate_expressions(predictions['faces'][i]['expression'])))

    message = "The following people have been spotted in a meeting room:\n {} \nand the current energy level is: *{}*"\
        .format(
            " \n".join(name_energy_pair),
            translate_energy_levels(predictions['energy'])
        )
    send_slack_message(message)
