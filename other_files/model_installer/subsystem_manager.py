import os
import docker

import support as s

import carly_help as help_add_on
import setup_docker as docker_add_on
import setup_models as models_add_on
import edit_models as models_edit_add_on

from colorama import Fore

from version import VERSION
from version import news

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

temp_list = "temp_something_for_model_installer.txt"

user_image = ""

answer_backup_compose ="no"

discord_id = s.get_uuid_id()

ver_info = VERSION

subsystem_file_name = "subsystem_ver_8.subsystemram"

ver_file_name = "midori_program_ver.txt"

if os.path.exists("debug.txt"):
    debug_test_mode = True
else:
    debug_test_mode = False

about_model_size = str("""
| Command | Description |
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

s.log("Booting... Please wait...")

if os.name == 'nt':
    os.system("del model_installer.zip > nul")
    os.system("del subsystem_manager.zip > nul")
    os.system("del model_installer.bat > nul")
    os.system("del model_installer.exe > nul")
    os.system("del restart.bat > nul")
    os.system("del docker.exe > nul")
else:
    os.system("rm -f model_installer_linux.tar.gz > /dev/null")
    os.system("rm -f subsystem_manager.tar.gz > /dev/null")
    os.system("rm -f model_installer > /dev/null")

if os.path.exists("running_subsystem_manager_other_os.py"):
    print("Other OS: Runner seen, updating it")
    os.system("curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/midori_ai_manager/subsystem_python_runner.py > subsystem_python_runner.py")


client_openai = help_add_on.setup_carly(temp_list)

ver_os_info = s.get_os_info()
backend_checker = s.backends_checking()

os.makedirs("files", exist_ok=True)

try:
    if ver_os_info == "linux":
        os.chmod("files", 0o777) # noqa
except Exception as e:
    s.log(f"Something errored with folder setup - {str(e)}")

s.data_helper_python()

client = s.get_docker_client(Fore, ver_os_info, docker, client_openai)

# List all containers
s.clear_window(ver_os_info)

s.check_for_update(ver_os_info, ver_info, client)

s.clear_window(ver_os_info)

s.data_helper_python()

try:
    local_ip_addres = str(s.get_local_ip())
except Exception as e:
    local_ip_addres = "error"
    print(str(e))

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

local_ip_text = f" Local IP ({local_ip_addres}) "
local_ip_text_len = len(local_ip_text)
local_ip_dash = int((num_dash - local_ip_text_len) / 2)
local_ip_text_done = f"{local_ip_dash * dash}{local_ip_text}{local_ip_dash * dash}"

menu_list_opt = []
menu_list_opt.append("``1`` - Midori AI Subsystem Repair")
menu_list_opt.append("``2`` - Install Backends to Subsystem")
menu_list_opt.append("``3`` - Update Backends in Subsystem")
menu_list_opt.append("``4`` - Uninstall Backends from Subsystem")
menu_list_opt.append("``5`` - Backend Programs (install models / edit backends)")
menu_list_opt.append("``6`` - Subsystem and Backend News")
menu_list_opt.append("``10`` - Enter Subsystem Commandline")

if debug_test_mode:
    menu_list_opt.append("``11`` - Python Debug Mode")

temp_context = "This is the main menu they are asking for help on..."
temp_context += f"The numbers are the menu items that they can type into the main menu, it only supports ``python ints``"
temp_context += f"Here is a list of options the user can choose from:\n{', '.join(menu_list_opt).title()}"

news(blank_line, Fore)
s.clear_window(ver_os_info)

while True:
    containers = client.containers.list()
    
    installed_backends = backend_checker.check_json()

    if len(installed_backends) < 1:
        backends_text = f"~~~ You have no backends installed ~~~"
        backends_text_text_len = len(backends_text)
        backends_text_dash = int((num_dash - backends_text_text_len) / 2)
        backends_text_text_done = f"{backends_text_dash * dash}{backends_text}{backends_text_dash * dash}"
        backend_context = f"The user has no backends installed."
    else :
        backends_text = (f"~~~ You have the following backends installed: {', '.join(installed_backends).title()} ~~~")
        backends_text_text_len = len(backends_text)
        backends_text_dash = int((num_dash - backends_text_text_len) / 2)
        backends_text_text_done = f"{backends_text_dash * dash}{backends_text}{backends_text_dash * dash}"
        backend_context = f"The user has these backends installed:\n{', '.join(installed_backends).title()}"


    temp_main_menu_dash = dash * main_menu_dash

    s.clear_window(ver_os_info)
    s.check_for_subsystem_update(ver_os_info, ver_info, DockerClient, compose_path, containers, use_gui, sg, client, ver_info, layout, client_openai, discord_id, subsystem_file_name)
    s.clear_window(ver_os_info)

    s.log(blank_line)
    s.log(main_menu_text_done)
    s.log(local_ip_text_done)
    s.log(backends_text_text_done)
    s.log(blank_line)
    
    for line in menu_list_opt:
        s.log(line)

    s.log("Logs will be send to Midori AI's servers.")
    s.log("If you need assistance with most menus, type help.")

    subsystem_backend_manager = models_edit_add_on.subsystem_backend_manager()
    
    questionbasic = "What would you like to do?: "
    sd_valid_answers = ["1", "2", "3", "4", "5", "6", "10", "11", "chat", "exit"]
    answerstartup = s.check_str(questionbasic, sd_valid_answers, use_gui, layout, sg, temp_context + backend_context, client_openai)

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
        s.repair_clean_up()
        docker_add_on.dev_setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, client, ver_info, layout, client_openai, discord_id, subsystem_file_name)
        s.data_helper_python()

    if answerstartup == 2:
        s.data_helper_python()
        subsystem_backend_manager.backend_installer("midori-docker-compose.yaml", client, client_openai, ver_os_info, discord_id) # type: ignore
        s.data_helper_python()

    if answerstartup == 3:
        s.data_helper_python()
        subsystem_backend_manager.backend_updater("midori-docker-compose.yaml", client, ver_os_info) # type: ignore
        input("Hit enter to go back to the main menu: ")
        s.data_helper_python()

    if answerstartup == 4:
        s.data_helper_python()
        subsystem_backend_manager.backend_uninstaller("midori-docker-compose.yaml", client, ver_os_info) # type: ignore
        s.data_helper_python()

    if answerstartup == 5:
        s.data_helper_python()
        backend_menu.main_menu() 
        input("Hit enter to go back to the main menu: ")

    if answerstartup == 6:
        s.data_helper_python()
        news(blank_line, Fore)
        
    
    if answerstartup == 10:
        s.data_helper_python()
        s.os_support_command_line(client, Fore)
        input("Hit enter to go back to the main menu: ")
        s.data_helper_python()
    
    if answerstartup == 11:
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