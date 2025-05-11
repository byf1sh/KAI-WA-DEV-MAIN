import os
from dotenv import load_dotenv
from services.auth import get_access_token
from services.onedrive import list_onedrive_root_files
from services.email_service import get_email
load_dotenv()

def start_graph():
    APPLICATION_ID = os.getenv("APPLICATION_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    # SCOPES = ['Files.ReadWrite.All','User.Read']
    SCOPES = ['https://graph.microsoft.com/.default']

    try:
        token = get_access_token(APPLICATION_ID, CLIENT_SECRET, SCOPES)
        return token
    except Exception as e:
        print(f'Error: {e}')
