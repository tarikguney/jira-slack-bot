from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import slack_helper
from config import EnvironmentSettings
import jira_helper

slack_client = WebClient(token=EnvironmentSettings.get_slack_bot_token())


def _post_message(channel, thread_ts, text):
    try:
        response = slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=text)
        print(response)
    except SlackApiError as e:
        print(f"Error posting message: {e}")


def _remove_command_from_title(text, command):
    return text.replace(f"{command} ", "").replace(command, "").strip()


def _respond_bug_command(user_id, text, channel, thread_ts):
    user_email = slack_helper.get_slack_user_email(user_id)
    bug_title = _remove_command_from_title(text, "!bug")
    if bug_title == "":
        response = (
            "Please provide a title for your bug ticket! A sample command looks like this: `!bug This is a ticket "
            "title`")
        _post_message(channel, thread_ts, response)
        return
    created_issue = jira_helper.create_bug(bug_title, user_email, channel, thread_ts)
    issue_link = created_issue.permalink()
    response = f"Your new bug ticket has been created here: {issue_link}"
    _post_message(channel, thread_ts, response)


def _respond_story_command(user_id, text, channel, thread_ts):
    user_email = slack_helper.get_slack_user_email(user_id)
    story_title = _remove_command_from_title(text, "!story")
    if story_title == "":
        response = ("Please provide a title for your story ticket! A sample command looks like this: `!story This "
                    "is a ticket title`")
        _post_message(channel, thread_ts, response)
        return
    created_issue = jira_helper.create_story(story_title, user_email, channel, thread_ts)
    issue_link = created_issue.permalink()
    response = f"Your new story ticket has been created here: {issue_link}"
    _post_message(channel, thread_ts, response)


def _respond_task_command(user_id, text, channel, thread_ts):
    user_email = slack_helper.get_slack_user_email(user_id)
    task_title = _remove_command_from_title(text, "!task")
    if task_title == "":
        response = (
            "Please provide a title for your task ticket! A sample command looks like this: "
            "`!task This is a ticket title`")
        _post_message(channel, thread_ts, response)
        return
    created_issue = jira_helper.create_task(task_title, user_email, channel, thread_ts)
    issue_link = created_issue.permalink()
    response = f"Your new task ticket has been created here: {issue_link}"
    _post_message(channel, thread_ts, response)


def _respond_epic_command(user_id, text, channel, thread_ts):
    user_email = slack_helper.get_slack_user_email(user_id)
    epic_title = _remove_command_from_title(text, "!epic")
    if epic_title == "":
        response = (
            "Please provide a title for your epic ticket! A sample command looks like this: "
            "`!epic This is a ticket title`")
        _post_message(channel, thread_ts, response)
        return
    created_issue = jira_helper.create_epic(epic_title, user_email, channel, thread_ts)
    issue_link = created_issue.permalink()
    response = f"Your new epic ticket has been created here: {issue_link}"
    _post_message(channel, thread_ts, response)


def _respond_priority_command(channel, thread_ts):
    response = (
        "Thanks for reporting your issue. For us to prioritize the issue appropriately, could you please provide "
        "the following information:\n\n"
        "1. Is this problem blocking any critical release? _[Yes | No]_\n"
        "2. In which environments have you observed the issue? _[Production | Staging | Development]_\n"
        "3. What is the estimated extent of production user impact? _[Affects large | medium | small number of "
        "users]_\n"
        "4. Have you identified any workaround? _[Yes | No]_\n"
        "5. How often are you able to reproduce this issue? _[Always | Sometimes | Rarely]_\n"
        "6. What is your expected timeline for resolving this issue? _[Immediate | Within 24 hours | This week | "
        "Longer]_\n"
        "7. How severe is the impact of this issue on user experience? _[Critical | High | Medium | Low]_")
    _post_message(channel, thread_ts, response)


def _respond_in_progress_command(channel, thread_ts, text):
    slack_user_mentioned_name = text.split('!inprogress')[1].strip()
    if not slack_user_mentioned_name.startswith('<@') or not slack_user_mentioned_name.endswith('>'):
        _post_message(channel, thread_ts, "Invalid user ID format. Please use the format <@USERID>.")
        return
    slack_user_id = slack_user_mentioned_name.replace('<@', '').replace('>', '')
    user_email = slack_helper.get_slack_user_email(slack_user_id)
    assigned_tasks = jira_helper.get_assigned_tasks(user_email)
    task_list = []
    for index, task in enumerate(assigned_tasks, start=1):
        task_string = f"{index}. _*{task['priority']}*_ - <{task['url']}|{task['ticket_id']} - {task['title']}> in *{task['state']}*."
        task_list.append(task_string)
    if len(task_list) == 0:
        response = f":construction: {slack_user_mentioned_name} has *no tasks* assigned that is in progress."
    else:
        response = f":construction: {slack_user_mentioned_name} is *currently working* on the following ticket(s):\n\n" + "\n".join(
            task_list)
    _post_message(channel, thread_ts, response)


def _respond_time_command(channel, thread_ts, text):
    ticket_id = text.split('!time')[1].strip()
    if ticket_id is None or ticket_id == "":
        response = "Please provide a ticket ID to get the elapsed time for each state transition."
        _post_message(channel, thread_ts, response)
        return
    try:
        elapsed_time_list = jira_helper.get_elapsed_time_for_each_jira_ticket_state(ticket_id)
    except Exception as e:
        _post_message(channel, thread_ts, f"Error getting elapsed time for ticket *{ticket_id.upper()}*: {e}")

    try:
        story_size_priority_dict = jira_helper.get_story_size_priority(ticket_id)
    except Exception as e:
        story_size_priority_dict = {
            "size": "None",
            "priority": "None"
        }

    elapse_times_joined_message = []

    def format_duration(duration):
        minutes, seconds = divmod(duration.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration_string = ""
        if duration.days > 0:
            duration_string += f"{duration.days} day(s) "
        if hours > 0:
            duration_string += f"{hours} hour(s) "
        if minutes > 0:
            duration_string += f"{minutes} minute(s) "
        if seconds > 0:
            duration_string += f"{seconds} second(s)"

        return duration_string.strip()

    # Then in your loop
    for index, time in enumerate(elapsed_time_list, start=1):
        formatted_time = format_duration(time["elapsed_time"])
        if len(elapsed_time_list) == index:
            elapse_times_joined_message.append(
                f"{index}. :here: Currently in *{time['state']}* state for *{formatted_time}*.")
        else:
            elapse_times_joined_message.append(
                f"{index}. Stayed in *{time['state']}* state for *{formatted_time}*.")

    response = f"The elapsed time for each state of ticket *{ticket_id.upper()}* with *{story_size_priority_dict['size']} points* and *{story_size_priority_dict['priority']} priority* as follows:\n\n" + "\n".join(
        elapse_times_joined_message)

    _post_message(channel, thread_ts, response)


def _respond_help_command(channel, thread_ts):
    response = (
        "Here are the commands you can use with me:\n\n"
        "1. `!bug <title>` - Create a new bug ticket with the provided title.\n"
        "2. `!story <title>` - Create a new story ticket with the provided title.\n"
        "3. `!task <title>` - Create a new task ticket with the provided title.\n"
        "4. `!epic <title>` - Create a new epic ticket with the provided title.\n"
        "5. `!priority` - Get the list of questions to prioritize an issue.\n"
        "6. `!inprogress <@USERID>` - Get the list of tasks that a user is currently working on.\n"
        "7. `!time <ticket_id>` - Get the elapsed time for each state transition for a ticket.\n"
        "8. `!help` - Get the list of commands you can use with me.\n"
    )
    _post_message(channel, thread_ts, response)


def handle_message(event_data):
    text = event_data['text']
    channel = event_data['channel']
    thread_ts = event_data['thread_ts'] if "thread_ts" in event_data else event_data['ts']
    user_id = event_data['user']

    bot_info = slack_client.auth_test()
    bot_user_id = bot_info['user_id']

    # We don't want to respond to bot's own messages.
    if user_id == bot_user_id:
        return

    elif text.startswith('!bug '):
        _respond_bug_command(user_id, text, channel, thread_ts)

    elif text.startswith("!story "):
        _respond_story_command(user_id, text, channel, thread_ts)

    elif text.startswith("!task "):
        _respond_task_command(user_id, text, channel, thread_ts)

    elif text.startswith("!epic "):
        _respond_epic_command(user_id, text, channel, thread_ts)

    elif text.startswith("!priority "):
        _respond_priority_command(channel, thread_ts)

    elif text.startswith("!inprogress "):
        _respond_in_progress_command(channel, thread_ts, text)

    elif text.startswith("!time "):
        _respond_time_command(channel, thread_ts, text)

    elif text.startswith("!help"):
        _respond_help_command(channel, thread_ts)
