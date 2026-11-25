import os.path

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = Path(__file__).resolve().parent

credentials_path = BASE_DIR / "credentials.json"

def jarvis_email():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(
            userId="me", 
            maxResults=15, 
            labelIds=["INBOX"],
            q="-category:social -category:promotions",
        ).execute()
        messages = results.get("messages", [])

        email_list = []

        if not messages:
            return ("No messages found")
        print("Messages:")
        for message in messages:
            email = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["From"]
            ).execute()

            email_list.append(email)

        str_email_list = " ".join(map(str, email_list))
        return str_email_list

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
