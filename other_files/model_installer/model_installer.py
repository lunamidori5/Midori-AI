import os
import yaml
import docker
import requests
import datetime
import platform

use_gpu = True

use_sd = False
use_tts = False

use_enbed = False
use_llava = False

compose_path = "docker-compose.yaml"

ver_info = "0.0.102"

now = datetime.datetime.now()
timestamp = now.strftime("%m%d%Y%H%M%S")
log_file_name = "log_" + timestamp + ".txt"

ver_file_name = "model_installer_ver.txt"

with open(log_file_name, "w") as f:
   f.write("Booted and Running Model Installer")

about_model_size = str("""
7b (Small easy to run but barly okay over all) - TheBloke/dolphin-2.6-mistral-7B-GGUF - https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF
43b (Normal sized, great output over all) - TheBloke/dolphin-2.7-mixtral-8x7b-GGUF - https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF
70b (Large, hard to run but great over all) - TheBloke/dolphin-2.2-70B-GGUF - https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF
""")

about_model_q_size = str("""
| Quant Mode | Description |
|Q3| Smallest, significant quality loss - not recommended|
|Q4| Medium, balanced quality|
|Q5| Large, very low quality loss|
|Q6| Very large, extremely low quality loss|
|Q8| Extremely large, No quality loss, hard to install - not recommended|
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
  placeholder_link = f"https://tea-cup.midori-ai.xyz/download/model_installer_{ver_os_info}.zip"

  # Send a request to the server for the model version.
  response = requests.get("https://tea-cup.midori-ai.xyz/download/model_installer_ver.txt")

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
try:
    log("Loading your docker-compose.yaml")
    with open(compose_path, "r") as f:
        compose_data  = yaml.safe_load(f)
        log("Auto loaded the docker-compose.yaml")
except FileNotFoundError:
    # If the file is not found, ask the user where it is
    compose_path = input("Could not find docker-compose.yaml in the current directory. Where is it located?: ") 
    models_path = input("Where is your models folder located?: ")
    try:
        with open(compose_path, "r") as f:
            compose_data = yaml.safe_load(f)
        log("Loaded the docker-compose.yaml from users path")
    except FileNotFoundError:
        # If the file is still not found, raise an error
        log("Could not find docker-compose.yaml at the specified location. Crashing...")
        raise FileNotFoundError("Could not find docker-compose.yaml at the specified location.")


# Extract service name and model folder path
for service_name, service_data in compose_data["services"].items():
    log(f"Checking... Service Name: {service_name}, Service Data: {service_data}")
    if service_data["image"].startswith("quay.io/go-skynet/local-ai"):
        models_volume = service_data["volumes"][0]
        models_folder_host = models_volume.split(":")[0]  # Assuming host path is first
        models_folder_container = models_volume.split(":")[1]  # Assuming container path is second
        models_ports = service_data["ports"][0]
        model_port_api = models_ports.split(":")[1]

        log(f"The inside model folder of the docker is {models_folder_container}, This is were ill place all the files inside of the docker.")
        break

# If no matching service is found, raise an error
if service_name not in compose_data["services"]:
    raise Exception("Could not find a service with the image 'quay.io/go-skynet/local-ai' in your docker-compose.yaml file.")

# Log the name and ID of each container
for container in containers:
    log(f"Checking Name: {container.name}, ID: {container.id}")

    # Check if there is a container with a name containing `service_name`
    if service_name in container.name:
        # Get the container object
        log(f"Found Localai, Logging into: {container.name} / {container.id}")
        container = client.containers.get(container.name)
        break
    
log("\n")
clear_window(ver_os_info)

check_for_update(ver_os_info)

log("Alright, now that I am logged into the docker, lets get you started with installing the model...")
log("For more info on the models used, or links to the models, go to ``https://io.midori-ai.xyz/howtos/easy-model-installer/``")
log(f"I am going to save our chat here and every thing I do to a file called ``{log_file_name}``, check it out if you like <3")
log("Here are a few questions to find out what model you would like to try")


questionbasic = "Would you like to install a LLM?: "
sd_valid_answers = ["yes", "no", "true", "false"]
answerbasic = check_str(questionbasic, sd_valid_answers)

if answerbasic.lower() == "no":
    answerbasic = "False"
        
if answerbasic.lower() == "yes":
    answerbasic = "True"

answerbasic = bool(answerbasic.lower())

if answerbasic:
    clear_window(ver_os_info)
    log(about_model_size)
    valid_answers2 = ["7b", "43b", "70b"]
    question2 = f"What size of known and supported model would you like to setup ({', '.join(valid_answers2)}): "
    answer2 = check_str(question2, valid_answers2)
    answer2 = str(answer2.lower())

    valid_answers1 = ["q3", "q4", "q5", "q6", "q8"] 
    added_valid_answers1 = ["q4-k-m", "q5-k-m"]

    if answer2.lower() == "43b":
        valid_answers1.extend(added_valid_answers1)

    clear_window(ver_os_info)
    log(about_model_q_size)

    question1 = f"What type of model would you like to setup? ({', '.join(valid_answers1)}): "
    answer1 = check_str(question1, valid_answers1)
    answer1 = str(answer1.upper())

    question4 = "\n What would you like to name the models file?: \n"
    answer4 = input(question4)
    answer4 = str(answer4.lower())

    # Check if the word "model" is in the answer
    if "model" in answer4:
        # Remove the word "model"  from the answer
        answer4 = answer4.replace("model", "")

        # Print a message to the user
        log("\nThe word 'model' has been removed from the file name.")


    # Check if GPU is turned on
    if "cuda11" in service_data["image"] or "cuda12" in service_data["image"]:
        # Ask the user the third question
        question3 = "\nNumber of GPU layers to give the model?  (0 to 100): \n"
        answer3 = input(question3)
        answer3 = int(answer3)
        use_gpu = True
    else:
        answer3 = 0
        answer3 = int(answer3)
        use_gpu = False

    clear_window(ver_os_info)

if "ffmpeg" in service_data["image"]:
    questionsd = "Would you like me to install a few Text to Speech models?: "
    sd_valid_answers = ["yes", "no", "true", "false"]
    answertts = check_str(questionsd, sd_valid_answers)

    if answertts.lower() == "no":
        answertts = "False"
        
    if answertts.lower() == "yes":
        answertts = "True"

    answertts = bool(answertts.lower())
    use_tts = answertts

    clear_window(ver_os_info)

if "core" in service_data["image"]:
    log("Looks like you are running a Core Image, Skipping: Stable diffusion, Llava, Huggingface Models")
else:
    if "cuda11" in service_data["image"] or "cuda12" in service_data["image"]:
        questionsd = "Would you like me to install a Stable diffusion model?: "
        sd_valid_answers = ["yes", "no", "true", "false"]
        answersd = check_str(questionsd, sd_valid_answers)

        if answersd.lower() == "no":
            answersd = "False"
        
        if answersd.lower() == "yes":
            answersd = "True"

        answersd = bool(answersd.lower())
        use_sd = answersd
        
        questionsd = "Would you like me to install the Llava model?: "
        sd_valid_answers = ["yes", "no", "true", "false"]
        answerllava = check_str(questionsd, sd_valid_answers)

        if answerllava.lower() == "no":
            answerllava = "False"
        
        if answerllava.lower() == "yes":
            answerllava = "True"

        answerllava = bool(answerllava.lower())
        use_llava = answerllava

        clear_window(ver_os_info)
    else:
        log("Looks like you are running on CPU only, Skipping: Stable diffusion, Llava, Huggingface Models")
    
    questionsd = "Would you like to use our encrypted endpoint for LocalAI to serve and setup the model?: "
    sd_valid_answers = ["yes", "no", "true", "false"]
    answerencrypted = check_str(questionsd, sd_valid_answers)

    if answerencrypted.lower() == "no":
        answerencrypted = "False"
    
    if answerencrypted.lower() == "yes":
        answerencrypted = "True"

    answerencrypted = bool(answerencrypted.lower())

    clear_window(ver_os_info)

questionsd = "Would you like me to install the embedding model?: "
sd_valid_answers = ["yes", "no", "true", "false"]
answerenbed = check_str(questionsd, sd_valid_answers)

if answerenbed.lower() == "no":
    answerenbed = "False"
        
if answerenbed.lower() == "yes":
    answerenbed = "True"

answerenbed = bool(answerenbed.lower())
use_enbed = answerenbed
clear_window(ver_os_info)

log(f"I am now going to install everything you requested, please wait for me to get done. As ill be running commands inside of your docker image.")
log("Hit enter to start")

input()

if answerbasic:
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
    

    encrypted_docker_commands_cpu = [
        ["echo", f"Setting up the {answer2} model you requested"],
        ["pip", "install", "psutil", "requests", "diskcache", "cryptography"],
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

    encrypted_docker_commands_gpu = [
        ["echo", f"Setting up the {answer2} model you requested"],
        ["pip", "install", "psutil", "requests", "diskcache", "cryptography"],
        ["rm", "-f", f"{inside_model_folder}/{answer4}.gguf"],
        ["rm", "-f", f"{inside_model_folder}/localai-chat.tmpl"],
        ["rm", "-f", f"{inside_model_folder}/localai-chatmsg.tmpl"],
        ["rm", "-f", f"{inside_model_folder}/{answer4}.yaml"],
        ["wget", "-O", f"helper_app.py", f"https://tea-cup.midori-ai.xyz/download/helper_app.py"],
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

else:
    docker_commands_cpu = []
    docker_commands_gpu = []

if use_gpu:
    docker_commands = docker_commands_gpu
else:
    docker_commands = docker_commands_cpu

if use_tts:
    tts_commands = [
        ["wget", "-O", inside_model_folder + f"/en_US-amy-medium.onnx.json", f"https://tea-cup.midori-ai.xyz/download/en_US-amy-medium.onnx.json"],
        ["wget", "-O", inside_model_folder + f"/en_US-amy-medium.onnx", f"https://tea-cup.midori-ai.xyz/download/en_US-amy-medium.onnx"],
        ["wget", "-O", inside_model_folder + f"/en-us-kathleen-low.onnx.json", f"https://tea-cup.midori-ai.xyz/download/en-us-kathleen-low.onnx.json"],
        ["wget", "-O", inside_model_folder + f"/en-us-kathleen-low.onnx", f"https://tea-cup.midori-ai.xyz/download/en-us-kathleen-low.onnx"],
    ]
    docker_commands.extend(tts_commands)

if use_sd:
    sd_commands = [
        ["wget", "-O", inside_model_folder + f"/diffusers.yaml", f"https://tea-cup.midori-ai.xyz/download/diffusers.yaml"] # type: ignore
    ]
    docker_commands.extend(sd_commands)

if use_enbed:
    embed_commands = [
        ["curl", f"http://localhost:{model_port_api}/models/apply", "-H", f"\"Content-Type: application/json\"", "-d", "'{\"id\": \"model-gallery@bert-embeddings\"}'"],
    ]
    docker_commands.extend(embed_commands)

if use_llava:
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