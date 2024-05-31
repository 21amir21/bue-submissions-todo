import webbrowser
from msal import ConfidentialClientApplication
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import os


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


APP_ID = os.getenv("APP_ID")
AUTHORITY = "https://login.microsoftonline.come/consumers/"
scopes = ["Tasks.ReadWrite"]


def create_confidential_client(client_id, client_secret, authority):
    """Call it in the main and then make an app from it"""
    return ConfidentialClientApplication(
        client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY
    )


def get_access_token(app, scopes):
    """
    1-put the return in access_token
    2-neeeds more automation
    """
    auth_url = app.get_authorization_request_url(scopes)
    webbrowser.open(auth_url, new=True)

    authorization_code = input("Enter the authorization code: ")
    token_response = app.accquire_token_by_authorization_code(
        code=authorization_code, scopes=scopes
    )
    return token_response.get("access_token")
