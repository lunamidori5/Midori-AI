import os
import yaml

import support as s

def setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, base_image_name, localai_ver_number, layout, client_openai):
    try:
        localai_docker = DockerClient(compose_files=["./docker-compose.yaml"])
        
        with open(compose_path, "r") as f:
            compose_yaml = f.read()

        s.log(f"You Already have localai setup in docker please use the uninstall / reinstall menu to update or remove it")
        input("Hit enter to exit")
        return
    except Exception as e:
        s.log(f"Failed docker check... good")

    try:
        anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])
        
        with open("anythingllm-docker-compose.yaml", "r") as f:
            compose_yaml = f.read()

        s.log(f"You Already have anythingllm setup in docker please use the uninstall / reinstall menu to update or remove it")
        input("Hit enter to exit")
        return
    except Exception as e:
        s.log(f"Failed docker check... good")
        
    s.log(containers)

    rebuild = s.check_cpu_support()
    backend_type = False

    s.clear_window(ver_os_info)

    if rebuild:
        s.log("The CPU does not support the required features. Rebuilding is necessary.")
    else:
        s.log("The CPU supports the required features. No need to rebuild.")

    s.log("Alright, now that I am logged into the docker, lets get you started with installing the model...")
    s.log(f"I am going to save our chat here and every thing I do to a log file, check it out if you like <3")
    s.log("Here are a few questions about how you want me to setup your LocalAI docker image...")

    question = "Would you like me to install LocalAI in docker to this computer?: "
    valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to install LocalAI. This is a yes or no question."
        
    answerbasic = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answerbasic.lower() == "no":
        answerbasic = "False"

    if answerbasic.lower() == "yes":
        answerbasic = "True"

    answerbasic = answerbasic.lower()

    if answerbasic == "false":
        s.log("Alright then ill go ahead and exit! Thank you!")
        return

    s.clear_window(ver_os_info)

    s.log("LocalAI offers a ``master`` image.")
    s.log("This image maybe unstable or have bugs but will let you test out the newer models.")

    question = "Would you like to try the ``master`` image?: "
    valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"LocalAI offers a ``master`` image.", size=(100, 1))],
                [sg.Text(f"This image maybe unstable or have bugs but will let you test out the newer models.", size=(100, 1))],
                [sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to use master (nightly) image of LocalAI. This is a yes or no question."
        
    answermaster = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answermaster.lower() == "no":
        answermaster = "False"

    if answermaster.lower() == "yes":
        answermaster = "True"

    answermaster = answermaster.lower()

    s.clear_window(ver_os_info)

    s.log("This setting lets you use only one backend at a time, it is HIGHLY recommended to type ``yes`` here")

    question = "Would you like to turn on ``SINGLE_ACTIVE_BACKEND``?: "
    valid_answers = ["yes", "no", "true", "false"]
    
    context_temp = f"The user was asked if they would like to use SINGLE_ACTIVE_BACKEND setting of LocalAI. Tell them its best to type yes! This is a yes or no question."
        
    answer_backend_type = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answer_backend_type.lower() == "no":
        backend_type = False

    if answer_backend_type.lower() == "yes":
        backend_type = True

    if answer_backend_type.lower() == "false":
        backend_type = False

    if answer_backend_type.lower() == "true":
        backend_type = True

    s.clear_window(ver_os_info)

    s.log("Sadly I am unable to check your CUDA install for GPU, If you have it already installed good!")
    s.log("If not please stop by ``https://developer.nvidia.com/cuda-downloads`` and get it for your OS, WSL is Linux")
    s.log("If you do not have CUDA installed or use a card that does not support it please type no...")

    question = ("Would you like to use GPU with LocalAI? It speeds up LLMs and SD models by 25x: ")
    valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"Sadly I am unable to check your CUDA install for GPU, If you have it already installed good!", size=(100, 1))],
                [sg.Text(f"If not please stop by ``https://developer.nvidia.com/cuda-downloads`` and get it for your OS, WSL is Linux", size=(100, 1))],
                [sg.Text(f"If you do not have CUDA installed or use a card that does not support it please type no...", size=(100, 1))],
                [sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to use GPU with LocalAI using Cuda. This is a yes or no question."
        
    answer_cuda = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answer_cuda.lower() == "no":
        answer_cuda = "False"

    if answer_cuda.lower() == "yes":
        answer_cuda = "True"

    use_cuda = answer_cuda.lower()

    if use_cuda == "true":
        s.clear_window(ver_os_info)
        os.system("nvidia-smi")
        s.log('I ran the cuda command, it "should" show you if you have CUDA11 or CUDA12')
        question = "Do you have CUDA11 or CUDA12? (Type just 11 or 12): "
        valid_answers = ["11", "12"]
        context_temp = f"The user was asked if they would like to use GPU with LocalAI using Cuda."
        context_temp = f"{context_temp}\nThis is the output of the nvidia-smi command\n{str(os.popen('nvidia-smi').read())}\nThe user needs to know if they have cuda 11 or cuda 12"
        version = s.check_str(question, valid_answers, "no", layout, sg, context_temp, client_openai)

    s.clear_window(ver_os_info)

    question = "Would you like me to add TTS / Audio support to LocalAI?: "
    valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to add TTS aka Text to Speach support to LocalAI. This is a yes or no question."
        
    answertts = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answertts.lower() == "no":
        answertts = "False"

    if answertts.lower() == "yes":
        answertts = "True"

    answertts = answertts.lower()
    use_tts = answertts

    s.clear_window(ver_os_info)

    question = "LocalAI offers a ``core`` image that lowers the image size by more than 60% \nInstalling this image removes support for all non LLM, Embedding, or TTS models.\nThis also removes the encrypted endpoint of the model installer. \nWould you like to use the core image? (Not Recommended): "
    valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to use the core image of LocalAI. This is a yes or no question. This is HIGHLY NOT recommended."
        
    answercore = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answercore.lower() == "no":
        answercore = "False"

    if answercore.lower() == "yes":
        answercore = "True"

    answercore = answercore.lower()

    s.clear_window(ver_os_info)

    s.log("We have a docker ready if you would like to try it, its called AnythingLLM, its a GUI or WebUI for LocalAI. It comes highly recommened for new users.")
    s.log("If you already have a AnythingLLM or WebUI image installed please type ``no``")

    question = "Would you like me to install AnythingLLM in a docker next to LocalAI?"
    valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to install AnythingLLM, a chat app that goes with LocalAI. This is a yes or no question."
        
    answeranything = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answeranything.lower() == "no":
        answeranything = "False"

    if answeranything.lower() == "yes":
        answeranything = "True"

    answeranything = answeranything.lower()

    s.clear_window(ver_os_info)

    s.log("Alright lets get everything together...")

    if answermaster == "true":
        s.log("you requested to use the master image, Ill add that to the compose file now!")
        user_image = "master"

    else:
        s.log(f"you requested to not use the master image, Ill set you to ``{localai_ver_number}`` image then! Adding that to your compose file!")
        user_image = localai_ver_number

    if use_cuda == "true":
        s.log("cuda is installed, setup, and requested. Adding that to the docker-compose file now <3")
        user_image = user_image + "-cublas-cuda"
        user_image = user_image + version

    if use_tts == "true":
        s.log("looks like you requested TTS / Audio support, Ill get that added now!")
        user_image = user_image + "-ffmpeg"

    if answercore == "true":
        s.log("looks like you wish to use the smaller core image. Ill add that to your docker-compose.yaml")
        user_image = user_image + "-core"

    s.log("I am now going to install everything you requested, please wait for me to get done.")
    s.log("Hit enter to start")

    input()

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
                        "SINGLE_ACTIVE_BACKEND": str(backend_type).lower(),
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
                        "SINGLE_ACTIVE_BACKEND": str(backend_type).lower(),
                    },  # env_file is commented out
                    "volumes": ["./models:/models", "./photos:/tmp/generated/images/"],
                    "command": ["/usr/bin/local-ai"],
                }
            },
        }

    s.log(config)

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
        s.log("making folders and docker compose file for AnythingLLM")

        anythingllm_str_env = """
        SERVER_PORT=3001
        STORAGE_DIR="/app/server/storage"
        UID='1000'
        GID='1000'
    """

        s.log("Making anythingllm docker compose file")

        with open(".env", "w") as f:
            f.write(anythingllm_str_env)

        s.log("``.env`` saved")

        os.system(f"curl https://tea-cup.midori-ai.xyz/download/anythingllm-docker-compose.yaml -o anythingllm-docker-compose.yaml")

        s.log("``docker compose`` saved")

        os.makedirs("storage", exist_ok=True)
        os.makedirs("hotdir", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)

        if ver_os_info == "linux":
            os.chmod("storage", 0o777)
            os.chmod("hotdir", 0o777)
            os.chmod("outputs", 0o777)

        anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])

    s.log("yaml saved spinning up the docker compose...")
    localai_docker = DockerClient(compose_files=["./localai-docker-compose.yaml"])

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
        s.log("Due to your CPU not supporting one of the needed things, LocalAI is now rebuilding itself, please wait before installing models or making requests...")
        s.log("This can take up to 10+ mins to do, sorry for the delay...")

    s.log("Alright all done, please try out our model installer if you would like us to install some starting models for you <3")
    s.log("Thank you for using Midori AI's Auto LocalAI installer!")

def change_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, layout, client_openai):
    try:
        localai_docker = DockerClient(compose_files=["./localai-docker-compose.yaml"])
        
        with open(compose_path, "r") as f:
            compose_yaml = f.read()

        s.log(f"LocalAI Found...")
    except Exception as e:
        s.log(f"Failed docker check... Please pick to install LocalAI from the main menu...")
        s.log(f"If you used ``docker run`` please ask on the discord for help on uninstalling the docker")
        input("Hit enter to exit")
        return
    
    anything_llm_installed = False

    try:
        anythingllm_docker = DockerClient(compose_files=["./anythingllm-docker-compose.yaml"])
        
        with open("anythingllm-docker-compose.yaml", "r") as f:
            compose_yaml = f.read()

        anything_llm_installed = True
        s.log(f"AnythingLLM Found...")
    except Exception as e:
        s.log(f"AnythingLLM not found, doing nothing")
        s.log(f"If you used ``docker run`` please ask on the discord for help on uninstalling the docker")
        
    s.log(containers)

    s.clear_window(ver_os_info)

    question = "What would you like to do? (Uninstall or Upgrade): "
    valid_answers = ["uninstall", "upgrade", "reinstall", "purge", "down", "up"]

    if use_gui == "yes":
        layout = [[sg.Text(f"{question}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
    
    context_temp = f"The user was asked if they would like to uninstall or reinstall the docker image for LocalAI. These are the things they can pick from {str(valid_answers)}"
        
    answeruninstaller = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

    if answeruninstaller == "uninstall":
        answeruninstaller = "down"
    
    if answeruninstaller == "purge":
        answeruninstaller = "down"

    if answeruninstaller == "upgrade":
        answeruninstaller = "up"
    
    if answeruninstaller == "reinstall":
        answeruninstaller = "up"

    s.clear_window(ver_os_info)

    if answeruninstaller == "down":
        try:
            localai_docker.compose.down(remove_images="all")
            s.log("Uninstalled LocalAI fully! Thank you for trying LocalAI out!")
        except Exception as e:
            s.log(f"Error occurred while running docker-compose down: {e}")

        if anything_llm_installed:
            try:
                anythingllm_docker.compose.down(remove_images="all")
                s.log("Uninstalled AnythingLLM fully! Thank you for trying AnythingLLM out!")
            except Exception as e:
                s.log(f"Error occurred while running docker-compose down: {e}")

    if answeruninstaller == "up":
        try:
            localai_docker.compose.down(remove_images="all")
            localai_docker.compose.up(build=False, detach=True, no_build=False, color=True, log_prefix=True, start=True, pull="always")
            s.log("Reinstalled LocalAI fully! If it must rebuild please wait about 10mins or more!")
        except Exception as e:
            s.log(f"Error occurred while running docker-compose: {e}")

        if anything_llm_installed:
            try:
                anythingllm_docker.compose.down(remove_images="all")
                anythingllm_docker.compose.up(build=False, detach=True, no_build=False, color=True, log_prefix=True, start=True, pull="always")
                s.log("Reinstalled AnythingLLM fully!")
            except Exception as e:
                s.log(f"Error occurred while running docker-compose: {e}")

def dev_setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, client, ver_info, layout, client_openai, discord_id):
    
    CPUCORES = 1
    GPUUSE = False
    BOTHUSE = False
    user_name = "placeholder"
    base_image_name = "lunamidori5/midori_ai_subsystem"

    docker_compose_yaml = "midori-docker-compose.yaml"

    s.log(f"Skipping subsystem check, will auto purge if its installed...")
        
    s.log(containers)

    s.clear_window(ver_os_info)

    if os.path.exists(os.path.join("files", "subsystem.ram")):
        s.log("You have already setup the Midori AI subsystem, Updating it!")
        with open(os.path.join("files", 'booleans.txt'), 'r') as f:
            GPUUSE = bool(f.readline())
            BOTHUSE = bool(f.readline())
    else:
        s.log("Your username will not get passed or shared with Midori AI, it is just a way to make sure your image is safe")

        user_name = str(input("Please enter a Username: "))

        s.clear_window(ver_os_info)

        s.log("This is the menu to setup the Midori AI Docker Subsystem! ")

        question = "Would you like me to install Subsystem in docker to this computer?: "
        valid_answers = ["yes", "no", "true", "false"]
        
        context_temp = f"The user was asked if they would like to install the Midori AI Docker Subsystem. This is a yes or no question."
            
        answerbasic = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

        if answerbasic.lower() == "no":
            answerbasic = "False"

        if answerbasic.lower() == "yes":
            answerbasic = "True"

        answerbasic = answerbasic.lower()

        if answerbasic == "false":
            s.log("Alright then ill go ahead and exit! Thank you!")
            return

        s.clear_window(ver_os_info)

        s.log("Sadly I am unable to check your CUDA install for GPU, If you have it already installed good!")
        s.log("If not please stop by ``https://developer.nvidia.com/cuda-downloads`` and get it for your OS, WSL is Linux")
        s.log("If you do not have CUDA installed or use a card that does not support it please type no...")
        s.log("This setting lets you use GPU and CPU for AI images in the subsystem.")

        question = "Would you like to use GPU and CPU for mixed AI images?: "
        valid_answers = ["yes", "no", "true", "false"]
        
        context_temp = f"The user was asked if they would like to use GPU for the Midori AI Docker Subsystem and other AI Images. This is a yes or no question."
        context_temp = f"{context_temp}\nThis is the output of the nvidia-smi command\n{str(os.popen('nvidia-smi').read())}\nIf the user does not have cuda installed please tell them to type no"
            
        answer_backend_type = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

        if answer_backend_type.lower() == "no":
            GPUUSE = False
            BOTHUSE = False

        if answer_backend_type.lower() == "yes":
            GPUUSE = True
            BOTHUSE = True

        if answer_backend_type.lower() == "false":
            GPUUSE = False
            BOTHUSE = False

        if answer_backend_type.lower() == "true":
            GPUUSE = True
            BOTHUSE = True
        
        with open(os.path.join("files", 'booleans.txt'), 'w') as f:
            f.write(str(GPUUSE)  + '\n')
            f.write(str(BOTHUSE) + '\n')

        s.clear_window(ver_os_info)
        s.log("Setting up the Midori AI Docker Subsystem...")

        s.log("I am now going to install everything you requested, please wait for me to get done.")
        s.log("Hit enter to start")

        input()

    os.makedirs("files", exist_ok=True)

    if ver_os_info == "linux":
        os.chmod("files", 0o777)

    if GPUUSE:
        config = {
            "version": "3.6",
            "services": {
                "midori_ai_subsystem": {
                    "deploy": {
                        "resources": {
                            "reservations": {
                                "devices": [
                                    {
                                        "driver": "nvidia",
                                        "count": "all",
                                        "capabilities": "changeme",
                                    }
                                ]
                            }
                        }
                    },
                    "image": f"{base_image_name}",
                    "tty": True,
                    "restart": "always",
                    "ports": ["9090:9090"],
                    "privileged": True,
                    "environment": {
                        "CPUCORES": CPUCORES,
                        "GPUUSE": GPUUSE,
                        "BOTHUSE": BOTHUSE,
                        "USERNAME": user_name,
                        "DISCORD_ID": discord_id,
                    },  # env_file is commented out
                    "volumes": ["./files:/app/files", "midori-ai:/app/int-files", "midori-ai-models:/app/models", "midori-ai-images:/app/images", "midori-ai-audio:/app/audio", "/var/run/docker.sock:/var/run/docker.sock"],
                }
            },
			"volumes": {
				"midori-ai": {
					"external": False
				},
				"midori-ai-models": {
					"external": False
				},
				"midori-ai-images": {
					"external": False
				},
				"midori-ai-audio": {
					"external": False
				},
			},
        }


    else:
        config = {
            "version": "3.6",
            "services": {
                "midori_ai_subsystem": {
                    "image": f"{base_image_name}",
                    "tty": True,
                    "restart": "always",
                    "ports": ["9090:9090"],
                    "privileged": True,
                    "environment": {
                        "CPUCORES": CPUCORES,
                        "GPUUSE": GPUUSE,
                        "BOTHUSE": BOTHUSE,
                        "USERNAME": user_name,
                        "DISCORD_ID": discord_id,
                    },  # env_file is commented out
                    "volumes": ["./files:/app/files", "midori-ai:/app/int-files", "midori-ai-models:/app/models", "midori-ai-images:/app/images", "midori-ai-audio:/app/audio", "/var/run/docker.sock:/var/run/docker.sock"],
                }
            },
			"volumes": {
				"midori-ai": {
					"external": False
				},
				"midori-ai-models": {
					"external": False
				},
				"midori-ai-images": {
					"external": False
				},
				"midori-ai-audio": {
					"external": False
				},
			},
        }

    s.log(config)

    # Dump the configuration to a YAML file
    with open(docker_compose_yaml, "w") as f:
        yaml.dump(config, f, sort_keys=True)

    if GPUUSE:
        with open(docker_compose_yaml, "r") as f:
            # Read the entire contents of the file into a string
            compose_yaml = f.read()

        # Replace all occurrences of 'changeme ' with '["gpu"]' in the string
        compose_yaml = compose_yaml.replace("changeme", '["gpu"]')

        # Write the modified string back to the file
        with open(docker_compose_yaml, "w") as f:
            f.write(compose_yaml)

    s.log("yaml saved spinning up the docker compose...")
    midori_ai_subsystem = DockerClient(compose_files=[f"./{docker_compose_yaml}"])

    midori_ai_subsystem.compose.down(remove_images="all")

    midori_ai_subsystem.compose.up(
        build=False,
        detach=True,
        no_build=False,
        remove_orphans=False,
        color=True,
        start=True,
        pull="always",
    )

    with open(os.path.join("files", "subsystem.ram"), "w") as f:
        f.write(ver_info)

    # s.log("All done, I am now rebooting the subsystem")
    # container.restart()

    s.log("Thank you for using Midori AI's Docker SubSystem!")
    input("Please press enter to go back to the main menu: ")