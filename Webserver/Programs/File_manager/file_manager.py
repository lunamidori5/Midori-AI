import os
import sys
import pytz
import json
import base64
import hashlib
import tarfile
import platform
import argparse
import requests
import datetime

from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description="File manager for packing, unpacking, uploading, and downloading files and folders to / from Midori AI\'s servers")
parser.add_argument("-i", "--item", required=True, type=str, help="File / Folder being packed / unpacked")
parser.add_argument("-t", "--type", required=True, type=str, help="Type of Item (file or folder)")
parser.add_argument("-p", "--pack", action="store_true", help="Pack items")
parser.add_argument("-un", "--unpack", action="store_true", help="Unpack items")
parser.add_argument("-up", "--upload", action="store_true", help="Upload items")
parser.add_argument("-d", "--download", action="store_true", help="Download items")

args = parser.parse_args()

item = str(args.item).lower()
item_type = str(args.type).lower()
action = str(args.action).lower()

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
os.makedirs(folder_path, exist_ok=True)

username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

la_timezone = pytz.timezone('America/Los_Angeles')
salt = str(datetime.datetime.now(la_timezone).strftime('%d')).encode()

print(f"Checking: {username_file}")
print(f"Checking: {api_key_file}")

username = None

if os.path.exists(username_file):
    with open(username_file, 'r') as f:
        username = f.read()

if username is None:
    if hasattr(args, "username"):
        username = args.username

if username is None:
    print("You have not logged into Midori AI\'s servers...")
    sys.exit(25)


def encrypt_user_data(data, username):
    stats = {
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
    }

    stats_json = json.dumps(stats)
    os_version = os.uname().machine

    hash_object = hashlib.sha512(stats_json.encode())
    os_hash_object = hashlib.sha512(os_version.encode())

    password = hash_object.hexdigest()
    twoflogin = os_hash_object.hexdigest()

    stats = {
        "user": {
            "username": username,
            "platform_hash": password,
            "os_version_hash": twoflogin,
        },
    }

    stats_json = json.dumps(stats)

    hash_object = hashlib.sha512(stats_json.encode())
    hash_hex = hash_object.hexdigest()
    
    # Generate a 32-byte Fernet-compatible key
    key = base64.urlsafe_b64encode(hashlib.sha256(hash_hex.encode() + salt).digest())

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypt_user_data(encrypted_data, username):
    stats = {
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
    }

    stats_json = json.dumps(stats)
    os_version = os.uname().machine

    hash_object = hashlib.sha512(stats_json.encode())
    os_hash_object = hashlib.sha512(os_version.encode())

    password = hash_object.hexdigest()
    twoflogin = os_hash_object.hexdigest()

    stats = {
        "user": {
            "username": username,
            "platform_hash": password,
            "os_version_hash": twoflogin,
        },
    }

    stats_json = json.dumps(stats)

    hash_object = hashlib.sha512(stats_json.encode())
    hash_hex = hash_object.hexdigest()

    # Generate the same 32-byte Fernet-compatible key for decryption
    key = base64.urlsafe_b64encode(hashlib.sha256(hash_hex.encode() + salt).digest())
    cipher = Fernet(key)

    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data