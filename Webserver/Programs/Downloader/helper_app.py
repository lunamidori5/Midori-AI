import os
import time
import random
import asyncio
import argparse
import requests
import datetime
import subprocess

from tqdm import tqdm

from aiohttp import ClientSession
from cryptography.fernet import Fernet

random_id = os.getenv("random_id")

if random_id == None:
    random_id = str(random.randint(999999, 99999999999999))

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
os.makedirs(folder_path, exist_ok=True)
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")
username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")

username = "unknown_user"

if os.path.exists(username_file):
    with open(username_file, 'r') as f:
        username = f.read()

def get_api_key():
    api_key = None
    attempt_count = 0

    while api_key == None:

        now = datetime.datetime.now()

        if os.path.exists(api_key_file):
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(api_key_file))

            time_since_modified = now - last_modified

            if time_since_modified.total_seconds() > 600:
                os.remove(api_key_file)
            else:
                with open(api_key_file, 'r') as f:
                    api_key = f.read()
                break

        if attempt_count > 1:
            print("Login failed, please try again manually")
            print("API KEY not set, please log into Midori AI's Servers")
            print("Run ``midori-ai-login -u \"username\"``")

            print("Encrypted endpoint is turned off, please login to use it...")
            api_key = str(random.randint(999999, 99999999999999))
            break

            #print("Exiting...")
            #exit(1)

        try:
            subprocess.call(["midori-ai-login"])
        except Exception as error:
            print(f"Midori AI login failed ({str(error)}), please try again")

        attempt_count += 1

    return api_key

def is_api_key_loaded():
    home_dir = os.path.expanduser("~")
    folder_path = os.path.join(home_dir, ".midoriai")
    api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

    if os.path.exists(api_key_file):
        return True
    else:
        return True
        #return False

async def download_files(FILES):
    headers = {"Discord-ID": random_id, "username": f"{str(username)}", "key": get_api_key()}
    async with ClientSession() as session:
        async with session.get(FILES, headers=headers) as response:
            if response.status == 200:
                log(f"Successfully downloaded {len(await response.read())} bytes of files")
                return await response.read()
            else:
                raise RuntimeError(f"Failed to download files: {response.status}")

async def download_keys(KEY):
    headers = {"Discord-ID": random_id, "key": get_api_key()}
    async with ClientSession() as session:
        async with session.get(KEY, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise RuntimeError(f"Failed to download keys: {response.status}")


def acquire_files_with_streaming(FILES):
    response = requests.get(FILES, headers={"Discord-ID": random_id, "username": f"{str(username)}", "key": get_api_key()}, stream=True, timeout=55)

    if response.status_code == 200:
        total_size = int(response.headers.get("Content-Length", 0))
        content = b''
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading File') as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    pbar.update(len(chunk))
                    content += chunk
        return content
    else:
        raise RuntimeError(f"Failed to download File: {response.status_code}")


def log(message):
    print(message)

    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

async def main():

    parser = argparse.ArgumentParser(description="Download and decrypt a file.")
    parser.add_argument("filename", help="The filename to download.")
    parser.add_argument("-o", "--output", help="The output filename.")
    parser.add_argument("-u", "--usermode", action="store_true", help="Enters user mode")
    args = parser.parse_args()

    base_url = "https://tea-cup.midori-ai.xyz/download/"
    filename = args.filename
    key_filename = f"{random_id}-key.txt"

    if os.path.exists(args.output or filename):
        log(f"File Already Downloaded, removing file and redownloading...")
        if args.output:
            os.remove(args.output)
        else:
            os.remove(filename)

    key_url = f"{base_url}{key_filename}"
    encrypted_file_url = f"{base_url}ai/{filename}"
    usermode_file_url = f"{base_url}user"
    backup_file_url = f"{base_url}{filename}"

    if args.usermode:
        trys = 16
        backup_file_url = usermode_file_url

    if ".gguf" in filename:
        trys = 16
    else:
        trys = 0

    if not is_api_key_loaded():
        trys = 16
        
    while trys < 18:
        try:
            if trys > 15:
                backup_commands = acquire_files_with_streaming(backup_file_url)

                if args.output:
                    filename = args.output

                with open(filename, "wb") as f:
                    f.write(backup_commands)

                log("File downloaded successfully")
                break

            if trys > 5:
                encrypted_commands = await download_files(encrypted_file_url)
            else:
                encrypted_commands = acquire_files_with_streaming(encrypted_file_url)
                
            keys = await download_keys(key_url)
            time.sleep(1)

            fernet = Fernet(keys.encode())
            decrypted_commands = fernet.decrypt(encrypted_commands)

            if args.output:
                filename = args.output

            with open(filename, "wb") as f:
                f.write(decrypted_commands)

            log(f"File downloaded and decrypted successfully: {filename}")

            break
        except Exception as e:
            log(f"Error: {str(e)}")
            trys = trys + 1
            time.sleep(0.2)


if __name__ == "__main__":
    asyncio.run(main())