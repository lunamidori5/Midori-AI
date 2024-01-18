import os
import yaml
import docker
import requests
import datetime
import platform
import subprocess

from cpuinfo import get_cpu_info
from multiprocessing import freeze_support

from python_on_whales import docker as docker_two
from python_on_whales import DockerClient

use_cuda = "False"
use_tts = "False"
use_core = "False"

missing_cuda = True
missing_cuda_toolkit = True

compose_path = "docker-compose.yaml"

ver_info = "0.0.23"

localai_ver_number = "v2.5.1"
base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y%H%M%S")
log_file_name = "log_" + timestamp + ".txt"

ver_file_name = "localai_installer_ver.txt"

with open(log_file_name, "w") as f:
  f.write("Booted and Running localai Installer")

def log(message):
  message_cleaned = str(message)
  # Read the current contents of  the file
  with open(log_file_name, "r") as f:
    contents = f.read()

  print(message_cleaned)
  contents += "\n" + message_cleaned

  # Resave the file
  with open(log_file_name, "w") as f:
    f.write(contents)

def clear_window(ver_os):
  log("Clearing the screen")
  if ver_os == 'windows':
    os.system('cls')
  if ver_os == 'linux':
    os.system('clear ')

def check_for_update(ver_os_info):
  """
  Sends a request to the server to check for a installer update.
  """
  placeholder_link = f"https://tea-cup.midori-ai.xyz/download/localai_installer_{ver_os_info}.zip"

  # Send a request to the server for the model version.
  response = requests.get("https://tea-cup.midori-ai.xyz/download/localai_installer_ver.txt")

  # Check if the request was successful.
  if response.status_code != 200:
    log(f"Servers seem to be down, please try again in a moment...")
    exit(418)

  # Get the current model version.
  current_version = response.text.strip()

  # Check if the current version is the latest version.
  clear_window(ver_os_info)
  if current_version == ver_info:
    log("Your installer is up to date.")
    clear_window(ver_os_info)
  else: 
    log(f"-----------------------------------------------------------------------------------------------")
    log(f"A update is available. Please update using the following link: {placeholder_link}")
    log(f"-----------------------------------------------------------------------------------------------")
    exit(1)

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

def check_str(question, valid_answers):
  """
  Checks if the user input is valid.

  Args:
    question: The  question to ask the user.
    valid_answers:  A list of valid answers.

  Returns:
    The user's input if it is valid, or None otherwise.
  """

  while True:
    answer = input(f"\n{question}\n").lower()
    if answer in valid_answers:
      log(f"I asked {question} / you replied {answer}")
      return answer
    else:
      log(f"\nInvalid input. Please enter one of the following: {', '.join(valid_answers)}\n")
    
# Get the operating system.
os_info = platform.system()

# Set the ver_os_info variable accordingly.
if os_info == "Windows":
  ver_os_info = "windows"
  os.system('title LocalAI Installer')
elif os_info == "Linux":
  ver_os_info = "linux"
else:
  log(f"Unsupported operating system: {os_info}")
  ver_os_info = "Unknown"

try:
  # Check if the current platform is Windows
  if os.name == 'nt':
    # Connect to the Docker daemon on Windows using Docker-py for Windows 
    log("Logging into  docker vm subsystem (Windows)")
    client = docker.from_env(version='auto')
  else:
    # Connect to the Docker daemon on Linux-like systems using Docker-py
    log("Logging into docker vm subsystem (Linux)")
    log("If this fails please try running me as root user")
    client = docker.from_env()
except Exception as e:
  log("Failed to connect to Docker daemon, please install Docker and try again")
  log(str(e))
  exit(1)

# List all containers
containers = client.containers.list()

log(containers)

check_for_update(ver_os_info)

rebuild = check_cpu_support()

clear_window(ver_os_info)

if rebuild:
  log("The CPU does not support the required features. Rebuilding is necessary.")
else:
  log("The CPU supports the required features. No need to rebuild.")

log("Alright, now that I am logged into the docker, lets get you started with installing the model...")
log(f"I am going to save our chat here and every thing I do to a file called ``{log_file_name}``, check it out if you like <3")
log("Here are a few questions about how you want me to setup your LocalAI docker image...")

questionbasic = "Would you like me to install LocalAI in docker to this computer?: "
valid_answers = ["yes", "no", "true", "false"]
answerbasic = check_str(questionbasic, valid_answers)

if answerbasic.lower() == "no":
  answerbasic = "False"
        
if answerbasic.lower() == "yes":
  answerbasic = "True"

answerbasic = answerbasic.lower()

if answerbasic == "false":
  log("Alright then ill go ahead and exit! Thank you!")
  exit(1)

clear_window(ver_os_info)

log("LocalAI offers a ``master`` image.")
log("This image maybe unstable or have bugs but will let you test out the newer models.")

questionbasic = "Would you like to try the ``master`` image?: "
valid_answers = ["yes", "no", "true", "false"]
answermaster = check_str(questionbasic, valid_answers)

if answermaster.lower() == "no":
  answermaster = "False"
        
if answermaster.lower() == "yes":
  answermaster = "True"

answermaster = answermaster.lower()

clear_window(ver_os_info)

log("Sadly I am unable to check your CUDA install for GPU, If you have it already installed good!")
log("If not please stop by ``https://developer.nvidia.com/cuda-downloads`` and get it for your OS, WSL is Linux")
log("If you do not have CUDA installed or use a card that does not support it please type no...")
questionbasic = "Would you like to use GPU with LocalAI? It speeds up LLMs and SD models by 25x: "
valid_answers = ["yes", "no", "true", "false"]
answer_cuda = check_str(questionbasic, valid_answers)

if answer_cuda.lower() == "no":
  answer_cuda = "False"
        
if answer_cuda.lower() == "yes":
  answer_cuda = "True"

use_cuda = answer_cuda.lower()

if use_cuda == "true":
  clear_window(ver_os_info)
  os.system('nvidia-smi')
  log("I ran the cuda command, it \"should\" show you if you have CUDA11 or CUDA12")
  questionbasic = "Do you have CUDA11 or CUDA12? (Type just 11 or 12): "
  valid_answers = ["11", "12"]
  version = check_str(questionbasic, valid_answers)

clear_window(ver_os_info)

questionbasic = "Would you like me to add TTS / Audio support to LocalAI?: "
valid_answers = ["yes", "no", "true", "false"]
answertts = check_str(questionbasic, valid_answers)

if answertts.lower() == "no":
  answertts = "False"
        
if answertts.lower() == "yes":
  answertts = "True"

answertts = answertts.lower()

clear_window(ver_os_info)

questionbasic = "LocalAI offers a ``core`` image that lowers the image size by more than 60% \nInstalling this image removes support for all non LLM, Embedding, or TTS models.\nThis also removes the encrypted endpoint of the model installer. \nWould you like to use the core image? (Not Recommended): "
valid_answers = ["yes", "no", "true", "false"]
answercore = check_str(questionbasic, valid_answers)

if answercore.lower() == "no":
  answercore = "False"
        
if answercore.lower() == "yes":
  answercore = "True"

answercore = answercore.lower()

clear_window(ver_os_info)

log("We have a docker ready if you would like to try it, its called AnythingLLM, its a GUI or WebUI for LocalAI. It comes highly recommened for new users.")
questionbasic = "Would you like me to install AnythingLLM in a docker next to LocalAI?"
valid_answers = ["yes", "no", "true", "false"]
answeranything = check_str(questionbasic, valid_answers)

if answeranything.lower() == "no":
  answeranything = "False"
        
if answeranything.lower() == "yes":
  answeranything = "True"

answeranything = answeranything.lower()

clear_window(ver_os_info)

log("Alright lets get everything together...")

if answermaster == "true":
  log("you requested to use the master image, Ill add that to the compose file now!")
  user_image = "master"

else:
  log(f"you requested to not use the master image, Ill set you to ``{localai_ver_number}`` image then! Adding that to your compose file!")
  user_image = localai_ver_number

if use_cuda == "true":
  log("cuda is installed, setup, and requested. Adding that to the docker-compose file now <3")
  user_image = user_image + "-cublas-cuda"
  user_image = user_image + version

if use_tts == "true":
  log("looks like you requested TTS / Audio support, Ill get that added now!")
  user_image = user_image + "-ffmpeg"

if use_core == "true":
  log("looks like you wish to use the smaller core image. Ill add that to your docker-compose.yaml")
  user_image = user_image + "-core"

os.makedirs("models", exist_ok=True)
os.makedirs("photos", exist_ok=True)
os.makedirs("others", exist_ok=True)

gpu_text_debug = ["gpu", "nvidia-compute"]

if use_cuda == "false":
  config = { 
      "version": "3.6",
      "services": {
          "api": {
              "image": f"{base_image_name}{user_image}",
              "tty": True,
              "restart": "always",
              "ports": ["8080:8080"],
              "environment": {
                "REBUILD": str(rebuild).lower(),
                "COMPEL": "0",
                "DEBUG": str(True).lower(),
                "MODELS_PATH": "/models",
                "SINGLE_ACTIVE_BACKEND": str(True).lower(),
                },  # env_file is commented out  
              "volumes": ["./models:/models", "./photos:/tmp/generated/images/"],
              "command": ["/usr/bin/local-ai"],
          }
      }
  }

else:

  config = { 
    "version": "3.6",
    "services": {
      "api": {
          "deploy": {
            "resources": {
              "reservations": {
                "devices": [
                  {'driver': 'nvidia', 
                   'count': 1, 
                   'capabilities': "changeme"
                   }]}}},
          "image": f"{base_image_name}{user_image}",
          "tty": True,
          "restart": "always",
          "ports": ["8080:8080"],
          "environment": {
            "REBUILD": str(rebuild).lower(),
            "COMPEL": "0",
            "DEBUG": str(True).lower(),
            "MODELS_PATH": "/models",
            "SINGLE_ACTIVE_BACKEND": str(True).lower(),
          },  # env_file is commented out
          "volumes": ["./models:/models", "./photos:/tmp/generated/images/"],
          "command": ["/usr/bin/local-ai"],
        }
      }
  }

log(config)

# Dump the configuration to a YAML file
with open(compose_path, "w") as f:
  yaml.dump(config, f, sort_keys=True)

if use_cuda == "true":
  with open(compose_path, 'r') as f: 
    # Read the entire contents of the file into a string
    compose_yaml = f.read()

  # Replace all occurrences of 'changeme ' with '["gpu"]' in the string
  compose_yaml = compose_yaml.replace('changeme', '["gpu"]')

  # Write the modified string back to the file
  with open(compose_path, 'w') as f:
    f.write(compose_yaml)

if answeranything == "true":
  log("making folders and docker compose file for AnythingLLM")

  anythingllm_str_env = """
    SERVER_PORT=3001
    STORAGE_DIR="/app/server/storage"
    UID='1000'
    GID='1000'
  """

  with open(".env", 'w') as f:
    f.write(anythingllm_str_env)
  
  os.system( f"curl https://tea-cup.midori-ai.xyz/download/anythingllm-docker-compose.yaml -o anythingllm-docker-compose.yaml")
  
  os.makedirs("storage", exist_ok=True)
  os.makedirs("hotdir", exist_ok=True)
  os.makedirs("outputs", exist_ok=True)
  
  anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])

log("yaml saved spinning up the docker compose...")
localai_docker = DockerClient(compose_files=["./docker-compose.yaml"])

localai_docker.compose.up(build=False, detach=True, no_build=False, remove_orphans=True, color=True, log_prefix=True, start=True, pull="always")

if answeranything == "true":
  anythingllm_docker.compose.up(build=False, detach=True, no_build=False, remove_orphans=True, color=True, log_prefix=True, start=True, pull="always")

if rebuild:
  log("Due to your CPU not supporting one of the needed things, LocalAI is now rebuilding itself, please wait before installing models or making requests...")
  log("This can take up to 10+ mins to do, sorry for the delay...")

log("Alright all done, please try out our model installer if you would like us to install some starting models for you <3")
log("Thank you for using Midori AI's Auto LocalAI installer!")
