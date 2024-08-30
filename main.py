from initializer import initialize, discover_submissions
from config import load_config

from msgraph import GraphServiceClient
from ms_todo_helpers import GraphApiHelper, SCOPES

# import asyncio


def main():
    initialize()
    config = load_config()
    graph_client = GraphServiceClient(config.ms_todo_token, SCOPES)
    graph_api = GraphApiHelper(graph_client, config)

    submissions = discover_submissions()

    graph_api.create_task(submissions)


if __name__ == "__main__":
    main()
