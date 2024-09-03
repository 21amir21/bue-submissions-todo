import requests
import os
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from msgraph import GraphServiceClient
from msgraph.generated.models.todo_task import TodoTask
from msgraph.generated.models.linked_resource import LinkedResource
from config import Config

from msal import ConfidentialClientApplication


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

SERVER_PORT = 5050  # or 5000

APP_ID = os.getenv("APP_ID")

REDIRECT_URI = f"http://localhost:{SERVER_PORT}/callback"
# AUTHORITY_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
AUTHORITY_URL = "https://login.microsoftonline.com/consumers"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
SCOPES = ["Tasks.ReadWrite"]


def create_confidential_client(
    client_id: str | None, client_secret: str | None, authority: str | None
):
    """Call it in the main and then make an app from it"""
    return ConfidentialClientApplication(
        client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY_URL
    )


def get_access_token(app: ConfidentialClientApplication, scopes):
    auth_url = app.get_authorization_request_url(scopes)
    webbrowser.open(auth_url, new=True)


# might need to REFACTOR this and make it with flask
def get_ms_todo_auth_code():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "response_type": "query",
        "scope": SCOPES,
    }

    authorization_url = f"{AUTHORITY_URL}?{urlencode(params)}"

    class AuthorizeServer(BaseHTTPRequestHandler):
        auth_code = ""
        token_retrieved = False

        def do_GET(self):
            AuthorizeServer.token_retrieved = True
            AuthorizeServer.auth_code = parse_qs(urlparse(self.path).query)["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes("Authorization completed. You can close this.", "utf-8")
            )

        def log_message(self, format: str, *args) -> None:
            return

    webbrowser.open(authorization_url)
    server = HTTPServer(("", SERVER_PORT), AuthorizeServer)

    while not AuthorizeServer.token_retrieved:
        server.handle_request()

    return AuthorizeServer.auth_code


def get_access_tokennn(auth_code):
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }

    response = requests.post(url=TOKEN_URL, data=token_data)
    data = response.json()

    return data["access_token"]


# in order to continue must read the docs
# https://learn.microsoft
# .com/en-us/graph/api/resources/todo-overview?view=graph-rest-1.0

# graph_client = GraphServiceClient(get_access_token(get_ms_todo_auth_code()), SCOPES)


class GraphApiHelper:
    def __init__(self, graph_client: GraphServiceClient, config: Config):
        self.graph_client = graph_client
        self.config = config

    # Do i Really have to make it async ?!
    def create_task(self, submissions: list):
        # submissions = scrape_bue_calendar(self.config)

        for submission in submissions:
            request_body = TodoTask(
                title=submission["title"],
                categories=[
                    "Important",
                ],
                linked_resources=[
                    LinkedResource(
                        web_url=submission["link"],
                        application_name="Microsoft",
                        display_name="Microsoft",
                    ),
                ],
            )

            tasks_lists = self.graph_client.me.todo.lists.get()
            important_list = next(
                (
                    task_list
                    for task_list in tasks_lists.value
                    if task_list.display_name == "Important"
                ),
                None,
            )

            result = self.graph_client.me.todo.lists.by_todo_task_list_id(
                important_list.id
            ).tasks.post(request_body)
