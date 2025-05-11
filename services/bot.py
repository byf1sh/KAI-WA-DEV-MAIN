import requests
from dotenv import load_dotenv
import os

load_dotenv()

def send(Message):
    token = os.getenv("tele_bot_token")
    chat_id = '5825923030'
    message = Message
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, data=payload)