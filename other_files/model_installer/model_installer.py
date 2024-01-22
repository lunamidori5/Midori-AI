import os
import json
import yaml
import docker
import requests
import datetime
import platform

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

localai_ver_number = "v2.6.0"
base_image_name = "quay.io/go-skynet/local-ai:"

user_image = ""

ver_info = "changemelunaplease"

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y%H%M%S")
log_file_name = "log_" + timestamp + ".txt"

ver_file_name = "midori_program_ver.txt"

with open(log_file_name, "w") as f:
   f.write("Booted and Running Model Installer")

about_model_size = str("""
7b [CPU Friendly!] (Small and okay quality) - https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF
43b (Normal sized, great quality) - https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF
70b (Large, hard to run but significant quality) - https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF
ID (These are models from the Midori AI model repo) - https://io.midori-ai.xyz/models/
""")

about_model_q_size = str("""
| Quant Mode | Description |
|Q3| Smallest, significant quality loss - not recommended|
|Q4| Medium, balanced quality|
|Q5| Large, very low quality loss - recommended for most users|
|Q6| Very large, extremely low quality loss|
|Q8| Extremely large, extremely low quality loss, hard to use - not recommended|
|None| Extremely large, No quality loss, super hard to use - really not recommended|
                         
Note: If the model does not support a quant mode, the server will return the next lowest one it has...
""")

def log(message):
  # Read the current contents of  the file
  with open(log_file_name, "r") as f:
    contents = f.read()

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
        os.system('clear ')

def check_for_update(ver_os_info):
    """
    Sends a request to the server to check for a installer update.
    """
    placeholder_link = f"https://io.midori-ai.xyz/howtos/easy-model-installer/"

    # Send a request to the server for the model version.
    response = requests.get("https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt")

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
        exit(15)
        
        # Run commands based on the OS
        if ver_os_info == 'windows':
            os.system("del model_installer.zip")
            os.system("del model_installer")
            os.system(f"curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/model_installer.bat -o model_installer.bat && start model_installer.bat")
            log(f"If the model manager failed to start, just run ``call model_installer.bat``")
        elif ver_os_info == 'linux':
            os.system("rm -f model_installer.tar.gz model_installer")
            os.system(f"curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/model_installer.sh | sh")
            log(f"If the model manager failed to start, just run ``./model_installer.sh``")

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
    os.system('title LocalAI Manager')
elif os_info == "Linux":
    ver_os_info = "linux"
else:
    log(f"Unsupported operating system: {os_info}")

# Check if the current platform is Windows
if os.name == 'nt':
    # Connect to the Docker daemon on Windows using Docker-py for Windows 
    log("Logging into docker vm subsystem (Windows)")
    client = docker.from_env(version='auto')
else:
    # Connect to the Docker daemon on Linux-like systems using Docker-py
    log("Logging into docker vm subsystem (Linux)")
    log("If this fails please try running me as root user")
    client = docker.from_env()

# List all containers
containers = client.containers.list()

check_for_update(ver_os_info)

log("\n")

log(f"-----------------------------------------------------------------------------------------------")
log(f"------------------------------ Main Menu (Ver: {ver_info}) ------------------------------------")
log(f"-----------------------------------------------------------------------------------------------")

log("``1`` - Setup LocalAI / AnythingLLM")
log("``2`` - Uninstall or Upgrade LocalAI / AnythingLLM")
log("``3`` - Setup or Upgrade Models")
log("``4`` - Uninstall Models")

questionbasic = "What would you like to do?: "
sd_valid_answers = ["1", "2", "3", "4"]
answerstartup = check_str(questionbasic, sd_valid_answers)

answerstartup = int(answerstartup)

clear_window(ver_os_info)

if answerstartup == 3:
    # Try to load the Docker Compose file
    log("Docker Server error, trying to check your docker-compose.yaml file...")
    docker_compose_found = False
    try:
        log("Loading your docker-compose.yaml")
        with open(compose_path, "r") as f:
            compose_data  = yaml.safe_load(f)
            log("Auto loaded the docker-compose.yaml")
            docker_compose_found = True
    except FileNotFoundError:
        # If the file is not found, ask the user where it is
        log("If you used docker run or just want to try to run this in ``fallback mode`` type ``fallback``")
        compose_path = input("Could not find docker-compose.yaml in the current directory. Where is it located?: ")
        try:
            with open(compose_path, "r") as f:
                compose_data = yaml.safe_load(f)
            log("Loaded the docker-compose.yaml from users path")
        except FileNotFoundError:
            # If the file is still not found, raise an error
            log("Could not find docker-compose.yaml at the specified location. Entering ``fallback mode``")


    # Extract service name and model folder path
    if docker_compose_found:
        for service_name, service_data in compose_data["services"].items():
            log(f"Checking... Service Name: {service_name}, Service Data: {service_data}")
            if service_data["image"].startswith("quay.io/go-skynet/local-ai"):
                models_volume = service_data["volumes"][0]
                models_folder_host = models_volume.split(":")[0]  # Assuming host path is first
                models_folder_container = models_volume.split(":")[1]  # Assuming container path is second
                models_ports = service_data["ports"][0]
                model_port_api = models_ports.split(":")[1]
                service_image = service_data["image"]

                log(f"The inside model folder of the docker is {models_folder_container}, This is were ill place all the files inside of the docker.")
                break

        # If no matching service is found, raise an error
        if service_name not in compose_data["services"]:
            raise Exception("Could not find a service with the image 'quay.io/go-skynet/local-ai' in your docker-compose.yaml file.")
    else:
        clear_window(ver_os_info)
        log("Running ``docker ps``")

        os.system('docker ps -a --format \"table {{.ID}}\t{{.Names}}\"')
        
        service_name = input("What is LocalAI called in ``docker ps`` (Please type the name like this ``localai-api-1`` or ``localai``): ")

        clear_window(ver_os_info)

        models_folder_container = input("Where is LocalAI's models folder located? (IE: ``/models`` or ``/build/models``): ")

        clear_window(ver_os_info)

        os.system('docker ps -a --format \"table {{.Names}}\t{{.Image}}\"')

        service_image = input("What is the full image name that you used? (Please paste the full link. IE: quay.io/go-skynet/local-ai:master-cublas-cuda12-ffmpeg): ")

        clear_window(ver_os_info)

        os.system('docker ps -a --format \"table {{.Names}}\t{{.Ports}}\"')
        models_ports = input("What port are you running LocalAI on?: ")

    clear_window(ver_os_info)

    for container in containers:
        log(f"Checking Name: {container.name}, ID: {container.id}")

        # Check if there is a container with a name containing `service_name`
        if service_name in container.name:
            # Get the container object
            log(f"Found LocalAI, Logging into: {container.name} / {container.id}")
            container = client.containers.get(container.name)
            break

    if container is None:
        log(f"Error: Could not find LocalAI container with name {service_name}")
        log("Checking images again with known names")
        for container in containers:
            log(f"Checking Name: {container.name}, ID: {container.id}")

            # Check if there is a container with a name containing `service_name`
            if service_name in container.name:
                # Get the container object
                log(f"Found LocalAI, Logging into: {container.name} / {container.id}")
                container = client.containers.get(container.name)
                break
        
    clear_window(ver_os_info)

    log("Alright, now that I am logged into the docker, lets get you started with installing the model...")
    log("For more info on the models used, or links to the models, go to ``https://io.midori-ai.xyz/howtos/easy-model-installer/``")
    log(f"I am going to save our chat here and every thing I do to a file called ``{log_file_name}``, check it out if you like <3")
    log("Here are a few questions to find out what model you would like to try")

    use_gpu = True

    answer4_name = ""

    use_sd = "false"
    use_tts = "false"

    use_enbed = "false"
    use_llava = "false"

    use_llava = "false"
    use_enbed = "false"

    answerencrypted = "false"

    questionbasic = "Would you like to install a LLM?: "
    sd_valid_answers = ["yes", "no", "true", "false"]
    answerbasic = check_str(questionbasic, sd_valid_answers)

    if answerbasic.lower() == "no":
        answerbasic = "False"
            
    if answerbasic.lower() == "yes":
        answerbasic = "True"

    answerbasic = answerbasic.lower()

    clear_window(ver_os_info)

    if answerbasic:
        question4 = "What would you like to name the models file?: \n"
        answer4 = input(question4)
        answer4 = str(answer4.lower())

        clear_window(ver_os_info)

        log(about_model_size)
        valid_answers2 = ["7b", "43b", "70b", "id"]
        question2 = f"What size of known and supported model would you like to setup ({', '.join(valid_answers2)}): "
        answer2 = check_str(question2, valid_answers2)
        answer2 = str(answer2.lower())

        valid_answers1 = ["q3", "q4", "q5", "q6", "q8"] 
        added_valid_answers1 = ["q4-k-m", "q5-k-m"]
        added_valid_answers2 = ["none"]

        if answer2.lower() == "43b":
            valid_answers1.extend(added_valid_answers1)
        
        if answer2.lower() != "id":
            valid_answers1.extend(added_valid_answers2)

        if answer2.lower() == "id":
            clear_window(ver_os_info)
            valid_answers2 = check_model_ids_file()
            question2 = f"What is the id of the model you would like to install? ({', '.join(valid_answers2)}): "
            answer2 = check_str(question2, valid_answers2)
            answer2 = str(answer2.lower())

        clear_window(ver_os_info)

        log(about_model_q_size)

        question1 = f"What type of quantised model would you like to setup? ({', '.join(valid_answers1)}): "
        answer1 = check_str(question1, valid_answers1)

        if answer1.lower() == "none":
            answer1 = str(answer1.lower())
        else:
            answer1 = str(answer1.upper())

        # Check if the word "model" is in the answer
        if "model" in answer4:
            # Remove the word "model"  from the answer
            answer4 = answer4.replace("model", "")

            # Print a message to the user
            log("\nThe word 'model' has been removed from the file name.")

        # Check if GPU is turned on
        if "cuda11" in service_image or "cuda12" in service_image:
            clear_window(ver_os_info)
            # Ask the user the third question
            if not answer1 == "none":
                question3 = "\nNumber of GPU layers to give the model?  (0 to 2000): \n"
                answer3 = input(question3)
                answer3 = int(answer3)
                use_gpu = True
        else:
            answer3 = 0
            answer3 = int(answer3)
            use_gpu = False

        clear_window(ver_os_info)

    if "ffmpeg" in service_image:
        questionsd = "Would you like me to install a few Text to Speech models?: "
        sd_valid_answers = ["yes", "no", "true", "false"]
        answertts = check_str(questionsd, sd_valid_answers)

        if answertts.lower() == "no":
            answertts = "False"
            
        if answertts.lower() == "yes":
            answertts = "True"

        answertts = answertts.lower()
        use_tts = answertts

        clear_window(ver_os_info)

    questionsd = "Would you like me to install the embedding model?: "
    sd_valid_answers = ["yes", "no", "true", "false"]
    answerenbed = check_str(questionsd, sd_valid_answers)

    if answerenbed.lower() == "no":
        answerenbed = "False"
            
    if answerenbed.lower() == "yes":
        answerenbed = "True"

    answerenbed = answerenbed.lower()
    use_enbed = answerenbed

    clear_window(ver_os_info)

    if "core" in service_image:
        log("Looks like you are running a Core Image, Skipping: Stable diffusion, Llava, Huggingface Models")
    else:
        if "cuda11" in service_image or "cuda12" in service_image:
            questionsd = "Would you like me to install a Stable diffusion model?: "
            sd_valid_answers = ["yes", "no", "true", "false"]
            answersd = check_str(questionsd, sd_valid_answers)

            if answersd.lower() == "no":
                answersd = "False"
            
            if answersd.lower() == "yes":
                answersd = "True"

            answersd = answersd.lower()
            use_sd = answersd

            clear_window(ver_os_info)
            
            questionsd = "Would you like me to install the Llava model?: "
            sd_valid_answers = ["yes", "no", "true", "false"]
            answerllava = check_str(questionsd, sd_valid_answers)

            if answerllava.lower() == "no":
                answerllava = "False"
            
            if answerllava.lower() == "yes":
                answerllava = "True"

            answerllava = answerllava.lower()
            use_llava = answerllava

            clear_window(ver_os_info)
        else:
            log("Looks like you are running on CPU only, Skipping: Stable diffusion, Llava, Huggingface Models")
        
        questionsd = "Would you like to use our slower but encrypted endpoint for LocalAI to serve and setup the model's files (Not the models file itself)?: "
        sd_valid_answers = ["yes", "no", "true", "false"]
        answerencrypted = check_str(questionsd, sd_valid_answers)

        if answerencrypted.lower() == "no":
            answerencrypted = "False"
        
        if answerencrypted.lower() == "yes":
            answerencrypted = "True"

        answerencrypted = answerencrypted.lower()

        clear_window(ver_os_info)

    log(f"I am now going to install everything you requested, please wait for me to get done. As ill be running commands inside of your docker image.")
    log("Hit enter to start")

    input()

    clear_window(ver_os_info)

    if answer1 == "none":
        if answer2 == "7b":
            answer4_name = "cognitivecomputations"
            answer4_name_b = "dolphin-2.6-mistral-7b"
        if answer2 == "43b":
            answer4_name = "cognitivecomputations"
            answer4_name_b = "dolphin-2.7-mixtral-8x7b"
        if answer2 == "70b":
            answer4_name = "cognitivecomputations"
            answer4_name_b = "dolphin-2.2-70b"

    if answerbasic == "true":
        log(f"The type of model you want to setup is: {answer1}")
        log(f"The size of the known model you want to setup is: {answer2}")
        log(f"The amount of GPU layers you want to give it is: {answer3}")
        log(f"You named the model: {answer4}")

        inside_model_folder = models_folder_container
        temp_chat_path =  inside_model_folder + "/localai-chat.tmpl"
        temp_chatmsg_path = inside_model_folder + "/localai-chatmsg.tmpl"
        model_path_temp = inside_model_folder + f"/{answer4}.gguf"
        yaml_path_temp = inside_model_folder + f"/{answer4}.yaml"

        docker_commands_cpu = [
            ["echo", f"Setting up the {answer2} model you requested"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.gguf"],
            ["rm", "-f", f"{inside_model_folder}/localai-chat.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/localai-chatmsg.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.yaml"],
            ["wget", "-O", f"localai-chat.tmpl", f"https://tea-cup.midori-ai.xyz/download/localai-chat.tmpl"],
            ["wget", "-O", f"localai-chatmsg.tmpl", f"https://tea-cup.midori-ai.xyz/download/localai-chatmsg.tmpl"],
            ["wget", "-O", f"{answer4}.yaml", f"https://tea-cup.midori-ai.xyz/download/models.yaml"],
            ["wget", "-O", f"{answer4}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"{answer4}.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer4}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/model.*/model: {answer4}.gguf/g", f"{yaml_path_temp}"],
            ["echo", f"Catting the yaml for easyer debuging..."],
            ["cat", f"{yaml_path_temp}"],
            ["rm", "-f", "localai-chat.tmpl"],
            ["rm", "-f", "localai-chatmsg.tmpl"],
            ["rm", "-f", f"{answer4}.yaml"],
            ["rm", "-f", f"{answer4}.gguf"],
        ]

        docker_commands_gpu = [
            ["echo", f"Setting up the {answer2} model you requested"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.gguf"],
            ["rm", "-f", f"{inside_model_folder}/localai-chat.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/localai-chatmsg.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.yaml"],
            ["wget", "-O", f"localai-chat.tmpl", f"https://tea-cup.midori-ai.xyz/download/localai-chat.tmpl"],
            ["wget", "-O", f"localai-chatmsg.tmpl", f"https://tea-cup.midori-ai.xyz/download/localai-chatmsg.tmpl"],
            ["wget", "-O", f"{answer4}.yaml", f"https://tea-cup.midori-ai.xyz/download/models-gpu.yaml"],
            ["wget", "-O", f"{answer4}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"{answer4}.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer4}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/gpu_layers.*/gpu_layers: {answer3}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/model.*/model: {answer4}.gguf/g", f"{yaml_path_temp}"],
            ["echo", f"Catting the yaml for easyer debuging..."],
            ["cat", f"{yaml_path_temp}"],
            ["rm", "-f", "localai-chat.tmpl"],
            ["rm", "-f", "localai-chatmsg.tmpl"],
            ["rm", "-f", f"{answer4}.yaml"],
            ["rm", "-f", f"{answer4}.gguf"],
        ]

        docker_commands_vllm = [
            ["echo", f"Setting up the {answer2} model you requested"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.yaml"],
            ["wget", "-O", f"{answer4}.yaml", f"https://tea-cup.midori-ai.xyz/download/models-{answer2}-vllm.yaml"],
            ["cp", f"{answer4}.yaml", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["echo", f"Catting the yaml for easyer debuging..."],
            ["cat", f"{yaml_path_temp}"],
            ["rm", "-f", f"{answer4}.yaml"],
        ]
        
        encrypted_docker_commands_cpu = [
            ["echo", f"Setting up the {answer2} model you requested"],
            ["pip", "install", "psutil", "requests", "diskcache", "cryptography", "aiohttp"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.gguf"],
            ["rm", "-f", f"{inside_model_folder}/localai-chat.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/localai-chatmsg.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.yaml"],
            ["wget", "-O", f"helper_app.py", f"https://tea-cup.midori-ai.xyz/download/helper_app.py"],
            ["python3", "helper_app.py", "localai-chat.tmpl"],
            ["python3", "helper_app.py", "localai-chatmsg.tmpl"],
            ["python3", "helper_app.py", "models.yaml"],
            ["wget", "-O", f"{answer2}model{answer1}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"models.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer2}model{answer1}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/model.*/model: {answer4}.gguf/g", f"{yaml_path_temp}"],
            ["echo", f"Catting the yaml for easyer debuging..."],
            ["cat", f"{yaml_path_temp}"],
            ["rm", "-f", "localai-chat.tmpl"],
            ["rm", "-f", "localai-chatmsg.tmpl"],
            ["rm", "-f", f"models.yaml"],
            ["rm", "-f", f"{answer2}model{answer1}.gguf"],
        ]

        encrypted_docker_commands_gpu = [
            ["echo", f"Setting up the {answer2} model you requested"],
            ["pip", "install", "psutil", "requests", "diskcache", "cryptography", "aiohttp"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.gguf"],
            ["rm", "-f", f"{inside_model_folder}/localai-chat.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/localai-chatmsg.tmpl"],
            ["rm", "-f", f"{inside_model_folder}/{answer4}.yaml"],
            ["wget", "-O", f"helper_app.py", f"https://tea-cup.midori-ai.xyz/download/helper_app.py"],
            ["python3", "helper_app.py", "localai-chat.tmpl"],
            ["python3", "helper_app.py", "localai-chatmsg.tmpl"],
            ["python3", "helper_app.py", "models-gpu.yaml"],
            ["wget", "-O", f"{answer2}model{answer1}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"models-gpu.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer2}model{answer1}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/gpu_layers.*/gpu_layers: {answer3}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/model.*/model: {answer4}.gguf/g", f"{yaml_path_temp}"],
            ["echo", f"Catting the yaml for easyer debuging..."],
            ["cat", f"{yaml_path_temp}"],
            ["rm", "-f", "localai-chat.tmpl"],
            ["rm", "-f", "localai-chatmsg.tmpl"],
            ["rm", "-f", f"models-gpu.yaml"],
            ["rm", "-f", f"{answer2}model{answer1}.gguf"],
        ]

    else:
        docker_commands_cpu = []
        docker_commands_gpu = []

    if answerencrypted == "true":
        docker_commands_cpu = encrypted_docker_commands_cpu
        docker_commands_gpu = encrypted_docker_commands_gpu

    if use_gpu:
        docker_commands = docker_commands_gpu
    else:
        docker_commands = docker_commands_cpu

    if answer1 == "none":
        docker_commands = docker_commands_vllm

    if use_tts == "true":
        tts_commands = [
            ["wget", "-O", inside_model_folder + f"/en_US-amy-medium.onnx.json", f"https://tea-cup.midori-ai.xyz/download/en_US-amy-medium.onnx.json"],
            ["wget", "-O", inside_model_folder + f"/en_US-amy-medium.onnx", f"https://tea-cup.midori-ai.xyz/download/en_US-amy-medium.onnx"],
            ["wget", "-O", inside_model_folder + f"/en-us-kathleen-low.onnx.json", f"https://tea-cup.midori-ai.xyz/download/en-us-kathleen-low.onnx.json"],
            ["wget", "-O", inside_model_folder + f"/en-us-kathleen-low.onnx", f"https://tea-cup.midori-ai.xyz/download/en-us-kathleen-low.onnx"],
        ]
        docker_commands.extend(tts_commands)

    if use_sd == "true":
        sd_commands = [
            ["wget", "-O", inside_model_folder + f"/diffusers.yaml", f"https://tea-cup.midori-ai.xyz/download/diffusers.yaml"]
        ]
        docker_commands.extend(sd_commands)

    if use_enbed == "true":
        embed_commands = [
            ["wget", "-O", inside_model_folder + f"/embedding.yaml", f"https://tea-cup.midori-ai.xyz/download/bert-embeddings.yaml"],
            ["wget", "-O", inside_model_folder + f"/bert-MiniLM-L6-v2q4_0.bin", f"https://tea-cup.midori-ai.xyz/download/bert-MiniLM-L6-v2q4_0.bin"],
        ]
        docker_commands.extend(embed_commands)

    if use_llava == "true":
        llava_commands = [
            ["wget", "-O", inside_model_folder + f"/ggml-model-q4_k.gguf", f"https://huggingface.co/mys/ggml_bakllava-1/resolve/main/ggml-model-q4_k.gguf"],
            ["wget", "-O", inside_model_folder + f"/mmproj-model-f16.gguf", f"https://huggingface.co/mys/ggml_bakllava-1/resolve/main/mmproj-model-f16.gguf"],
            ["wget", "-O", inside_model_folder + f"/chat-simple.tmpl", f"https://github.com/mudler/LocalAI/blob/b8240b4c1839089b9d06a3e2b1c629a294cff87e/examples/configurations/llava/chat-simple.tmpl"],
            ["wget", "-O", inside_model_folder + f"/llava.yaml", f"https://github.com/mudler/LocalAI/blob/b8240b4c1839089b9d06a3e2b1c629a294cff87e/examples/configurations/llava/llava.yaml"],
        ]
        docker_commands.extend(llava_commands)

    # Run a command inside the container
    log("Downloading and setting up model into the docker")
    for command in docker_commands:
        log(f"Running {command}: ")
        command_output = container.exec_run(command)
        log(command_output.output.decode("utf-8"))

    log("All done, I am now rebooting LocalAI")
    container.restart()
    log("Thank you! Please enjoy your new models!")

if answerstartup == 4:
    # Try to load the Docker Compose file
    log("Docker Server error, trying to check your docker-compose.yaml file...")
    docker_compose_found = False
    try:
        log("Loading your docker-compose.yaml")
        with open(compose_path, "r") as f:
            compose_data  = yaml.safe_load(f)
            log("Auto loaded the docker-compose.yaml")
            docker_compose_found = True
    except FileNotFoundError:
        # If the file is not found, ask the user where it is
        log("If you used docker run or just want to try to run this in ``fallback mode`` type ``fallback``")
        compose_path = input("Could not find docker-compose.yaml in the current directory. Where is it located?: ")
        try:
            with open(compose_path, "r") as f:
                compose_data = yaml.safe_load(f)
            log("Loaded the docker-compose.yaml from users path")
        except FileNotFoundError:
            # If the file is still not found, raise an error
            log("Could not find docker-compose.yaml at the specified location. Entering ``fallback mode``")


    # Extract service name and model folder path
    if docker_compose_found:
        for service_name, service_data in compose_data["services"].items():
            log(f"Checking... Service Name: {service_name}, Service Data: {service_data}")
            if service_data["image"].startswith("quay.io/go-skynet/local-ai"):
                models_volume = service_data["volumes"][0]
                models_folder_host = models_volume.split(":")[0]  # Assuming host path is first
                models_folder_container = models_volume.split(":")[1]  # Assuming container path is second
                models_ports = service_data["ports"][0]
                model_port_api = models_ports.split(":")[1]
                service_image = service_data["image"]

                log(f"The inside model folder of the docker is {models_folder_container}, This is were ill place all the files inside of the docker.")
                break

        # If no matching service is found, raise an error
        if service_name not in compose_data["services"]:
            raise Exception("Could not find a service with the image 'quay.io/go-skynet/local-ai' in your docker-compose.yaml file.")
    else:
        clear_window(ver_os_info)
        log("Running ``docker ps``")

        os.system('docker ps -a --format \"table {{.ID}}\t{{.Names}}\"')
        
        service_name = input("What is LocalAI called in ``docker ps`` (Please type the name like this ``localai-api-1`` or ``localai``): ")

        clear_window(ver_os_info)

        models_folder_container = input("Where is LocalAI's models folder located? (IE: ``/models`` or ``/build/models``): ")

        clear_window(ver_os_info)

        os.system('docker ps -a --format \"table {{.Names}}\t{{.Image}}\"')

        service_image = input("What is the full image name that you used? (Please paste the full link. IE: quay.io/go-skynet/local-ai:master-cublas-cuda12-ffmpeg): ")

        clear_window(ver_os_info)

        os.system('docker ps -a --format \"table {{.Names}}\t{{.Ports}}\"')
        models_ports = input("What port are you running LocalAI on?: ")

    clear_window(ver_os_info)

    for container in containers:
        log(f"Checking Name: {container.name}, ID: {container.id}")

        # Check if there is a container with a name containing `service_name`
        if service_name in container.name:
            # Get the container object
            log(f"Found LocalAI, Logging into: {container.name} / {container.id}")
            container = client.containers.get(container.name)
            break

    if container is None:
        log(f"Error: Could not find LocalAI container with name {service_name}")
        log("Checking images again with known names")
        for container in containers:
            log(f"Checking Name: {container.name}, ID: {container.id}")

            # Check if there is a container with a name containing `service_name`
            if service_name in container.name:
                # Get the container object
                log(f"Found LocalAI, Logging into: {container.name} / {container.id}")
                container = client.containers.get(container.name)
                break
        
    clear_window(ver_os_info)

    bearer_token = str(input("If you have a API Key, please put it here: "))
    ip_address = str(input("What is the LocalAI's IP and Port?: "))

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    response = requests.get(f"http://{ip_address}/models", headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        models = response_data["data"]

        # Extract model IDs
        model_ids = [model["id"] for model in models]

        # Print model IDs or perform other operations as needed
        log("Available model IDs:", model_ids)

        clear_window(ver_os_info)

        questionbasic = "What model would you like to uninstall?: "
        valid_answers = model_ids
        answeruninstallmodel = check_str(questionbasic, valid_answers)

        # If the answeruninstallmodel  contains ".yaml" or ".gguf", strip it
        if ".yaml" in answeruninstallmodel or ".gguf" in answeruninstallmodel:
            answeruninstallmodel = answeruninstallmodel.replace(".yaml", "").replace(".gguf", "")

        inside_model_folder = models_folder_container

        docker_commands = [
            ["rm", "-f", f"{inside_model_folder}/{answeruninstallmodel}.gguf"],
            ["rm", "-f", f"{inside_model_folder}/{answeruninstallmodel}.yaml"],
        ]

        # Run a command inside the container
        log("Uninstalling model from the docker")
        for command in docker_commands:
            log(f"Running {command}: ")
            command_output = container.exec_run(command)
            log(command_output.output.decode("utf-8"))

        log("All done, I am now rebooting LocalAI")
        container.restart()
        log("Thank you! Models unintalled!")

    else:
        log("Request failed with status code:", response.status_code)
        log("Response text:", response.text)

if answerstartup == 1:
    try:
        localai_docker = DockerClient(compose_files=["./docker-compose.yaml"])
        
        with open(compose_path, "r") as f:
            compose_yaml = f.read()

        log(f"You Already have localai setup in docker please use the uninstall / reinstall menu to update or remove it")
        input("Hit enter to exit")
        exit()
    except Exception as e:
        log(f"Failed docker check... good")

    try:
        anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])
        
        with open("anythingllm-docker-compose.yaml", "r") as f:
            compose_yaml = f.read()

        log(f"You Already have anythingllm setup in docker please use the uninstall / reinstall menu to update or remove it")
        input("Hit enter to exit")
        exit()
    except Exception as e:
        log(f"Failed docker check... good")
        
    log(containers)

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

    questionbasic = ("Would you like to use GPU with LocalAI? It speeds up LLMs and SD models by 25x: ")
    valid_answers = ["yes", "no", "true", "false"]
    answer_cuda = check_str(questionbasic, valid_answers)

    if answer_cuda.lower() == "no":
        answer_cuda = "False"

    if answer_cuda.lower() == "yes":
        answer_cuda = "True"

    use_cuda = answer_cuda.lower()

    if use_cuda == "true":
        clear_window(ver_os_info)
        os.system("nvidia-smi")
        log('I ran the cuda command, it "should" show you if you have CUDA11 or CUDA12')
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
    use_tts = answertts

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
    log("If you already have a AnythingLLM or WebUI image installed please type ``no``")

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

    if ver_os_info == "linux":
        os.chmod("models", 0o777)
        os.chmod("photos", 0o777)
        os.chmod("others", 0o777)

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
            },
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
                                    {
                                        "driver": "nvidia",
                                        "count": 1,
                                        "capabilities": "changeme",
                                    }
                                ]
                            }
                        }
                    },
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
            },
        }

    log(config)

    # Dump the configuration to a YAML file
    with open(compose_path, "w") as f:
        yaml.dump(config, f, sort_keys=True)

    if use_cuda == "true":
        with open(compose_path, "r") as f:
            # Read the entire contents of the file into a string
            compose_yaml = f.read()

        # Replace all occurrences of 'changeme ' with '["gpu"]' in the string
        compose_yaml = compose_yaml.replace("changeme", '["gpu"]')

        # Write the modified string back to the file
        with open(compose_path, "w") as f:
            f.write(compose_yaml)

    if answeranything == "true":
        log("making folders and docker compose file for AnythingLLM")

        anythingllm_str_env = """
        SERVER_PORT=3001
        STORAGE_DIR="/app/server/storage"
        UID='1000'
        GID='1000'
    """

        log("Making anythingllm docker compose file")

        with open(".env", "w") as f:
            f.write(anythingllm_str_env)

        log("``.env`` saved")

        os.system(f"curl https://tea-cup.midori-ai.xyz/download/anythingllm-docker-compose.yaml -o anythingllm-docker-compose.yaml")

        log("``docker compose`` saved")

        os.makedirs("storage", exist_ok=True)
        os.makedirs("hotdir", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        if ver_os_info == "linux":
            os.chmod("storage", 0o777)
            os.chmod("hotdir", 0o777)
            os.chmod("outputs", 0o777)

        anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])

    log("yaml saved spinning up the docker compose...")
    localai_docker = DockerClient(compose_files=["./docker-compose.yaml"])

    localai_docker.compose.up(
        build=False,
        detach=True,
        no_build=False,
        remove_orphans=True,
        color=True,
        start=True,
        pull="always",
    )

    if answeranything == "true":
        anythingllm_docker.compose.up(
            build=False,
            detach=True,
            no_build=False,
            color=True,
            log_prefix=True,
            start=True,
            pull="always",
        )

    if rebuild:
        log("Due to your CPU not supporting one of the needed things, LocalAI is now rebuilding itself, please wait before installing models or making requests...")
        log("This can take up to 10+ mins to do, sorry for the delay...")

    log("Alright all done, please try out our model installer if you would like us to install some starting models for you <3")
    log("Thank you for using Midori AI's Auto LocalAI installer!")

if answerstartup == 2:
    try:
        localai_docker = DockerClient(compose_files=["./docker-compose.yaml"])
        
        with open(compose_path, "r") as f:
            compose_yaml = f.read()

        log(f"LocalAI Found...")
    except Exception as e:
        log(f"Failed docker check... Please pick to install LocalAI from the main menu...")
        log(f"If you used ``docker run`` please ask on the discord for help on uninstalling the docker")
        input("Hit enter to exit")
        exit()
    
    anything_llm_installed = False

    try:
        anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])
        
        with open("anythingllm-docker-compose.yaml", "r") as f:
            compose_yaml = f.read()

        anything_llm_installed = True
        log(f"AnythingLLM Found...")
    except Exception as e:
        log(f"AnythingLLM not found, doing nothing")
        log(f"If you used ``docker run`` please ask on the discord for help on uninstalling the docker")
        
    log(containers)

    clear_window(ver_os_info)

    questionbasic = "What would you like to do? (Uninstall or Upgrade): "
    valid_answers = ["uninstall", "upgrade", "reinstall", "purge", "down", "up"]
    answeruninstaller = check_str(questionbasic, valid_answers)

    if answeruninstaller == "uninstall":
        answeruninstaller = "down"
    
    if answeruninstaller == "purge":
        answeruninstaller = "down"

    if answeruninstaller == "upgrade":
        answeruninstaller = "up"
    
    if answeruninstaller == "reinstall":
        answeruninstaller = "up"

    clear_window(ver_os_info)

    if answeruninstaller == "down":
        try:
            localai_docker.compose.down(remove_images=True)
            log("Uninstalled LocalAI fully! Thank you for trying LocalAI out!")
        except Exception as e:
            log(f"Error occurred while running docker-compose down: {e}")

        if anything_llm_installed:
            try:
                anythingllm_docker.compose.down(remove_images=True)
                log("Uninstalled AnythingLLM fully! Thank you for trying AnythingLLM out!")
            except Exception as e:
                log(f"Error occurred while running docker-compose down: {e}")

    if answeruninstaller == "up":
        try:
            localai_docker.compose.down(remove_images=True)
            localai_docker.compose.up(build=False, detach=True, no_build=False, color=True, log_prefix=True, start=True, pull="always")
            log("Reinstalled LocalAI fully! If it must rebuild please wait about 10mins or more!")
        except Exception as e:
            log(f"Error occurred while running docker-compose: {e}")

        if anything_llm_installed:
            try:
                anythingllm_docker.compose.down(remove_images=True)
                anythingllm_docker.compose.up(build=False, detach=True, no_build=False, color=True, log_prefix=True, start=True, pull="always")
                log("Reinstalled AnythingLLM fully!")
            except Exception as e:
                log(f"Error occurred while running docker-compose: {e}")


