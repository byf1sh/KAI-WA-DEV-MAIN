import requests
from services.data_utils import extract_field
import json
from datetime import datetime, timedelta, timezone

list_of_email = []
def get_email(access_token):
    url = (
        "https://graph.microsoft.com/v1.0/me/mailFolders/AQMkADAwATMwMAExLTk0MTAtNWIwYS0wMAItMDAKAC4AAAPXk1ofh1tcQ7a7zM87lgGIAQCbYCOQqe0FS4jHj3XUdozvAAACZ1wAAAA=/messages"
        "?$top=20&$orderby=receivedDateTime desc"
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    fol = json.dumps(response.json(), indent= 4)
    # print(fol)
    if response.status_code == 200:
        emails = response.json().get("value", [])
        # print(emails)
        for email in emails:
            email_data = {
                "timestamp":email.get("receivedDateTime"),
                "case_id" : extract_field("Case ID", email.get("bodyPreview")),
                "content":email.get("bodyPreview")
                }
            list_of_email.append(email_data)
            # email = json.dumps(email_data, indent=4)
            # print(email)
        # print(list_of_email)
        return list_of_email
    else:
        print("Gagal mengambil email:", response.status_code, response.text)
