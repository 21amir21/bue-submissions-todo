from config import Config, load_config, is_configured, save_config
from ms_todo_helpers import (
    get_ms_todo_auth_code,
    get_access_token,
    GraphApiHelper,
    SCOPES,
)
from msgraph import GraphServiceClient
from scrapper import scrape_bue_calendar


def show_welcome_msg():
    print("Welcome to this Script")
    print(
        # TODO refactor Script_name
        "This script is a tool that notifies you about new submissions on the BUE E-Learning."
    )


def ask_for_credentials():
    print("The Script needs to be configured first. This is a one-time process.")
    print("This tool requires your BUE credentials to access the E=Learning.")
    print(
        "Don't worry, your credentials are stored locally and are not shared with anyone."
    )
    bue_username = input("What is your BUE username? ")
    bue_password = input("What is your BUE password? ")
    print("Now, we need to authorize the script to access your Microsoft account.")
    print(
        "A browser window will open, please authorize the script to access your Microsoft account."
    )
    todo_auth_code = get_ms_todo_auth_code()
    todo_token = get_access_token(todo_auth_code)
    config = Config(bue_username, bue_password, todo_token)

    return config

    # graph_client = GraphServiceClient(user.ms_todo_token, SCOPES)
    # graph_api = GraphApiHelper(graph_client, user)


def discover_submissions():
    print("Discovering new submissions...")
    config = load_config()
    submissions = scrape_bue_calendar(config)

    # TODO: implement validation XXX
    # to make sure that the submission are all new before returning them
    # to prevent having duplicates

    return submissions


def initialize():
    show_welcome_msg()

    if not is_configured():
        config = ask_for_credentials()
        save_config(config)
