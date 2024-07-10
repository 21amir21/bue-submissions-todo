import requests
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

from msgraph import GraphServiceClient
from msgraph.generated.models.todo_task import TodoTask
from msgraph.generated.models.linked_resource import LinkedResource


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

SERVER_PORT = 5050

APP_ID = os.getenv("APP_ID")

redirect_uri = f"http://localhost:{SERVER_PORT}/callback"
authority_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
scopes = ["Tasks.ReadWrite"]


# def create_confidential_client(
#     client_id: str | None, client_secret: str | None, authority: str | None
# ):
#     """Call it in the main and then make an app from it"""
#     return ConfidentialClientApplication(
#         client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=authority_url
#     )


def get_ms_todo_auth_code():

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "response_type": "query",
        "scope": scopes,
    }
    authorization_url = f"{authority_url}?{urlencode(params)}"

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

        def log_message(self, format: str, *args: os.Any) -> None:
            return

    webbrowser.open(authorization_url)
    server = HTTPServer(("", SERVER_PORT), AuthorizeServer)

    while not AuthorizeServer.token_retrieved:
        server.handle_request()

    return AuthorizeServer.auth_code


def get_access_token(auth_code):
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "scope": scopes,
    }

    response = requests.post(url=token_url, data=token_data)
    data = response.json()

    return data["access_token"]


# in order to continue must read the docs
# https://learn.microsoft.com/en-us/graph/api/resources/todo-overview?view=graph-rest-1.0

graph_client = GraphServiceClient(get_access_token(get_ms_todo_auth_code()), scopes)
