import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]  # read + create drafts/send

def gmail_service():
    """
    Returns an authorized Gmail API service instance.
    Make sure credentials.json (OAuth client) is in the same folder.
    On first run a browser window will open to authorize.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for next runs
        with open("token.json", "w") as f:
            f.write(creds.to_json())

    service = build("gmail", "v1",  credentials=creds)
    return service

if __name__ == "__main__":
    
    s = gmail_service()
    print("✅ Gmail service ready.")
