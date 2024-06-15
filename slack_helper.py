from slack_sdk.errors import SlackApiError
from config import EnvironmentSettings
from slack_sdk import WebClient

slack_client = WebClient(token=EnvironmentSettings.get_slack_bot_token())


def get_slack_user_email(user_id):
    try:
        user_info = slack_client.users_info(user=user_id)
        if user_info and user_info['user']['profile'].get('email'):
            return user_info['user']['profile']['email']
    except SlackApiError as e:
        print(f"Error retrieving user info: {e}")
    return None


def get_parent_message(channel_id, thread_ts):
    try:
        response = slack_client.conversations_replies(channel=channel_id, ts=thread_ts)
        messages = response.get('messages', [])
        if messages:
            return messages[0].get('text')
    except SlackApiError as e:
        print(f"Error fetching thread message: {e}")
    return None
