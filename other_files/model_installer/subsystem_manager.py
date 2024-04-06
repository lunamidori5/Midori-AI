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

base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

answer_backup_compose ="no"

ver_info = "changemelunaplease"

subsystem_file_name = "subsystem_ver_8.subsystemram"

ver_file_name = "midori_program_ver.txt"

about_model_size = str("""
| Command | Description |
|7b| Recommend for lowerend PC (6gb of Vram or less / 10gb of system ram)
|8x7b| Recommended for highend PC (24gb or more Vram needed / 55gb of system ram)
|70b| Recommended for high end servers only (AI card or better with 48gb Vram + 100gb system ram)
|Huggingface| All GGUF Huggingface Models are supported - https://io.midori-ai.xyz/subsystem/local-ai/install_models/
|ID| Models from the Midori AI Repo - https://io.midori-ai.xyz/models/offsite_models/
|Base| Models that are baked into LocalAI - https://localai.io/basics/getting_started/
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
    os.system("del model_installer.zip > nul")
    os.system("del subsystem_manager.zip > nul")
    os.system("del model_installer.bat > nul")
    os.system("del model_installer.exe > nul")
else:
    os.system("rm -f model_installer_linux.tar.gz > /dev/null")
    os.system("rm -f subsystem_manager.tar.gz > /dev/null")
    os.system("rm -f model_installer > /dev/null")

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

        # Check if the current working directory is in a  restricted folder
        if os.path.abspath(os.getcwd()) in ['C:\\Windows', 'C:\\Windows\\System32', 'C:\\Program Files', 'C:\\Program Files (x86)']:
            print ("Error: We are running in a restricted folder. Crashing...")
            input("Press enter to exit: ")
            exit(1)

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

menu_list_opt = []
menu_list_opt.append("``1`` - Midori AI Subsystem Repair")
menu_list_opt.append("``2`` - Install Backends to Subsystem")
menu_list_opt.append("``3`` - Update Backends in Subsystem")
menu_list_opt.append("``4`` - Uninstall Backends from Subsystem")
menu_list_opt.append("``5`` - Backend Programs (install models / edit backends)")
menu_list_opt.append("``10`` - Enter Subsystem Commandline")

temp_context = "This is the main menu they are asking for help on..."
temp_context += f"The numbers are the menu items that they can type into the main menu, it only supports ``python ints``"
temp_context += f"Here is a list of options the user can choose from:\n{', '.join(menu_list_opt).title()}"

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
    s.check_for_subsystem_update(ver_os_info, ver_info, DockerClient, compose_path, containers, use_gui, sg, client, ver_info, layout, client_openai, 1234, subsystem_file_name)
    s.clear_window(ver_os_info)
    s.log(blank_line)
    s.log(main_menu_text_done)
    s.log(blank_line)
    s.log(backends_text_text_done)
    print("")
    print(Fore.RED + 'DEV NOTE' + Fore.WHITE + ': Please report bugs to the github or email so we can fix them!')
    print(Fore.RED + 'DEV NOTE' + Fore.WHITE + ': Thank you all so much for helpping with the beta! <3')
    print("")
    
    for line in menu_list_opt:
        s.log(line)

    s.log("Logs will be send to Midori AI's servers.")
    sd_valid_answers = ["1", "2", "3", "4", "5", "10", "chat", "exit"]

    s.log("If you need assistance with most menus, type help.")
    
    questionbasic = "What would you like to do?: "
        
    answerstartup = s.check_str(questionbasic, sd_valid_answers, use_gui, layout, sg, temp_context, client_openai)

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
        docker_add_on.dev_setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, client, ver_info, layout, client_openai, 1234, subsystem_file_name)
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