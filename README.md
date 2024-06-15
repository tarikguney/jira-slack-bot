# Jira Slack Bot

This project is a Slack bot that integrates with Jira to manage tasks, bugs, stories, and epics. It allows users to create and manage tickets directly from Slack.

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

## Project Structure

- `app.py`: This is the main entry point of the application. It initializes the Flask application and starts the server.  

- `slack_message_handler.py`: This file contains the logic for handling incoming Slack messages and responding to them. It includes functions for each command that the bot supports (!bug, !story, !task, !epic, !priority, !inprogress, !time, !help).  

- `jira_helper.py`: This file contains helper functions for interacting with the Jira API. It includes functions for creating tickets, getting the elapsed time for each state transition of a ticket, and getting the story size and priority of a ticket.  

- `requirements.txt`: This file lists the Python dependencies that need to be installed for the project to run.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.