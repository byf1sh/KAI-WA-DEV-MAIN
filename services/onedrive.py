import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def list_onedrive_root_files(access_token, MS_GRAPH_BASE_URL=os.getenv("MS_GRAPH_BASE_URL")):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    # response = requests.get(f"{MS_GRAPH_BASE_URL}/me/drive/sharedWithMe", headers=headers)
    response = requests.get(f"{MS_GRAPH_BASE_URL}/me/drive/root/children", headers=headers)
    if response.status_code == 200:
        # print(response.json)
        json_helper(response.json())
        for item in response.json().get('value', []):
            print(f"{item['name']} - {item['webUrl']}")
    else:
        print(f"Gagal mengambil file: {response.status_code} {response.text}")


def json_helper(data):
    clean = json.dumps(data, indent=4)
    print(clean)