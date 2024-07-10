from config import Config
from ms_todo_helpers import get_ms_todo_auth_code, get_access_token


def show_welcome_msg():
    print("Welcome to this Script")
    print(
        # TODO refactor Script_name
        "Script_name is a tool that notifies you about new submissions on the BUE E-Learning."
    )


def ask_for_credentials():
    print("The Script needs to be configured first. This is a one-time process.")
    print("This tool requires your BUE credentials to access the E=Learning.")
    print(
        "Don't worry, your credentials are stored locally and are not shared with anyone."
    )
    bue_username = input("What is your BUE username? ")
    bue_password = input("What is your BUE password? ")
    print("Now, we need to authorize the script to access your Todoist account.")
    print(
        "A browser window will open, please authorize the script to access your Todoist account."
    )
    todo_auth_code = get_ms_todo_auth_code()
    todo_token = get_access_token(todo_auth_code)
