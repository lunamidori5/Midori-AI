import os
import time
import random
import asyncio
import argparse
import requests
import datetime
import subprocess

from tqdm import tqdm

from rich import print

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

async def get_api_key():
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

        try:
            subprocess.call(["midori_ai_login"])
            await asyncio.sleep(2)
        except Exception as error:
            print("Login failed, please try again manually")
            print("API KEY not set, please log into Midori AI's Servers")
            print("Run ``midori_ai_login -u \"username\"``")

            print("Encrypted endpoint is turned off, please login to use it...")
            print("BYPASSING Encrypted endpoint is turned ON, we are working on updating our CLI tools...")
            
            api_key = str(random.randint(999999, 99999999999999))
            break

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
    headers = {"Discord-ID": random_id, "username": f"{str(username)}", "key": str(await get_api_key())}
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


async def acquire_files_with_streaming(FILES):
    chunk_size = 1024 * 1024 * 2
    filename = f"temp_download_{random.randint(1000, 10000)}.tmp"
    
    try:
        response = requests.get(FILES, headers={"Discord-ID": random_id, "username": f"{str(username)}", "key": str(await get_api_key())}, stream=True, timeout=55)
        response.raise_for_status()

        total_size = int(response.headers.get("Content-Length", 0))
        
        with open(filename, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading File') as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

        with open(filename, "rb") as f:
            content = f.read()
        os.remove(filename)
        return content

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Download failed: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

def log(message):
    print(message)

    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

async def main():

    parser = argparse.ArgumentParser(description="Download and decrypt a file.")
    parser.add_argument("filename", help="The filename to download.")
    parser.add_argument("-o", "--output", help="The output filename.")
    parser.add_argument("-u", "--usermode", action="store_true", help="Enters user mode")
    parser.add_argument("-un", "--unsafe", required=False, action='store_true', help="Enable unsafe mode")
    args = parser.parse_args()

    base_url = "https://tea-cup.midori-ai.xyz/download/"
    filename = args.filename
    usermode = bool(args.usermode)
    pre_unsafe = bool(args.unsafe)
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

    max_retries = 18
    use_backup = usermode or pre_unsafe or ".gguf" in filename or not is_api_key_loaded()

    if usermode: backup_file_url = usermode_file_url;

    for attempt in range(max_retries):
        try:
            if attempt > 15 or use_backup:
                download_url = backup_file_url if backup_file_url else encrypted_file_url
                downloaded_data = await acquire_files_with_streaming(download_url)
                log("Downloaded using backup/direct method.")
            elif attempt > 5:
                downloaded_data = await download_files(encrypted_file_url)
            else:
                downloaded_data = await acquire_files_with_streaming(encrypted_file_url)

            if not use_backup:
                keys = await download_keys(key_url)
                fernet = Fernet(keys.encode())
                downloaded_data = fernet.decrypt(downloaded_data)
                log("File downloaded and decrypted successfully.")
            else:
                if not backup_file_url:
                    raise Exception("Backup download attempted but no backup URL provided.")

            if args and args.output:
                filename = args.output

            with open(filename, "wb") as f:
                f.write(downloaded_data)

            log(f"File saved: {filename}")  # Log the filename always
            break  # Exit the function on success

        except Exception as e:
            log(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            await asyncio.sleep(0.2)


if __name__ == "__main__":
    asyncio.run(main())