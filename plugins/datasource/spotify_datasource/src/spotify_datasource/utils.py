import base64
import os
from pathlib import Path
import requests
from dotenv import load_dotenv


def get_auth_token() -> str:

    load_dotenv()
    print(os.getenv("SPOTIFY_CLIENT_ID"))

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data)
    auth_token = response.json().get("access_token")

    return auth_token
