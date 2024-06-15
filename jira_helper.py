from typing import Dict
from datetime import datetime

from config import EnvironmentSettings
from jira import JIRA
import slack_helper

jira_client = JIRA(server=EnvironmentSettings.get_jira_api_server(),
                   basic_auth=(EnvironmentSettings.get_jira_user_email(),
                               EnvironmentSettings.get_jira_api_token()))


def create_bug(issue_title, reporter_email, channel_id, thread_ts):
    return _create_ticket(issue_title, reporter_email, channel_id, thread_ts, ticket_type="Bug")


def create_story(issue_title, reporter_email, channel_id, thread_ts):
    return _create_ticket(issue_title, reporter_email, channel_id, thread_ts, ticket_type="Story")


def create_task(issue_title, reporter_email, channel_id, thread_ts):
    return _create_ticket(issue_title, reporter_email, channel_id, thread_ts, ticket_type="Task")


def create_epic(issue_title, reporter_email, channel_id, thread_ts):
    return _create_ticket(issue_title, reporter_email, channel_id, thread_ts, ticket_type="Epic")


def _create_ticket(issue_title, reporter_email, channel_id, thread_ts, ticket_type):
    account_id = _get_jira_user_id_by_email(reporter_email)
    slack_thread_link = f"{EnvironmentSettings.get_slack_server()}/archives/{channel_id}/p{thread_ts.replace('.', '')}"
    parent_message = slack_helper.get_parent_message(channel_id, thread_ts) if thread_ts else "No thread message"
    stripped_command = ticket_type.lower()
    parent_message = parent_message.replace(f"!{stripped_command} ", "").replace(f"!{stripped_command}", "").strip()

    if ticket_type in ["Story", "Task", "Epic"]:
        description = (
            f"{{panel:borderStyle=dashed|borderColor=#00b|titleBGColor=#d2e0fc|bgColor=#f0f4ff}}This ticket is created as a result of the following Slack thread and its content is automatically copied here: {slack_thread_link}{{panel}}\n\n"
            f"*The automatically populated description from the original Slack thread:*\n\n{parent_message}"
        )
    else:
        description = (
            f"{{panel:borderStyle=dashed|borderColor=#00b|titleBGColor=#d2e0fc|bgColor=#f0f4ff}}This ticket is created as a result of the following Slack thread and its content is automatically copied here: {slack_thread_link}{{panel}}\n\n"
            f"{{panel:title=Quick Reminder|borderStyle=dashed|borderColor=#ccc|titleBGColor=#F7D6C1|bgColor=#FFFFCE}}Hey [~accountid:{account_id}], please ensure that the bug description adheres to the guidelines.{{panel}}"
            f"\n\n*The automatically populated description from the original Slack thread:*\n\n{parent_message}"
        )

    new_issue = jira_client.create_issue(project=EnvironmentSettings.get_jira_project_key(),
                                         summary=issue_title,
                                         description=description,
                                         issuetype={'name': ticket_type},
                                         labels=[ "SlackBot"],
                                         reporter={'accountId': account_id})
    return new_issue


def _get_jira_user_id_by_email(email):
    try:
        users = jira_client.search_users(query=email)
        if users:
            return users[0].accountId
    except Exception as e:
        print(f"Error finding Jira user: {e}")
    return None


def get_assigned_tasks(user_email) -> list[Dict[str, str]]:
    try:
        user_email = _get_jira_user_id_by_email(user_email)
        issues = jira_client.search_issues(f"assignee = {user_email} AND status IN ('Development', 'Code Complete', "
                                           f"'Blocked')")
        tasks = []
        for issue in issues:
            task = {
                'title': issue.fields.summary,
                'ticket_id': issue.key,
                'url': f"{EnvironmentSettings.get_jira_api_server()}/browse/{issue.key}",
                'state': issue.fields.status.name,
                'size': issue.fields.customfield_10428,
                'priority': issue.fields.priority.name
            }
            tasks.append(task)
        return tasks
    except Exception as e:
        print(f"Error finding assigned tasks: {e}")
    return None


def get_story_size_priority(ticket_number):
    try:
        issue = jira_client.issue(ticket_number)
        # Jira stores story points, etc. in custom fields. The custom field ID for story points is 10428.
        return {
            "size": issue.fields.customfield_10428,
            "priority": issue.fields.priority.name
        }
    except Exception as e:
        raise Exception(f"The ticket could not be found!")


def get_elapsed_time_for_each_jira_ticket_state(ticket_number):
    try:
        issue = jira_client.issue(ticket_number, expand='changelog')
    except Exception as e:
        raise Exception(f"The ticket could not be found!")

    if issue.fields.issuetype.name == "Epic":
        raise Exception(f"Cannot get elapsed time for an Epic ticket!")

    changelog = issue.changelog

    transitions = []
    last_transition_time = issue.fields.created
    last_transition_time = datetime.strptime(last_transition_time.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    last_state = "To Do"
    changelog.histories.reverse()

    for history in changelog.histories:
        for item in history.items:
            if item.field == 'status':
                transition_time = datetime.strptime(history.created.split('.')[0], "%Y-%m-%dT%H:%M:%S")
                elapsed_time = transition_time - last_transition_time
                transitions.append({
                    'state': last_state,
                    'elapsed_time': elapsed_time
                })
                last_transition_time = transition_time
                last_state = item.toString

    # Handle the time in the final state
    elapsed_time = datetime.now() - last_transition_time
    transitions.append({
        'state': last_state,
        'elapsed_time': elapsed_time
    })

    return transitions
