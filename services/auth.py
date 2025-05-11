import webbrowser
import msal
import os
from dotenv import load_dotenv

load_dotenv()

CACHE_FILE = 'token_cache.bin'
REDIRECT_URI = 'http://localhost:8000'

def load_token_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        cache.deserialize(open(CACHE_FILE, 'r').read())
    return cache

def save_token_cache(cache):
    if cache.has_state_changed:
        with open(CACHE_FILE, 'w') as f:
            f.write(cache.serialize())

def get_access_token(application_id, client_secret, scopes):
    cache = load_token_cache()

    client = msal.ConfidentialClientApplication(
        client_id=application_id,
        client_credential=client_secret,
        authority=f'https://login.microsoftonline.com/common',
        # authority=f'https://login.microsoftonline.com/{os.getenv("TENANT_ID")}/',
        token_cache=cache
    )

    # Coba ambil token dari cache
    accounts = client.get_accounts()
    if accounts:
        token_response = client.acquire_token_silent(scopes, account=accounts[0])
        if token_response:
            save_token_cache(cache)
            return token_response['access_token']

    # Jika tidak ada token yang valid, lakukan auth code flow
    auth_url = client.get_authorization_request_url(scopes, redirect_uri=REDIRECT_URI)
    print(auth_url)
    webbrowser.open(auth_url)
    # webbrowser.get("C:\Program Files\Google\Chrome\Application\chrome.exe %s").open(auth_url)
    code = input("Masukkan authorization code: ")

    token_response = client.acquire_token_by_authorization_code(
        code=code,
        scopes=scopes,
        redirect_uri=REDIRECT_URI
    )

    if 'access_token' in token_response:
        save_token_cache(cache)
        return token_response['access_token']
    else:
        raise Exception(f"Gagal mendapatkan token: {token_response.get('error_description')}")
