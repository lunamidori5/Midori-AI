import os
import json
import yaml
import docker
import requests
import datetime
import platform

compose_path = "docker-compose.yaml"

ver_info = "changemelunaplease"

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y%H%M%S")
log_file_name = "log_" + timestamp + ".txt"

ver_file_name = "midori_program_ver.txt"

with open(log_file_name, "w") as f:
   f.write("Booted and Running Model Installer")

about_model_size = str("""
7b (Small easy to run but okay quality over all) - https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF
43b (Normal sized, great quality over all) - https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF
70b (Large, hard to run but significant quality over all) - https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF
ID (These are models from the Midori AI model repo) - https://io.midori-ai.xyz/models/
""")

about_model_q_size = str("""
| Quant Mode | Description |
|Q3| Smallest, significant quality loss - not recommended|
|Q4| Medium, balanced quality|
|Q5| Large, very low quality loss|
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
    placeholder_link = f"https://tea-cup.midori-ai.xyz/download/model_installer_{ver_os_info}"

    if ver_os_info == 'windows':
        placeholder_link = placeholder_link + ".zip"
    if ver_os_info == 'linux':
        placeholder_link = placeholder_link + ".tar.gz"

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
    os.system('title LocalAI Model Installer')
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

# Log the name and ID of each container
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

check_for_update(ver_os_info)

log("\n")

log(f"-----------------------------------------------------------------------------------------------")
log(f"------------------------------------------ Main Menu ------------------------------------------")
log(f"-----------------------------------------------------------------------------------------------")

log("``1`` - Setup / Upgrade Models")
log("``2`` - Uninstall Models")

questionbasic = "What would you like to do?: "
sd_valid_answers = ["1", "2"]
answerstartup = check_str(questionbasic, sd_valid_answers)

answerstartup = int(answerstartup)

clear_window(ver_os_info)

if answerstartup == 1:
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
                question3 = "\nNumber of GPU layers to give the model?  (0 to 100): \n"
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
        
        questionsd = "Would you like to use our slower but encrypted endpoint for LocalAI to serve and setup the model? (Not Recommend): "
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
            ["python3", "helper_app.py", f"{answer2}model{answer1}.gguf"],
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
            ["python3", "helper_app.py", f"{answer2}model{answer1}.gguf"],
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

if answerstartup == 2:
    bearer_token = str(input("Do you have a API Key on your models endpoint?"))
    ip_address = str(input("What is the LocalAI's IP and Port? "))

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