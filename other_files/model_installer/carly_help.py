import os
import time
import json
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

def request_llm(client_openai, request_in, system_message, added_context):
    temp_str_memory = "There was a really big error..."

    if os.path.exists("memory.ram"):
        for i in range(5):
            try:
                with open('memory.ram', 'r') as jsonfile:
                    session_inside = json.load(jsonfile)

                message_gpt = [
                        *session_inside,
                        {"role": "user", "content": "Please Summarize these conversations into one paragraph. You may add, remove, or forget somethings as you see fit."}]

                messages = [{" role": msg["role"], "content": msg["content"]} for msg in message_gpt]

                completion = client_openai.create(
                model="gpt-14b-carly",
                messages=messages
                )
                temp_str_memory = str(list(client_openai.extract_text_or_completion_object(completion))[0]).strip()
                session_inside = []
                break

            except:
                continue

    else:
        session_inside = []
        temp_str_memory = "Carly has just meet these user... This is a new chat!"
    
    message_gpt = [
            {"role": "system", "content": system_message},
            {"role": "system", "content": temp_str_memory},
            {"role": "system", "content": added_context},
            {"role": "user", "content": request_in}
            ]

    messages = [{"role": msg["role"], "content": msg["content"]} for msg in message_gpt]

    for i in range(5):
        try:
            completion = client_openai.create(
            model="gpt-14b-carly",
            messages=messages
            )
            break

        except:
            continue

    end_message = str(list(client_openai.extract_text_or_completion_object(completion))[0]).strip()

    print(client_openai.extract_text_or_completion_object(completion))

    print(f"Trying to save memory...")
    session_inside.append({"role": "memory", "content": f"The User said ``{request_in}``"})
    session_inside.append({"role": "assistant", "content": f"Carly replied with ``{end_message}``"})

    with open('memory.ram', 'w') as jsonfile:
        json.dump(session_inside, jsonfile)

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

    chat_room(request_info("system_prompt.txt"), client_openai, ver_os_info, "This is a open chat room with Carly, no added context is needed.")
    return

def chat_room(system_message, client_openai, ver_os_info, added_context):
    s.log("Dev Note: This copy of Carly will get some context of your setup using the Subsystem Manager")
    s.log("Dev Note: She can not however help you install, setup, or other tasks with non supported models.")
    s.log("Dev Note: Questions like ``how to install xzy model`` will make her make something up.")
    s.log("Dev Note: I am fully remaking this Subsystem manager api and am deeply sorry for the delay.")
    s.log("``Carly's servers are running in low power mode... Sorry for the slow replys`` - Luna")
    s.log("Input Question: ")
    message = input()
    s.log("Carly is thinking...")
    requested_context = added_context
    reply = request_llm(client_openai, message, system_message, requested_context)
    s.clear_window(ver_os_info)
    s.log(reply)