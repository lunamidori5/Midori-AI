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

try:
    discord_id = os.getenv("DISCORD_ID")
except:
    discord_id = str(random.randint(999999, 99999999999999))

if discord_id == None:
    discord_id = str(random.randint(999999, 99999999999999))

api_key = None
api_key_file = "MIDORI_AI_API_KEY_TEMP"
attempt_count = 0

while api_key == None:

    now = datetime.datetime.now()

    if os.path.exists(api_key_file):
        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(api_key_file))

        time_since_modified = now - last_modified

        if time_since_modified.total_seconds() > 200:
            os.remove(api_key_file)
        else:
            with open(api_key_file, 'r') as f:
                api_key = f.read()
            break

    if attempt_count > 1:
        print("Login failed, please try again manually")
        print("API KEY not set, please log into Midori AI's Servers")
        print("Run ``midori-ai-login -u \"username\"``")

        print("Fallback code running for now, setting api to random int")
        api_key = str(random.randint(999999, 99999999999999))
        break

        #print("Exiting...")
        #exit(1)
    
    try:
        subprocess.call(["midori-ai-login"])
    except Exception:
        print("Midori AI login failed, please try again")

    attempt_count += 1

async def download_commands(COMMAND_SITE_COMMANDS):
    log(f"Attempting to download commands from {COMMAND_SITE_COMMANDS}")
    headers = {"Discord-ID": discord_id, "api_key": api_key}
    async with ClientSession() as session:
        async with session.get(COMMAND_SITE_COMMANDS, headers=headers) as response:
            if response.status == 200:
                log(f"Successfully downloaded {len(await response.read())} bytes of commands")
                return await response.read()  # Read binary data
            else:
                raise RuntimeError(f"Failed to download commands: {response.status}")

async def download_keys(COMMAND_SITE_KEY):
    log(f"Attempting to download keys from {COMMAND_SITE_KEY}")
    headers = {"Discord-ID": discord_id, "api_key": api_key}
    async with ClientSession() as session:
        async with session.get(COMMAND_SITE_KEY, headers=headers) as response:
            if response.status == 200:
                log(f"Successfully downloaded {len(await response.text())} bytes of keys")
                return await response.text()  # Read text-based key
            else:
                raise RuntimeError(f"Failed to download keys: {response.status}")


def download_commands_new(COMMAND_SITE_COMMANDS):
    response = requests.get(COMMAND_SITE_COMMANDS, headers={"Discord-ID": discord_id, "api_key": api_key}, stream=True)

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
    print(message)  # Print message to the screen

    with open("log.txt", "a") as log_file:  # Open "log.txt" in append mode
        log_file.write(message + "\n")  # Append message to the file with a newline

async def main():

    parser = argparse.ArgumentParser(description="Download and decrypt a file.")
    parser.add_argument("filename", help="The filename to download.")
    parser.add_argument("-o", "--output", help="The output filename.")
    args = parser.parse_args()

    base_url = "https://tea-cup.midori-ai.xyz/download/"
    filename = args.filename
    key_filename = f"{discord_id}-key.txt"

    if os.path.exists(args.output or filename):
        log(f"File Already Downloaded, removing file and redownloading...")
        if args.output:
            os.remove(args.output)
        else:
            os.remove(filename)

    # Download the key file
    key_url = f"{base_url}{key_filename}"
    encrypted_file_url = f"{base_url}ai/{filename}"
    backup_file_url = f"{base_url}{filename}"


    if ".gguf" in filename:
        trys = 16
        log(f"Trying to download - {backup_file_url}")
    else:
        trys = 0
        log(f"Trying to download - {encrypted_file_url} with the key of {key_url}")

    # Download commands and keys
    while trys < 18:
        try:
            log(f"Try number: {trys}")
            if trys > 15:
                log("Trying to download normal file")
                backup_commands = download_commands_new(backup_file_url)

                with open(filename, "wb") as f:
                    f.write(backup_commands)

                log("File downloaded successfully")
                break

            if trys > 5:
                log("Trying to download encrypted file")
                encrypted_commands = await download_commands(encrypted_file_url)
            else:
                log("Trying to download encrypted file (new method)")
                encrypted_commands = download_commands_new(encrypted_file_url)

            log("Encrypted file downloaded successfully")
            keys = await download_keys(key_url)
            log("Keys downloaded successfully")
            time.sleep(1)

            # Decrypt commands
            log("Decrypting file")
            fernet = Fernet(keys.encode())  # Create Fernet object with the key
            decrypted_commands = fernet.decrypt(encrypted_commands)

            if args.output:
                filename = args.output

            with open(filename, "wb") as f:
                f.write(decrypted_commands)

            log(f"File decrypted successfully: {filename}")

            break
        except Exception as e:
            log(f"Error: {str(e)}")
            trys = trys + 1
            time.sleep(0.2)


if __name__ == "__main__":
    asyncio.run(main())