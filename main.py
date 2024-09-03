from initializer import initialize, discover_submissions
from config import load_config

from msgraph import GraphServiceClient
from ms_todo_helpers import (
    GraphApiHelper,
    SCOPES,
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORITY_URL,
    create_confidential_client,
    get_access_token,
)


def main():
    # initialize()
    # config = load_config()
    # graph_client = GraphServiceClient(config.ms_todo_token, SCOPES)
    # graph_api = GraphApiHelper(graph_client, config)

    # submissions = discover_submissions()

    # graph_api.create_task(submissions)
    app = create_confidential_client(CLIENT_ID, CLIENT_SECRET, AUTHORITY_URL)
    get_access_token(app, SCOPES)


if __name__ == "__main__":
    main()
