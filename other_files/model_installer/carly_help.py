import os
import time
import random
import requests
import platform

from cryptography.fernet import Fernet

import support as s
import setup_docker as docker_add_on
import setup_models as models_add_on
import edit_models as models_edit_add_on

def download_prompt(COMMAND_SITE_COMMANDS, discord_id):
    with requests.get(COMMAND_SITE_COMMANDS, headers={"Discord-ID": discord_id}) as response:
         if response.status_code == 200:
            return response.text  # Read binary data
         else:
            raise RuntimeError(f"Failed to download commands: {response.status_code}")


def download_keys(COMMAND_SITE_KEY, discord_id):
     with requests.get(COMMAND_SITE_KEY, headers={"Discord-ID": discord_id}) as response:
        if response.status_code == 200:
            return response.text  # Read text-based key
        else:
            raise RuntimeError(f"Failed to download keys: {response.status_code}")

def request_info(filename_pre):
    discord_id = str(random.randint(1, 99999999))

    base_url = "https://tea-cup.midori-ai.xyz/download/"
    filename = filename_pre
    key_filename = f"{discord_id}-key.txt"

    key_url = f"{base_url}{key_filename}"
    encrypted_file_url = f"{base_url}ai/{filename}"

    encrypted_commands = download_prompt(encrypted_file_url, discord_id)
    keys = download_keys(key_url, discord_id)

    fernet = Fernet(keys.encode())  # Create Fernet object with the key
    decrypted_commands = fernet.decrypt(encrypted_commands)

    system_message = bytes(decrypted_commands).decode()

    return system_message

def request_llm(client_openai, request_in, system_message):
    completion = client_openai.chat.completions.create(
    model="gpt-4.1-turbo",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": request_in}
    ],
    stream=True
    )

    end_message = ""

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            end_message = end_message + str(chunk.choices[0].delta.content)
            print(str(chunk.choices[0].delta.content), end="")

    return end_message

def carly(client_openai):
    #this is the main def for the carly api requests

    os_info = platform.system()

    # Set the ver_os_info variable accordingly.
    if os_info == "Windows":
        ver_os_info = "windows"
        os.system('title Chat with Carly')
    elif os_info == "Linux":
        ver_os_info = "linux"
    else:
        s.log(f"Unsupported operating system: {os_info}")

    chat_room(request_info("system_prompt.txt"), client_openai, ver_os_info)
    return

def chat_room(system_message, client_openai, ver_os_info):
    s.log("Starting the chat room")
    s.log("WARNING THIS CHAT ROOM AS NO CONTEXT YET. \nDO NOT ASK QUESTIONS ABOUT THE MANAGER THANK YOU!")
    while True:
        s.log("Input Message: ")
        message = input()
        s.log("Carly is typing...")
        reply = request_llm(client_openai, message, system_message)
        s.clear_window(ver_os_info)
        s.log(reply)