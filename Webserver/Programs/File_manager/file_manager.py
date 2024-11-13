import os
import sys
import json
import hashlib
import platform
import argparse
import requests

from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description="File manager for packing, unpacking, uploading, and downloading files and folders to / from Midori AI\'s servers")
parser.add_argument("-i", "--item", required=True, type=str, help="File / Folder being packed / unpacked")
parser.add_argument("-t", "--type", required=True, type=str, help="Type of Item (file or folder)")
parser.add_argument("-a", "--action", required=True, type=str, help="Action to perform (pack, unpack, upload, download)")
args = parser.parse_args()

item = str(args.item).lower()
item_type = str(args.type).lower()
action = str(args.action).lower()

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
os.makedirs(folder_path, exist_ok=True)

username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

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