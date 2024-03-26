import os
import json
import yaml
import docker
import requests
import datetime

import support as s

import carly_help as help_add_on
import setup_docker as docker_add_on
import setup_models as models_add_on
import edit_models as models_edit_add_on

from colorama import Fore

from autogen import OpenAIWrapper

from cpuinfo import get_cpu_info
from multiprocessing import freeze_support

from python_on_whales import DockerClient
from python_on_whales import docker as docker_two

use_cuda = "False"
use_tts = "False"
use_core = "False"

missing_cuda = True
missing_cuda_toolkit = True

layout = None
sg = None

compose_path = "localai-docker-compose.yaml"
compose_backup_path = "docker-compose.yaml"

localai_ver_number = "v2.8.0"
base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

answer_backup_compose ="no"

ver_info = "changemelunaplease"

ver_file_name = "midori_program_ver.txt"

about_model_size = str("""
7b - Recommend for lowerend PC (6gb of Vram or less / 10gb of system ram) - https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF
2x7b - Recommended for home PC (8gb or more of Vram needed / 25gb of system ram) - (**Is removed for the time being**)
8x7b - Recommended for highend PC (24gb or more Vram needed / 55gb of system ram) - https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF
70b - Recommended for high end servers only (AI card or better with 48gb Vram + 100gb system ram) - https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF
ID - (These are models from the Midori AI model repo) - https://io.midori-ai.xyz/models/offsite_models/
Base - Models that are baked into LocalAI - https://localai.io/basics/getting_started/
""")

about_model_q_size = str("""
| Quant Mode | Description |
|Q3| Smallest, significant quality loss - not recommended|
|Q4| Medium, balanced quality|
|Q5| Large, very low quality loss - recommended for most users|
|Q6| Very large, extremely low quality loss|
|Q8| Extremely large, extremely low quality loss, hard to use - not recommended|
|None| Extremely large, No quality loss, super hard to use - really not recommended|
                         
If unsure what you need, type ``q5``

Note: 
That some models may deviate from our conventional model formatting standards (Quantized/Non-Quantized), 
and will be served using a rounding-down approach. For instance, if you request a Q8 model and none is available, 
the Q6 model will be served instead, and so on.
""")

if os.name == 'nt':
    os.system("del model_installer.zip")
    os.system("del subsystem_manager.zip")
    os.system("del model_installer.bat")
    os.system("del model_installer.exe")
else:
    os.system("rm -f model_installer_linux.tar.gz")
    os.system("rm -f subsystem_manager.tar.gz")
    os.system("rm -f model_installer")

response_git = requests.get("https://github.com/lunamidori5/Midori-AI/blob/b9a74490f5b5ad0ecce56dbd7718fab3e31ece1b/data/version.json")

if response_git.status_code != 200:
    s.log(f"Github seem to be down, please try again in a moment...")
    exit(418)

current_version_git = response_git.text.strip()

s.log("I am setting up a temp copy of Carly...")
temp_response = help_add_on.request_info("temp_something_for_model_installer.txt")
temp_keys = temp_response.strip()
client_openai = OpenAIWrapper(base_url="https://ai.midori-ai.xyz/v1", api_key=temp_keys, timeout=6000)

ver_os_info = s.get_os_info()
backend_checker = s.backends_checking()

os.makedirs("files", exist_ok=True)

if ver_os_info == "linux":
    os.chmod("files", 0o777)

try:
    if os.name == 'nt':
        # Connect to the Docker daemon on Windows using Docker-py for Windows 
        s.log("logging into docker vm subsystem (Windows)")
        client = docker.from_env(version='auto')
    else:
        # Connect to the Docker daemon on Linux-like systems using Docker-py
        s.log("logging into docker vm subsystem (Linux)")
        s.log("If this fails please try running me as root user")
        client = docker.from_env()

except Exception as e:
    s.log("Looks like I was unable to log into the docker subsystem...")
    s.log("Do you have docker installed? / Please try running me as root user, Linux users.")
    input("Please press enter to exit: ")
    exit(1)

# List all containers
s.clear_window(ver_os_info)

s.check_for_update(ver_os_info, ver_info)

s.clear_window(ver_os_info)

s.data_helper_python()

backend_menu = models_add_on.backend_programs_manager(ver_os_info, client, about_model_size, about_model_q_size, client_openai)

use_gui = "no"
dev_mode = True
login_midori_ai = False
dash = '~'
num_dash = int(76)
blank_line = dash * num_dash

main_menu_text = f" Main Menu (Ver: {ver_info}) "
main_menu_text_len = len(main_menu_text)
main_menu_dash = int((num_dash - main_menu_text_len) / 2)
main_menu_text_done = f"{main_menu_dash * dash}{main_menu_text}{main_menu_dash * dash}"

while True:
    containers = client.containers.list()
    
    installed_backends = backend_checker.check_json()

    if len(installed_backends) < 1:
        backends_text = f"~~~ You have no backends installed ~~~"
        backends_text_text_len = len(backends_text)
        backends_text_dash = int((num_dash - backends_text_text_len) / 2)
        backends_text_text_done = f"{backends_text_dash * dash}{backends_text}{backends_text_dash * dash}"
    else :
        backends_text = (f"~~~ You have the following backends installed: {', '.join(installed_backends).title()} ~~~")
        backends_text_text_len = len(backends_text)
        backends_text_dash = int((num_dash - backends_text_text_len) / 2)
        backends_text_text_done = f"{backends_text_dash * dash}{backends_text}{backends_text_dash * dash}"


    temp_main_menu_dash = dash * main_menu_dash

    s.clear_window(ver_os_info)
    s.check_for_subsystem_update(ver_os_info, ver_info, DockerClient, compose_path, containers, use_gui, sg, client, ver_info, layout, client_openai, 1234)
    s.clear_window(ver_os_info)
    s.log(blank_line)
    s.log(main_menu_text_done)
    s.log(blank_line)
    s.log(backends_text_text_done)
    print("")
    print(Fore.RED + 'DEV NOTE' + Fore.WHITE + ': Please report bugs to the github or email so we can fix them!')
    print(Fore.RED + 'DEV NOTE' + Fore.WHITE + ': Thank you all so much for helpping with the beta!')
    print("")
    s.log("``1`` - Midori AI Subsystem Repair")
    s.log("``2`` - Install Backends to Subsystem")
    s.log("``3`` - Update Backends in Subsystem")
    s.log("``4`` - Uninstall Backends from Subsystem")
    s.log("``5`` - Backend Programs (install models / edit backends)")
    s.log("``10`` - Enter Subsystem Commandline")
    s.log("Logs will be send to Midori AI's servers.")
    sd_valid_answers = ["1", "2", "3", "4", "5", "10", "chat", "exit"]

    s.log("If you need assistance with most menus, type help.")
    
    questionbasic = "What would you like to do?: "
        
    answerstartup = s.check_str(questionbasic, sd_valid_answers, use_gui, layout, sg, "This is the main menu they are asking for help on...", client_openai)

    if answerstartup.lower() == "exit":
        break

    if answerstartup.lower() == "support":
        answerstartup = "20"

    if answerstartup.lower() == "chat":
        answerstartup = "25"

    answerstartup = int(answerstartup)

    s.clear_window(ver_os_info)
    
    if answerstartup == 1:
        s.data_helper_python()
        docker_add_on.dev_setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, client, ver_info, layout, client_openai, 1234)
        input("Hit enter to go back to the main menu: ")
        s.data_helper_python()

    if answerstartup == 2:
        s.data_helper_python()
        models_edit_add_on.subsystem_backend_manager.backend_installer(None, "midori-docker-compose.yaml", client, client_openai, ver_os_info, 1234)
        s.data_helper_python()

    if answerstartup == 3:
        s.data_helper_python()
        models_edit_add_on.subsystem_backend_manager.backend_updater(None, "midori-docker-compose.yaml", client, ver_os_info)
        input("Hit enter to go back to the main menu: ")
        s.data_helper_python()

    if answerstartup == 4:
        s.data_helper_python()
        models_edit_add_on.subsystem_backend_manager.backend_uninstaller(None, "midori-docker-compose.yaml", client, ver_os_info)
        s.data_helper_python()

    if answerstartup == 5:
        s.data_helper_python()
        backend_menu.main_menu()
        input("Hit enter to go back to the main menu: ")

    if answerstartup == 6:
        s.data_helper_python()
        s.log("this menu is not ready dropping to shell...")
    
    if answerstartup == 10:
        s.data_helper_python()
        s.os_support_command_line(client, Fore)
        input("Hit enter to go back to the main menu: ")
        s.data_helper_python()

    if answerstartup == 20:
        s.log("Support Logs Uploading...")
        s.data_helper_python()
        s.log("Support Logs UPLOADED, please contact Midori AI (contact-us@midori-ai.xyz) for support!")
        input("Hit enter to go back to the main menu: ")

    if answerstartup == 25:
        while True:
            help_add_on.chat_room(help_add_on.request_info("system_prompt.txt"), client_openai, ver_os_info, "This is the main menu, let the user know they need to type help into other menus for you to get context")
            keep_chatting = s.check_str("Would you like to keep chatting?", ["yes", "no"], use_gui, layout, sg, "This is the main menu they are asking for help on...", client_openai)
            s.data_helper_python()
            if keep_chatting == "no":
                break