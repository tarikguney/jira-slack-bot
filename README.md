# Jira Slack Bot

This project is a Slack bot that integrates with Jira to manage tasks, bugs, stories, and epics. It allows users to create and manage tickets directly from Slack.

## Sample Slack Conversation

> The following is an example of a conversation between two users in Slack using the bot and how they can create a bug ticket:

**John**: Hey Jane, I've noticed an issue with the login functionality. It seems to be failing when I try to login with my credentials.

**Jane**: That's strange, John. I just tested it and it seems to be working fine for me. Can you provide more details about the issue?

**John**: Sure, I'm getting a "Invalid Credentials" error even though I'm entering the correct username and password.

**Jane**: That's definitely not expected. Let's create a bug for this. 

**Jane**: `!bug Login functionality failing with valid credentials`

**SlackBot**: Bug ticket created with title "Login functionality failing with valid credentials". You can view the ticket [here](https://jira.example.com/browse/BUG-1234).

## Features

The bot supports the following commands:

1. `!bug <title>` - Create a new bug ticket with the provided title.
2. `!story <title>` - Create a new story ticket with the provided title.
3. `!task <title>` - Create a new task ticket with the provided title.
4. `!epic <title>` - Create a new epic ticket with the provided title.
5. `!priority` - Get the list of questions to prioritize an issue.
6. `!inprogress <@USERID>` - Get the list of tasks that a user is currently working on.
7. `!time <ticket_id>` - Get the elapsed time for each state transition for a ticket.
8. `!help` - Get the list of commands you can use with me.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python
- pip

### Installing

1. Clone the repository
2. Install the dependencies with pip:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

## Built With

- Python
- Flask
- slack_sdk
- Jira SDK

## Integrating with Slack

### Creating a Slack Bot

To create a Slack bot, follow these steps:

1. Go to the [Slack API website](https://api.slack.com/apps) and click on the 'Create New App' button.
2. In the pop-up window, select 'From scratch', give your app a name, and select the workspace where you want to install the bot.
3. Once the app is created, go to the 'Bot Users' feature in the sidebar, click on 'Add a Bot User', and then 'Add Bot User' again to validate.
4. Install the app to your workspace. Go to the 'Install App' feature in the sidebar, and click on 'Install App to Workspace'. You will be redirected to your workspace's authorization page.
5. Authorize the app. Once authorized, you will be redirected back to the 'Install App' page, where you will find the 'Bot User OAuth Access Token'. This token is used to authenticate the bot in your code.

### Setting Up Event Subscriptions

To use event subscriptions with this Slack bot, you need to configure your Slack app to send specific events to your bot's server. Here's how you can do it:

1. Go to your app's configuration page on the Slack API website.
2. Click on 'Event Subscriptions' in the sidebar.
3. Toggle 'Enable Events' to 'On'.
4. In the 'Request URL' field, enter the URL of your server where the bot is running. This should be the URL followed by `/slack/events`, which is the endpoint in your `app.py` that Slack will send event data to. For example, if your server is running at `http://myserver.com`, you would enter `http://myserver.com/slack/events`.
5. Once you've entered the URL, Slack will send a challenge request to verify the server. Your server should respond to this challenge, which is already handled in your `app.py`.
6. In the 'Subscribe to Bot Events' section, click on 'Add Bot User Event'.
7. In the pop-up, select the 'message.channels' event. This event is triggered whenever a message is posted in a channel.
8. Click on 'Save Changes'.

Now, whenever a message is posted in a channel that the bot is a member of, Slack will send an event to your server. The server will then handle the event as defined in your `app.py`.

Remember to reinstall your app in your workspace after making these changes for them to take effect. You can do this from the 'Install App' page in your app's configuration.

### Authorization Scopes

For the Slack bot to read messages in public and private channels and write messages, you need to add the following OAuth scopes to your Slack app:

- `channels:history`: This scope lets your app view messages and other content in public channels that your app has been added to.
- `groups:history`: This scope lets your app view messages and other content in private channels that your app has been added to.
- `chat:write`: This scope lets your app send messages as itself.

To add these scopes, follow these steps:

1. Go to your app's configuration page on the Slack API website.
2. Click on 'OAuth & Permissions' in the sidebar.
3. Scroll down to the 'Scopes' section.
4. In the 'Bot Token Scopes' subsection, click on 'Add an OAuth Scope'.
5. In the pop-up, select `channels:history`, `groups:history`, and `chat:write`.
6. Click on 'Save Changes'.

Remember to reinstall your app in your workspace after making these changes for them to take effect. You can do this from the 'Install App' page in your app's configuration.

## Project Structure

- `app.py`: This is the main entry point of the application. It initializes the Flask application and starts the server.

- `slack_message_handler.py`: This file contains the logic for handling incoming Slack messages and responding to them. It includes functions for each command that the bot supports (!bug, !story, !task, !epic, !priority, !inprogress, !time, !help).

- `slack_helper.py`: This file contains helper functions for interacting with the Slack API. It includes functions for sending messages, handling event subscriptions, and verifying requests from Slack.

- `jira_helper.py`: This file contains helper functions for interacting with the Jira API. It includes functions for creating tickets, getting the elapsed time for each state transition of a ticket, and getting the story size and priority of a ticket.

- `requirements.txt`: This file lists the Python dependencies that need to be installed for the project to run.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.