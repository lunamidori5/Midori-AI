import os
import json
import yaml
import docker
import requests
import datetime
import platform

import support as s

import carly_help as help_add_on
import setup_docker as docker_add_on
import setup_models as models_add_on
import edit_models as models_edit_add_on

from colorama import Fore

from openai import OpenAI

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

compose_path = "docker-compose.yaml"

localai_ver_number = "v2.7.0"
base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

ver_info = "changemelunaplease"

ver_file_name = "midori_program_ver.txt"

about_model_size = str("""
7b [CPU Friendly!] (Small and okay quality) - https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF
2x7b (Normal sized, good quality) - https://huggingface.co/TheBloke/laser-dolphin-mixtral-2x7b-dpo-GGUF
8x7b (Big, great quality) - https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF
70b (Large, hard to run but significant quality) - https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF
ID (These are models from the Midori AI model repo) - https://io.midori-ai.xyz/models/offsite_models/
""")

about_model_q_size = str("""
| Quant Mode | Description |
|Q3| Smallest, significant quality loss - not recommended|
|Q4| Medium, balanced quality|
|Q5| Large, very low quality loss - recommended for most users|
|Q6| Very large, extremely low quality loss|
|Q8| Extremely large, extremely low quality loss, hard to use - not recommended|
|None| Extremely large, No quality loss, super hard to use - really not recommended|

Note: 
That some models may deviate from our conventional model formatting standards (Quantized/Non-Quantized), 
and will be served using a rounding-down approach. For instance, if you request a Q8 model and none is available, 
the Q6 model will be served instead, and so on.
""")

response_git = requests.get("https://github.com/lunamidori5/Midori-AI/blob/b9a74490f5b5ad0ecce56dbd7718fab3e31ece1b/data/version.json")

if response_git.status_code != 200:
    s.log(f"Github seem to be down, please try again in a moment...")
    exit(418)

current_version_git = response_git.text.strip()

s.log("I am setting up a temp copy of Carly...")
temp_response = requests.get("https://tea-cup.midori-ai.xyz/download/temp_something_for_model_installer.txt")
temp_keys = temp_response.text.strip()
client_openai = OpenAI(base_url="https://ai.midori-ai.xyz/v1", api_key=temp_keys)

# localai_ver_number = version_data['version']

# Get the operating system.
os_info = platform.system()

# Set the ver_os_info variable accordingly.
if os_info == "Windows":
    ver_os_info = "windows"
    os.system('title LocalAI Manager')
elif os_info == "Linux":
    ver_os_info = "linux"
else:
    s.log(f"Unsupported operating system: {os_info}")

# Check if the current platform is Windows
try:
    if os.name == 'nt':
         # Connect to the Docker daemon on Windows using Docker-py for Windows 
        s.log("s.logging into docker vm subsystem (Windows)")
        client = docker.from_env(version='auto')
    else:
        # Connect to the Docker daemon on Linux-like systems using Docker-py
        s.log("s.logging into docker vm subsystem (Linux)")
        s.log("If this fails please try running me as root user")
        client = docker.from_env()

except Exception as e:
    s.log("Looks like I was unable to s.log into the docker subsystem...")
    s.log("Do you have docker installed? / Please try running me as root user, Linux users.")
    input("Please press enter to exit: ")
    exit(1)


# List all containers
containers = client.containers.list()

s.clear_window(ver_os_info)

s.check_for_update(ver_os_info)

if ver_os_info == "windows":
    questionbasic = "Would you like to use a GUI: "
    valid_answers = ["yes", "no"]
    use_gui = s.check_str(questionbasic, valid_answers, "no", None)
else:
    use_gui = "no"

s.clear_window(ver_os_info)

s.log("-----------------------------------------------------------------------------------------------")
s.log(f"------------------------------ Main Menu (Ver: {ver_info}) ------------------------------------")
s.log("-----------------------------------------------------------------------------------------------")

s.log("``1`` - Setup LocalAI / AnythingLLM")
s.log("``2`` - Uninstall or Upgrade LocalAI / AnythingLLM")
s.log("``3`` - Setup or Upgrade Models")
s.log("``4`` - Edit Models Configs")
s.log("``5`` - Uninstall Models")
s.log("``Help`` - Ask Carly's 7b model for help (Not done yet, dont use)")

questionbasic = "What would you like to do?: "
sd_valid_answers = ["1", "2", "3", "4", "5", "exit"]

if use_gui == "yes":
    import PySimpleGUI as sg
    layout = [[sg.Text(f"Main Menu (Ver: {ver_info})", size=(40, 1))],
            [sg.Text(f"``1`` - Setup LocalAI / AnythingLLM", size=(30, 1)), 
             sg.Text(f"``2`` - Uninstall or Upgrade LocalAI / AnythingLLM", size=(45, 1)),],
            [sg.Text(f"``3`` - Setup or Upgrade Models", size=(30, 1)),
             sg.Text(f"``4`` - Edit Models Configs", size=(30, 1)),
             sg.Text(f"``5`` - Uninstall Models", size=(30, 1))],
            [sg.Text(f"{questionbasic}", size=(100, 1))],
            [sg.Input(key='-QUERY-'),
            sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
            ]
    
answerstartup = s.check_str(questionbasic, sd_valid_answers, use_gui, layout, sg)

if answerstartup.lower() == "exit":
    exit(0)

if answerstartup.lower() == "help":
    answerstartup = int(25)

answerstartup = int(answerstartup)

s.clear_window(ver_os_info)

if answerstartup == 1:
    docker_add_on.setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, base_image_name, localai_ver_number)
    
if answerstartup == 2:
    docker_add_on.change_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg)

if answerstartup == 3:
    models_add_on.models_install(compose_path, ver_os_info, containers, client, use_gui, sg, about_model_size, about_model_q_size)

if answerstartup == 4:
    models_edit_add_on.edit(compose_path, ver_os_info, containers, client, use_gui, sg)

if answerstartup == 5:
    models_add_on.models_uninstall(compose_path, ver_os_info, containers, client, use_gui, sg)

if answerstartup == 25:
    completion = client_openai.chat.completions.create(
    model="gpt-4.1-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=True
    )

    for chunk in completion:
        print(chunk.choices[0].delta)