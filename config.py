from dotenv import load_dotenv
import os

load_dotenv()

_slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
_jira_user_email = os.getenv("JIRA_USER_EMAIL")
_jira_api_token = os.getenv("JIRA_API_TOKEN")
_jira_api_server = os.getenv("JIRA_API_SERVER")
_jira_project_key = os.getenv("JIRA_PROJECT_KEY")
_slack_server = os.getenv("SLACK_SERVER")


class EnvironmentSettings:
    @staticmethod
    def get_slack_bot_token():
        return _slack_bot_token

    @staticmethod
    def get_jira_api_token():
        return _jira_api_token

    @staticmethod
    def get_jira_api_server():
        return _jira_api_server

    @staticmethod
    def get_jira_user_email():
        return _jira_user_email

    @staticmethod
    def get_jira_project_key():
        return _jira_project_key

    @staticmethod
    def get_slack_server():
        return _slack_server
