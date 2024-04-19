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

from cryptography.fernet import Fernet

localai_ver_number = "v2.9.0"
base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y")
log_file_name = str(socket.gethostbyname(socket.gethostname())) + "_log_" + timestamp + ".txt"

ver_file_name = "midori_program_ver.txt"

def remove_non_printable_chars(input_string):
    printable_chars = set(string.printable)
    cleaned_string = ''.join(char for char in input_string if char in printable_chars)
    return cleaned_string

def log(message):
    # Read the current contents of  the file
    if os.path.exists(log_file_name):
        with open(log_file_name, "r") as f:
            contents = f.read()
    else:
        contents = "This is the start of a new log"
    
    message = remove_non_printable_chars(str(message).strip())

    print(str(message))

    contents += "\n" + str(message)

    # Resave the file
    with open(log_file_name, "w") as f:
        f.write(contents)

def download_commands(site_url, discord_id):
    response = requests.get(site_url, headers={"Discord-ID": discord_id})
    if response.status_code == 200:
        return response.content  # Read binary data
    else:
        raise RuntimeError(f"Failed to download commands: {response.status_code}")

def clear_window(ver_os):
    if ver_os == 'windows':
        os.system('cls')
    if ver_os == 'linux':
        os.system('clear')
        
def repair_clean_up():
    files = os.listdir("files")

    for file in files:
        if "ram" in file:
            os.remove(os.path.join("files", file))
        if "txt" in file:
            os.remove(os.path.join("files", file))

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
                break
        
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
        log(f"Ver mis match, EXE ver: {ver_info} / Server ver: {current_version}")
        log(f"-----------------------------------------------------------------------------------------------")
        log(f"A update is available. Auto updating...")
        log(f"-----------------------------------------------------------------------------------------------")
        
        # Run commands based on the OS
        if bypass == "none":
            if ver_os_info == 'windows':
                os.system("del subsystem_manager.zip")
                os.system("del subsystem_manager.exe")
                os.system("del model_installer.bat")
                os.system(f"curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/shell_files/model_installer.bat -o model_installer.bat && start model_installer.bat")
                log(f"If the subsystem manager failed to start, just run ``call model_installer.bat``")
            elif ver_os_info == 'linux':
                os.system("rm -f subsystem_manager.tar.gz subsystem_manager model_installer.sh")
                os.system(f"curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/shell_files/model_installer.sh | sh")
                log(f"If the subsystem manager failed to start, just run ``./model_installer.sh``")

        exit(0)

def check_for_subsystem_update(ver_os_info, ver_info, DockerClient, compose_path, containers, use_gui, sg, client, localai_ver_number, layout, client_openai, discord_id, subsystem_file_name):
    """
    Sends a request to the server to check for a installer update.
    """

    if os.path.exists(os.path.join("files", subsystem_file_name)):
        with open(os.path.join("files", subsystem_file_name), "r") as f:
            response = f.read()
    else:
        response = "nul"

    # Get the current model version.
    current_version = response.strip()

    # Check if the current version is the latest version.
    clear_window(ver_os_info)

    if current_version == ver_info:
        log("Your subsystem is up to date.")
    else:
        bypass = "none"
        import setup_docker as docker_add_on
        log(f"-----------------------------------------------------------------------------------------------")
        log(f"A subsystem update is available. Auto updating...")
        log(f"-----------------------------------------------------------------------------------------------")
        docker_add_on.dev_setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, client, localai_ver_number, layout, client_openai, discord_id, subsystem_file_name)

def get_os_info():
    # Get the operating system.
    os_info = platform.system()

    # Set the ver_os_info variable accordingly.
    if os_info == "Windows":
        ver_os_info = "windows"
        os.system('title Midori AI Subsystem Manager')
    elif os_info == "Linux":
        ver_os_info = "linux"
    else:
        ver_os_info = "unknown"
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
        return

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
                    log(f"\nIf you need help, please type ``help``.\n")

class backends_checking():
    def load_installed_backends(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def save_installed_backends(self, path, backends):
        with open(path, 'w') as f:
            json.dump(backends, f, indent=2)
    
    def check_json(self):
        path = os.path.join("files", "backends.json")
        if os.path.exists(path):
            backends = self.load_installed_backends(path)
        else:
            backends = []
            self.save_installed_backends(path, backends)
        return backends
    
    def add_backend(self, backend):
        path = os.path.join("files", "backends.json")
        known_backends = self.check_json()
        known_backends.append(backend)
        self.save_installed_backends(path, known_backends)

    def remove_backend(self, backend):
        path =  os.path.join("files", "backends.json")
        known_backends = self.check_json()
        if backend in known_backends:
            known_backends.remove(backend)
            self.save_installed_backends(path, known_backends)

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
        response = requests.post("https://tea-cup.midori-ai.xyz/receive-data", headers={"Discord-ID": f"{username}", "Key": f"{bytes(key).decode()}"}, files={"file": file})

    os.remove("encrypted_data.txt")

def get_subsystem(client):
    containers = client.containers.list()
    for container in containers:
        service_name = "midori_ai_subsystem"
        log(f"Checking Name: {container.name}, ID: {container.id}")

        # Check if there is a container with a name containing `service_name`
        if service_name in str(container.name):
            # Get the container object
            log(f"Found subsystem, logging into: {container.name} / {container.id}")
            container = client.containers.get(container.name)
            return container
        
    log("If you are seeing this message, the program will crash...")

def os_support_command_line(client, Fore):
    container = get_subsystem(client)
    container_id = container.id
    print(Fore.RED + 'Entering subsystem shell! Type ``Exit`` to exit...')
    print(Fore.WHITE + '------------------------------------------')
    input("Press enter to start the shell...")
    os.system(f"docker exec -it {container_id} /bin/tmux")
    log(f"Leaving the subsystem shell, returning to host os...")

def get_port_number(backend_request):
    if backend_request == "localai":
        return 38080
    if backend_request == "anythingllm":
        return 33001
    if backend_request == "ollama":
        return 11434
    if backend_request == "oobabooga":
        ## needs ports 7860 and 5000
        return 7860
    if backend_request == "oobaboogaapi":
        ## needs ports 7860 and 5000
        return 5000
    if backend_request == "invokeai":
        return 9090
    if backend_request == "home assistant":
        return 8123