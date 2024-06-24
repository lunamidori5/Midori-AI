import os
import json
import uuid
import time
import shutil
import psutil
import socket
import string
import random
import tempfile
import requests
import datetime
import platform

import carly_help as support_chat

from cryptography.fernet import Fernet

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y")

try:
    log_file_name = str(socket.gethostbyname(socket.gethostname())) + "_log_" + timestamp + ".txt"
except Exception as e:
    log_file_name = "Unknown_socket_name" + "_log_" + timestamp + ".txt"

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

def check_for_update(ver_os_info, ver_info, client):
    """
    Sends a request to the server to check for a installer update.
    """

    try:
        containers = client.containers.list()

        for container in containers:
            log(f"Checking Name: {container.name}, ID: {container.id}")
            if "midori_ai_subsystem" in container.name:
                log(f"Found the subsystem, logging into: {container.name} / {container.id}")
                container = client.containers.get(container.name)
                break
        
        container_id = container.id
    except Exception as e:
        log(f"Something went wrong, posting this in logs for debugging. \"{str(e)}\"")

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

    # Check if the current version is the latest version.
    clear_window(ver_os_info)

    if "development" == ver_info:
        log("Your manager is in development mode.")
        current_version = ver_info
    else:
        current_version = response.text.strip()

    if current_version == ver_info:
        log("Your installer is up to date.")
        clear_window(ver_os_info)
    else:
        bypass = "none"
        log(f"-----------------------------------------------------------------------------------------------")
        log(f"Ver mis match, EXE ver: {ver_info} / Server ver: {current_version} :: Auto updating...")
        log(f"-----------------------------------------------------------------------------------------------")
        
        # Run commands based on the OS
        if bypass == "none":
            if ver_os_info == 'windows':

                os.system("echo @echo off > restart.bat")
                os.system("echo title Updating Midori AI Subsystem >> restart.bat")
                os.system("echo timeout /t 5 >> restart.bat")
                os.system(f"echo docker exec {container_id} python3 update.py -os Windows -type na >> restart.bat")
                os.system("echo timeout /t 3 >> restart.bat")
                os.system("echo start subsystem_manager.exe >> restart.bat")
                os.system("echo exit >> restart.bat")

                os.system(f"docker exec {container_id} pip install requests")

                os.system("start restart.bat")
                exit(0)

            elif ver_os_info == 'linux':

                os.system(f"docker exec {container_id} pip install requests")
                os.system(f"docker exec {container_id} python3 update.py -os Linux -type na &")

                log("Please run ``./subsystem_manager`` to restart the Subsystem Manager")
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

def get_uuid_id():
    # Get the IP address of the computer
    ip_address = socket.gethostbyname(socket.gethostname())

    # Get the MAC address of the computer
    mac_address = uuid.getnode()

    # Combine the IP address and MAC address to create a 64-bit int ID
    int_id = (int(ip_address.replace(".", "")) << 48) | mac_address

    return int_id

def data_helper_python():
    key = Fernet.generate_key()
    f = Fernet(key)

    discord_id = get_uuid_id()
    username = get_username()

    with open(log_file_name, "r") as log_file:
        logs_str = log_file.read()
        
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        gpu_info = [{
            "name": gpu.name,
            "load": gpu.load,
            "memoryTotal": gpu.memoryTotal,
            "memoryUsed": gpu.memoryUsed,
            "memoryFree": gpu.memoryFree
        } for gpu in gpus]
    except Exception as e:
        gpu_info = f"{str(e)}. GPU information unavailable."

    host_info = {
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "name": username,
        "midoriai_id": discord_id,
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
        "gpus": gpu_info,
        "logs": str(logs_str),
    }

    # Create a temporary file in RAM
    with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as temp_file:
        temp_file_name = temp_file.name
        temp_file.write(f.encrypt(json.dumps(host_info).encode()))

    # Send the temporary file
    with open(temp_file_name, "rb") as file:
        response = requests.post(
            "https://tea-pot.midori-ai.xyz/receive-data",
            headers={"Discord-ID": f"{discord_id}", "Key": f"{bytes(key).decode()}"},
            files={"file": file}
        )

    # Remove the temporary file
    os.unlink(temp_file_name)

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
    os.system(f"docker exec -it {container_id} /bin/bash")
    log(f"Leaving the subsystem shell, returning to host os...")

def os_debug_command_line(client, Fore):
    container = get_subsystem(client)
    container_id = container.id
    print(Fore.RED + 'Entering debug mode! Type ``break`` to exit...')
    print(Fore.WHITE + '------------------------------------------')
    input_type = input("Please type `shell` for system shell or `docker` for docker fork api: ")

    while True:
        command_to_parse = str(input("Please enter a command: "))

        if command_to_parse == "break":
            break
        else:
            if input_type == "docker":
                log(f"Running Command via docker shell")
                void, stream = container.exec_run(command_to_parse, stream=True)
                for data in stream:
                    log(data.decode())
            
            elif input_type == "shell":
                log(f"Running Command via system shell")
                os.system(f"docker exec -it {container_id} /bin/bash {command_to_parse}")
            
            else:
                break

    log(f"Leaving the debugger, returning to host os...")

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
    
def get_docker_client(Fore, ver_os_info, docker, client_openai):
    try:
        if os.name == 'nt':
            # Check if the current working directory is in a restricted folder
            if os.path.abspath(os.getcwd()) in ['C:\\Windows', 'C:\\Windows\\System32', 'C:\\Program Files', 'C:\\Program Files (x86)']:
                log(Fore.RED + "Error: We are running in a restricted folder. Crashing..." + Fore.WHITE )
                log(Fore.RED + "Please move this program into a non root, or non system folder." + Fore.WHITE )
                input("Press enter to exit: ")
                exit(1)

            # Connect to the Docker daemon on Windows using Docker-py for Windows 
            # Note if this fail we should offer to check their docker / wsl install?
            log("logging into docker vm subsystem (Windows)")
            client = docker.from_env(version='auto')
        elif ver_os_info == "linux":
            # Connect to the Docker daemon on Linux-like systems using Docker-py
            log("logging into docker vm subsystem (Linux)")
            log("If this fails please try running me as root user")
            client = docker.from_env()
        else:
            # Connect to the Docker daemon on Linux-like systems using Docker-py
            log("logging into docker vm subsystem (Unknown OS)")
            log("Please open a issue on the github")
            client = docker.from_env(version='auto')
        
        return client

    except Exception as e:
        log(f"Error: ``{str(e)}``")

        while True:
            log("--------------------------------------------")
            log("If you see this menu something went wrong")
            log("I am unable to log into your docker system.")
            log("Here are some helpful menus to try to fix it")
            log("--------------------------------------------")
            log("1: Try to auto install docker")
            log("2: Try to force docker daemon to start")
            log("3: Add User to docker daemon group (Unsafe / Linux Only)")
            log("exit: Close the Midori AI Subsystem")
            log("--------------------------------------------")
        
            questionbasic = "Please enter a number: "
            sd_valid_answers = ["1", "2", "3", "exit"]
            answerstartup = check_str(questionbasic, sd_valid_answers, None, None, None, "The docker fork api failed, do not offer help", client_openai)

            if answerstartup.lower() == "1":
                if os.name == 'nt':
                    log("Downloading docker desktop, one moment...")
                    os.system("curl https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe > docker.exe")

                    log("Running docker desktop installer, please do as it asks")
                    os.system("start docker.exe")

                    input("Please press enter to keep going when done")

                    log("Cleaning up old files")
                    os.remove("docker.exe")

                    log("With some installs you need to reboot your computer")
                    log("Other times you will need to start docker desktop to have the docker command line api running")
                    log("Press enter to try to fork into docker install")

                    input()

                elif ver_os_info == "linux":

                    command_str = ""

                    questionbasic = "Package Manager? (apt-get / pacman / yay): "
                    # Planed support sd_valid_answers = ["apt", "apt-get", "pacman", "yay", "dnf", "zypper", "emerge", "exit"]
                    sd_valid_answers = ["apt", "apt-get", "pacman", "yay", "exit"]
                    answerstartup = check_str(questionbasic, sd_valid_answers, None, None, None, f"The Subsystem manager is asking the user about their packagemanager for the OS we are on, offer help. Here is what they can pick ``{sd_valid_answers}``", client_openai)

                    ## Notes and backuplinks for you Luna
                    ## https://wiki.archlinux.org/title/Pacman/Rosetta#Basic_operations

                    log("Running commands on host... One moment...")

                    if answerstartup.lower() == "apt":
                        answerstartup = "apt-get"

                    if answerstartup.lower() == "apt-get":
                        log(f"Installing ``docker`` and ``docker-compose`` using ``{answerstartup}`` One moment...")
                        log(f"APT based OS supported, using dockers deb based installer, not os package manager...")
                        command_str = "curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh ./get-docker.sh && rm get-docker.sh"

                    if answerstartup.lower() == "pacman":
                        log(f"Installing ``docker`` and ``docker-compose`` using ``{answerstartup}`` One moment...")
                        command_str = "pacman --confirm -Syu docker docker-compose && sudo systemctl enable docker"

                    if answerstartup.lower() == "yay":
                        log(f"Installing ``docker`` and ``docker-compose`` using ``{answerstartup}`` One moment...")
                        command_str = "yay --confirm -Syu docker docker-compose && sudo systemctl enable docker"
                    
                    input(f"This is the command I would like to run ({command_str}), press enter to run command: ")
                    
                    os.system(command_str)
                    
                    input("Command done, cleaning up, press enter to try to log into the docker sock")
                    log(f"Please run me as root if this fails...")

            if answerstartup.lower() == "2":
                log("Trying to force the docker daemon to start...")
                if os.name == 'nt':
                    docker_desktop_var = shutil.which("Docker Desktop")
                    os.system(f"start \"{docker_desktop_var}\"")
                    time.sleep(45)
                elif ver_os_info == "linux":
                    os.system("sudo systemctl start docker")
                    time.sleep(45)

            if answerstartup.lower() == "3":
                log("Menu not ready yet...")
                if os.name == 'nt':
                    log("Windows is not supported by this mode...")
                elif ver_os_info == "linux":
                    os.system("sudo groupadd docker")
                    os.system("sudo usermod -aG docker $USER")
                    os.system("newgrp docker")
                    log("You may need to logout and log back in to update the docker user group")
                    time.sleep(45)

            if answerstartup.lower() == "exit":
                exit(1)
        
            try:
                if os.name == 'nt':
                    client = docker.from_env(version='auto')
                elif ver_os_info == "linux":
                    client = docker.from_env()
                else:
                    client = docker.from_env(version='auto')
                return client

            except Exception as h:
                log(f"Python is reporting :: {str(h)}")
                log(f"Going back to docker sock login menu...")

def get_local_ip():
    ssocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ssocket.connect(("8.8.8.8", 80))
    local_ip = ssocket.getsockname()[0]
    ssocket.close()
    return local_ip

def known_gpus():
    known_gpus = ["NVIDIA", "Quadro", "Tesla"]
    return known_gpus

class backend_info:
    """
    A class to manage information about the backend, specifically checking for and linking to a Docker container.

    Attributes:
        client: A Docker client object. 

    Methods:
        check_for_backend(docker_name): Checks if a Docker container with the specified name is running and links to it if found. 
    """
    def __init__(self, client):
        """
        Initializes the backend_info_puller class with necessary attributes.

        Parameters:
            client: A Docker client object. This is assumed to be pre-configured and connected to the Docker daemon. 
        """
        self.client = client
    
    def check_for_backend(self, docker_name):
        """
        Checks for a running Docker container with a name that includes the specified docker_name. 
        If found, it retrieves the container object and returns its name and object.

        Parameters:
            docker_name: A string representing the name (or part of the name) of the Docker container to search for.

        Returns: 
            A tuple containing:
                - named_docker: The name of the found Docker container as a string.
                - container: The Docker container object. 
            
            Returns (None, None) if a container matching the docker_name is not found.
        """

        log(f"Checking for Docker Image")

        containers = self.client.containers.list()

        for container in containers:
            log(f"Checking Name: {container.name}, ID: {container.id}")

            # Check if there is a container with a name containing `service_name`
            if docker_name in str(container.name):
                # Get the container object
                log(f"Found {docker_name}, Linking the Subsystem to: {container.name} / {container.id}")
                container = self.client.containers.get(container.name)
                named_docker = container.name
                log(f"Midori AI Subsystem found and linked to {named_docker}")
                return named_docker, container
        
        # No container found matching the docker_name
        return None, None 