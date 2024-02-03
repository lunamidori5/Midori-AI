import os
import time
import random
import requests

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

def request_system_message():
    discord_id = str(random.randint(1, 99999999))

    base_url = "https://tea-cup.midori-ai.xyz/download/"
    filename = "system_prompt.txt"
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
    
    s.log(end_message)

    return end_message

def carly(client_openai):
    #this is the main def for the carly api requests
    system_message = request_system_message()
    chat_room(system_message, client_openai)
    return

def chat_room(system_message, client_openai):
    s.log("Starting the chat room")
    while True:
        s.log("Hello please type a message to Carly: ")
        message = input()
        reply = request_llm(client_openai, message, system_message)
        s.log(reply)