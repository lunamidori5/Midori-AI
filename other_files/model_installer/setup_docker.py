import os
import yaml
import GPUtil
import psutil
import platform
import subprocess

import support as s

import edit_models as models_edit_add_on

def dev_setup_docker(DockerClient, compose_path, ver_os_info, containers, use_gui, sg, client, ver_info, layout, client_openai, unused_int, subsystem_file_name):
    CPUCORES = int(psutil.cpu_count())
    os_checker = platform.release()
    known_niv_gpus = s.known_gpus()
    GPUUSE = False
    BOTHUSE = False
    setgpu = False
    update_all = False
    answerupdater = "false"
    subsystem_ver_unraid_mount = "subsystem_unraid_mount.ram"
    subsystem_ver_auto_update = "subsystem_auto_update.ram"
    base_image_name = "lunamidori5/midori_ai_subsystem"

    docker_compose_yaml = "midori-docker-compose.yaml"

    discord_id = s.get_uuid_id()

    try:
        gpus = GPUtil.getGPUs()

        # Check if any of the GPUs are NVIDIA GPUs
        s.log("Checking for GPUs")
        for gpu in gpus:
            s.log(str("Found an GPU: {}".format(gpu.name)))
            for known_gpu in known_niv_gpus:
                if gpu.name.startswith(known_gpu):
                    setgpu = True
                    s.log(str("Found an NVIDIA GPU: {}".format(gpu.name)))
    except:
        s.log("No GPUs found, setting to false")
        setgpu = False
        
    s.log(containers)

    s.clear_window(ver_os_info)

    if os.path.exists(subsystem_ver_unraid_mount):
        with open(subsystem_ver_unraid_mount, 'r') as f:
            vol_mountpoint = str(f.read())
    else:
        if "Unraid" in os_checker:
            s.log("Unraid seen")
            if "MIDORI_AI_MOUNT_POINT" in os.environ:
                vol_mountpoint = os.environ["MIDORI_AI_MOUNT_POINT"]
            else:
                vol_mountpoint = input("Please enter a mountpoint - (/mnt/user/appdata/MidoriAI): ")
                while True:
                    confirmation = input("Are you sure this is the correct mountpoint? (y/n): ")
                    if confirmation.lower() == "y":
                        break
                    elif confirmation.lower() == "n":
                        s.clear_window(ver_os_info)
                        vol_mountpoint = input("Please enter a mountpoint - (/mnt/user/appdata/MidoriAI): ")
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            
            with open(subsystem_ver_unraid_mount, 'w') as f:
                f.write(vol_mountpoint)
        else:
            vol_mountpoint = "/var/lib/docker/volumes/midoriai_midori-ai"

    s.clear_window(ver_os_info)

    if os.path.exists(os.path.join("files", subsystem_file_name)):
        s.log("You have already setup the Midori AI subsystem, Updating it!")
        CPUCORES = int(psutil.cpu_count())
        with open(os.path.join("files", '1stbooleans.txt'), 'r') as f:
            GPUUSE = str(f.read())
        with open(os.path.join("files", '2ntbooleans.txt'), 'r') as f:
            BOTHUSE = str(f.read())
        if GPUUSE == "False":
            GPUUSE = False
            BOTHUSE = False
        else:
            GPUUSE = True
            BOTHUSE = True

        update_all = True

    else:
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
            exit(404)

        s.clear_window(ver_os_info)

        question = "Would you like me to auto update / start the backends that are installed in the Subsystem?: "
        valid_answers = ["yes", "no", "true", "false"]
        
        context_temp = f"The user was asked if they would like to auto update the backends that are installed in the Midori AI Docker Subsystem. This is a yes or no question. Tell the user to type ``yes`` for most usecases"
            
        answerupdater = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

        if answerupdater.lower() == "no":
            answerupdater = "False"

        if answerupdater.lower() == "yes":
            answerupdater = "True"

        answerupdater = answerupdater.lower()

        s.clear_window(ver_os_info)

        if setgpu == True:
            GPUUSE = True
            BOTHUSE = True
        else:
            GPUUSE = False
            BOTHUSE = False

        if setgpu == True:
            question = "Do you have the NVIDIA Toolkit (nvidia-smi) installed? (type ``help`` if unsure): "
            valid_answers = ["yes", "no", "true", "false"]
            
            context_temp = f"The user was asked if they would like to use GPU for the Midori AI Docker Subsystem and other AI Images. This is a yes or no question."
            context_temp = f"{context_temp}\nThis is the output of the nvidia-smi command\n{str(os.popen('nvidia-smi').read())}\nIf the user does not have cuda installed please tell them to type no"
            context_temp = f"{context_temp}\nIf the user has CUDA installed let them know what type (12 or 11) and to type ``yes``, do not give other info in this menu"
                
            answer_backend_type = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

            if answer_backend_type.lower() == "yes":
                s.log("Okay, let me assist with checking your install...")
                s.log("I'll try to call ``nvidia-smi`` now, if you get an error or a message about it not being found then it's not installed.")
                try:
                    rc = subprocess.check_call("nvidia-smi", shell=True)
                    if rc == 0:
                        s.log("Alright! You do have ``nvidia-smi`` installed and it looks good to use CUDA!")
                        input("Press enter to keep going: ")
                    else:
                        print(5/0)
                except Exception as e:
                    s.log("It seems ``nvidia-smi`` did not run correctly, please make sure it's installed and then if it is working properly, run this setup again.")
                    s.log("``https://developer.nvidia.com/cuda-downloads``")
                    GPUUSE = False
                    BOTHUSE = False
                    input("Press enter to keep going on CPU only / Exit and install Docker CUDA to use GPU:")
            else:
                s.log("Okay, that's totally fine! You do not need a GPU or CUDA to run this script.")
                s.log("Just know that having one can speed things up a little.")
                GPUUSE = False
                BOTHUSE = False
        
        with open(os.path.join("files", '1stbooleans.txt'), 'w') as f:
            f.write(str(GPUUSE))

        with open(os.path.join("files", '2ntbooleans.txt'), 'w') as f:
            f.write(str(BOTHUSE))

        s.clear_window(ver_os_info)
        s.log("Setting up the Midori AI Docker Subsystem...")

        s.log("I am now going to install everything you requested, please wait for me to get done.")

        input("Hit enter to start: ")

    os.makedirs("files", exist_ok=True)

    if ver_os_info == "linux":
        os.chmod("files", 0o777)

    if GPUUSE:
        config = {
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
                        "DISCORD_ID": discord_id,
                    },  # env_file is commented out
                    "volumes": ["./:/app/system_files", "./files:/app/files", "midori-ai:/app/int-files", f"{vol_mountpoint}-models/_data:/app/models", f"{vol_mountpoint}-images/_data:/app/images", f"{vol_mountpoint}-audio/_data:/app/audio", "/var/run/docker.sock:/var/run/docker.sock"],
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
                        "DISCORD_ID": discord_id,
                    },  # env_file is commented out
                    "volumes": ["./:/app/system_files", "./files:/app/files", "midori-ai:/app/int-files", f"{vol_mountpoint}-models/_data:/app/models", f"{vol_mountpoint}-images/_data:/app/images", f"{vol_mountpoint}-audio/_data:/app/audio", "/var/run/docker.sock:/var/run/docker.sock"],
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

    with open(os.path.join("files", subsystem_file_name), "w") as f:
        f.write(ver_info)

    if answerupdater == "true":
        with open(os.path.join("files", subsystem_ver_auto_update), "w") as f:
            f.write(ver_info)
        
        if os.path.exists(os.path.join("files", subsystem_ver_auto_update)):
            models_edit_add_on.subsystem_backend_manager.backend_updater(None, "midori-docker-compose.yaml", client, ver_os_info)


    if update_all:
        if os.path.exists(os.path.join("files", subsystem_ver_auto_update)):
            models_edit_add_on.subsystem_backend_manager.backend_updater(None, "midori-docker-compose.yaml", client, ver_os_info)



    # s.log("All done, I am now rebooting the subsystem")
    # container.restart()

    s.log("Thank you for using Midori AI's Docker SubSystem!")
    input("Please press enter to go back to the main menu: ")