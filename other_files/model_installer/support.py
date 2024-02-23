import os
import json
import shutil
import psutil
import socket
import string
import random
import requests
import datetime
import platform

import carly_help as support_chat

from cpuinfo import get_cpu_info
from cryptography.fernet import Fernet
from multiprocessing import freeze_support

localai_ver_number = "v2.7.0"
base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y%H")
log_file_name = "log_" + timestamp + ".txt"

ver_file_name = "midori_program_ver.txt"

with open(log_file_name, "w") as f:
    f.write("Booted and Running Model Installer")

def remove_non_printable_chars(input_string):
    printable_chars = set(string.printable)
    cleaned_string = ''.join(char for char in input_string if char in printable_chars)
    return cleaned_string

def log(message):
    # Read the current contents of  the file
    with open(log_file_name, "r") as f:
        contents = f.read()
    
    message = remove_non_printable_chars(str(message).strip())

    print(str(message))

    contents += "\n" + str(message)

    # Resave the file
    with open(log_file_name, "w") as f:
        f.write(contents)

def clear_window(ver_os):
    log("Clearing the screen")
    if ver_os == 'windows':
        os.system('cls')
    if ver_os == 'linux':
        os.system('clear')

def check_for_update(ver_os_info, ver_info):
    """
    Sends a request to the server to check for a installer update.
    """
    placeholder_link = f"https://io.midori-ai.xyz/howtos/easy-model-installer/"

    servers_replyed = True

    retry = 0

    while retry < 15:
        # Send a request to the server for the model version.
        response = requests.get("https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt")

        # Check if the request was successful.
        if response.status_code != 200:
            log(f"Servers seem to be down, please try again in a moment...")
            servers_replyed = False
            retry = retry + 1
            if retry > 10:
                exit(404)
        
        if servers_replyed:
            break

    # Get the current model version.
    current_version = response.text.strip()

    # Check if the current version is the latest version.
    clear_window(ver_os_info)

    if current_version == ver_info:
        log("Your installer is up to date.")
        clear_window(ver_os_info)
    else:
        bypass = "none"
        log(f"-----------------------------------------------------------------------------------------------")
        log(f"A update is available. Auto updating...")
        log(f"-----------------------------------------------------------------------------------------------")
        
        # Run commands based on the OS
        if bypass == "none":
            if ver_os_info == 'windows':
                os.system("del model_installer.zip")
                os.system("del model_installer.exe")
                os.system("del model_installer.bat")
                os.system(f"curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/model_installer.bat -o model_installer.bat && start model_installer.bat")
                log(f"If the localai manager failed to start, just run ``call model_installer.bat``")
            elif ver_os_info == 'linux':
                os.system("rm -f model_installer.tar.gz model_installer model_installer.sh")
                os.system(f"curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/model_installer.sh | sh")
                log(f"If the localai manager failed to start, just run ``./model_installer.sh``")

        exit(0)

def check_cpu_support():

    freeze_support()

    info = get_cpu_info()

    log(info)

    info = str(info).lower()

    log(info)

    # Check if the CPU supports F16C
    if "f16c" not in info:
        log("f16c failed check")
        return True

    # Check if  the CPU supports AVX512
    if "avx512" not in info:
        log("avx512 failed check")
        log("overriding failed avx512 check")
        log("avx512 found (OVERRIDE)")

    # Check if the CPU supports AVX2
    if "avx2" not in info:
        log("avx2 failed check")
        return True

    # Check if the CPU supports AVX
    if "avx" not in info:
        log("avx failed check")
        return True

    # Check if the CPU supports FMA
    if "fma" not in info:
        log("fma failed check")
        return True

    # If all checks pass, return False
    return False

def get_os_info():
    # Get the operating system.
    os_info = platform.system()

    # Set the ver_os_info variable accordingly.
    if os_info == "Windows":
        ver_os_info = "windows"
        os.system('title LocalAI Manager')
    elif os_info == "Linux":
        ver_os_info = "linux"
    else:
        log(f"Unsupported operating system: {os_info}")
    
    return ver_os_info

def check_model_ids_file():
    """Downloads a file from a server and loads it into a list 1 line at a time.

    Args:
    url: The URL of the  file to download.

    Returns:
    A list of the lines in the file.
    """

    # Download the file.
    response = requests.get("https://tea-cup.midori-ai.xyz/download/model_list.txt")

    # Check if the request was successful.
    if response.status_code != 200:
        log(f"Servers seem to be down, please try again in a moment...")
        exit(418)

    # Load the file into a list.
    lines = [] 
    for line in response.iter_lines():
        lines.append(line.decode("utf-8"))

    # Return the list.
    return lines

def check_str(question, valid_answers, use_gui="no", layout=None, sg=None, support_context="Oops context missing", client_openai=None):
    """
    Checks if the user input is valid.

    Args:
    question: The  question to ask the user.
    valid_answers:  A list of valid answers.

    Returns:
    The user's input if it is valid, or None otherwise.
    """

    if use_gui == "yes":
        window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=False, resizable=True, margins=(0,0), use_custom_titlebar=True, finalize=True, keep_on_top=True)

        while True:     # The Event Loop
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                break
            if event == 'SEND':
                query = str(values['-QUERY-'].rstrip())
                if query in valid_answers:
                    log(f"I asked {question} / you replied {query}")
                    window.close()
                    return query

        window.close()

    else:
        while True:
            answer = input(f"\n{question}\n").lower()
            if answer in valid_answers:
                log(f"I asked {question} / you replied {answer}")
                return answer
            else:
                if answer == "help":
                    ver_os_info = get_os_info()
                    support_chat.chat_room(support_chat.request_info("system_prompt.txt"), client_openai, ver_os_info, support_context)
                else:
                    log(f"\nInvalid input. Please enter one of the following: {', '.join(valid_answers)}\n")
                    log(f"\nIf you need help, please type ``help`` or restart the program and type ``support`` into the main menu.\n")

def get_username():
    """
    Get the username of the computer.

    Returns: 
        str: The username of the computer.
    """
    if os.name == "nt":
        username = os.getenv("USERNAME")
    else:
        username = os.getenv("USER")

    return username

def data_helper_python():
    discord_id_pre = str(random.randint(1, 99999999))
    key = Fernet.generate_key()
    f = Fernet(key)

    discord_id = int(discord_id_pre)
    username = get_username()

    with open(log_file_name, "r") as log_file:
        logs_str = log_file.read()

    host_info = {
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "name": username,
        "discord_id": discord_id,
        "computer_type": platform.machine(),
        "os_name": platform.system(),
        "os_version": platform.release(),
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_total": psutil.virtual_memory().total,
        "memory_used": psutil.virtual_memory().used,
        "disk_total": shutil.disk_usage("/").total,
        "disk_used": shutil.disk_usage("/").used,
        "disk_free_space": shutil.disk_usage("/").free,
        "ssh_installed": shutil.which("ssh"),
        "docker_installed": shutil.which("docker"),
        "python_installed": shutil.which("python"),
        "pip_installed": shutil.which("pip"),
        "logs": str(logs_str),
    }

    encrypted_data = f.encrypt(json.dumps(host_info).encode())

    with open("encrypted_data.txt", "wb") as file:
        file.write(encrypted_data)

    with open("encrypted_data.txt", "rb") as file:
        response = requests.post("https://tea-cup.midori-ai.xyz/receive-data", headers={"Discord-ID": f"manager_program", "Key": f"{bytes(key).decode()}"}, files={"file": file})

    os.remove("encrypted_data.txt")