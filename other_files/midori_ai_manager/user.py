import json
import random
import requests
import platform

from cryptography.fernet import Fernet

def download_keys(COMMAND_SITE_KEY, discord_id):
     with requests.get(COMMAND_SITE_KEY, headers={"Discord-ID": discord_id}) as response:
        if response.status_code == 200:
            return response.text  # Read text-based key
        else:
            raise RuntimeError(f"Failed to download keys: {response.status_code}")

def request_keys(discord_id):

    base_url = "https://tea-cup.midori-ai.xyz/download/"
    key_filename = f"{discord_id}-key.txt"

    key_url = f"{base_url}{key_filename}"
    keys = download_keys(key_url, discord_id)

    fernet = Fernet(keys.encode())
    #decrypted_commands = fernet.decrypt(encrypted_commands)
    #system_message = bytes(decrypted_commands).decode()

    return fernet

class User:
    def __init__(self, username, discord_id): 
        self.username = username
        self.discord_id = discord_id

def load_user_from_json(filename):
    data = load_json(filename)
    return User(data["username"], data["discord_id"])

def load_json(filename, fernet):
    with open(filename, "rb") as f:
        encrypted_data = f.read()
    pre_data = bytes(fernet.decrypt(encrypted_data)).decode()
    data = json.loads(pre_data)
    return data

def save_json(filename, data, fernet):
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(filename, "wb") as f :
        f.write(encrypted_data)

## user.username = "Jane Doe"