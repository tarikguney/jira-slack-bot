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

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.