import os
import sys
import json
import hashlib
import platform
import argparse
import requests

from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description="N/A")
parser.add_argument("-u", "--username", required=False, type=str, help="Username to use for the server...")
parser.add_argument("-byp", "--bypassplatform", required=False, type=str, help="Bypass platform check")
parser.add_argument("-byos", "--bypassoscheck", required=False, type=str, help="Bypass OS check")
parser.add_argument("-unsafe", "--unsafe", required=False, action='store_true', help="Enable unsafe mode")
parser.add_argument("-cli", "--commandline", required=False, action='store_true', help="Enable CLI mode")
parser.add_argument("-mkuser", "--makeuser", required=False, action='store_true', help="Enable makeuser mode")
args = parser.parse_args()

pre_unsafe = str(args.unsafe).lower()
pre_cli = str(args.commandline).lower()
pre_makeuser = str(args.makeuser).lower()

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
os.makedirs(folder_path, exist_ok=True)

username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

username = None

if os.path.exists(username_file):
    with open(username_file, 'r') as f:
        username = f.read()

if username is None:
    if hasattr(args, "username"):
        username = args.username

if username is None:
    print("Please use ``-u`` with your username...")
    sys.exit(25)

if len(str(username)) < 6:
    print("Please make your username 6 or more letters...")
    sys.exit(15)

if pre_makeuser == "true":
    makeuser = True
    response = requests.post("https://tea-pot.midori-ai.xyz/new_user_check", headers={"username": username})
        
    if response.status_code == 200:
        pass
    else:
        error_message = response.text
        print("Username is most likely taken, please pick a new username!")
        raise Exception(f"Server returned status code {response.status_code}: {error_message}")

else: 
    makeuser = False

if pre_unsafe == "true":
    print("UNSAFE MODE: True")
    print("UNSAFE MODE: Please note this is really unsafe and you could be banned from logging in")
    print("UNSAFE MODE: Only use this if you are a cluster member or if Midori AI asked you to...")
    unsafe = True
else: 
    unsafe = False

if pre_cli == "true":
    unsafe = True

key_one = Fernet.generate_key()

fernet_one = Fernet(key_one)

if not unsafe:
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

    hash_hex = hash_object.hexdigest()
    os_hash_hex = os_hash_object.hexdigest()

else:
    hash_hex = str(args.bypassplatform).lower()
    os_hash_hex = str(args.bypassoscheck).lower()

encrypted_platform_one = fernet_one.encrypt(str(hash_hex).encode())
encrypted_os_version_one = fernet_one.encrypt(str(os_hash_hex).encode())

if makeuser:
    invite_key = input("Please enter the invite key from Midori AI: ")
    try:
        response = requests.post("https://tea-pot.midori-ai.xyz/make_user_user", 
            headers=
            {
                "username": f"{str(username)}", 
                "invitekey": f"{str(invite_key)}", 
                "platform" : f"{encrypted_platform_one.decode()}", 
                "osversion" : f"{encrypted_os_version_one.decode()}", 
                "apiverison" : f"{key_one.decode()}"
            }, timeout=55
            )
        
        if response.status_code == 200:
            print("User Made Logging in!")
        else:
            error_message = response.text
            raise Exception(f"Server returned status code {response.status_code}: {error_message}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

try:
    response = requests.post("https://tea-pot.midori-ai.xyz/get_api_key_user", 
        headers=
        {
            "username": f"{str(username)}", 
            "platform" : f"{encrypted_platform_one.decode()}", 
            "osversion" : f"{encrypted_os_version_one.decode()}", 
            "apiverison" : f"{key_one.decode()}"
        }, timeout=55
        )
    
    if response.status_code == 200:
        api_key = response.text
        
        with open(api_key_file, "w") as f:
            f.write(api_key)
        
        with open(username_file, "w") as f:
            f.write(username)
        
        print(f"Now loged into Midori AI")

    else:
        error_message = response.text
        raise Exception(f"Server returned status code {response.status_code}: {error_message}")

except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)