import os
import sys
import pytz
import json
import base64
import shutil
import hashlib
import tarfile
import getpass
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

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
os.makedirs(folder_path, exist_ok=True)

username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

username = None

if os.path.exists(username_file):
    with open(username_file, 'r') as f:
        username = f.read()
    
    os.system("midori-ai-login")

if username is None:
    if hasattr(args, "username"):
        username = args.username

if username is None:
    print("You have not logged into Midori AI\'s servers...")
    sys.exit(25)

def check_programs(program_name):
  try:
    shutil.which(program_name)
    return True
  except shutil.Error:
    return False

def encrypt_user_data(data, username, salt):
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

def decrypt_user_data(encrypted_data, username, salt):
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



def upload_to_midori_ai():
    print("Please enter a token to encrypt your data before sending it to Midori AI")
    print("Midori AI will not get this token, please record this token in a safe place")
    pre_salt = getpass.getpass("Token: ")
    salt = str(pre_salt).encode()

def download_from_midori_ai():
    print("Please enter a token to decrypt your data after downloading it from Midori AI")
    pre_salt = getpass.getpass("Token: ")
    salt = str(pre_salt).encode()

def main(args):
    item = str(args.item).lower()
    item_type = str(args.type).lower()
    pack = bool(args.pack)
    unpack = bool(args.unpack)
    upload = bool(args.upload)
    download = bool(args.download)

    if pack and unpack:
        raise Exception("You cannot pack/unpack at the same time.")

    if upload and download:
        raise Exception("You cannot upload/download at the same time.")

    midori_ai_programs = ["midori-ai-downloader", "midori-ai-uploader"]

    for program in midori_ai_programs:
        if check_programs(program):
            continue
        else:
            print(f"You are missing {program} form your path, please install or update them...")



if __name__ == "__main__":
    main(args)