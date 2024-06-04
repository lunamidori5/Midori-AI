import os
import GPUtil
import platform

import support as s

from colorama import Fore

class subsystem_backend_manager:
    def backend_installer(self, docker_compose_yaml, client, client_openai, ver_os_info, discord_id):
        setgpu = False
        known_niv_gpus = s.known_gpus()
        containers = client.containers.list()
        backend_checker = s.backends_checking()
        installed_backends = backend_checker.check_json()
        os_checker = platform.release()

        subsystem_ver_unraid_mount = "subsystem_unraid_mount.ram"

        list_of_supported_backends = [
            "localai", 
            "anythingllm",
            "ollama",
            "axolotl",
            "invokeai",
            "chromadb",
            "autogpt",
            "bigagi"
            ]
        
        """
        list_of_supported_backends = [
            "localai", 
            "anythingllm", 
            "ollama",
            "invokeai",
            "oobabooga",
            "home-assistant",
            "midoricluster"
            ]
        """
        
        list_of_supported_backends = [
            item for item in list_of_supported_backends if item not in installed_backends
        ]
        
        s.clear_window(ver_os_info)

        try:
            gpus = GPUtil.getGPUs()

            # Check if any of the GPUs are NVIDIA GPUs
            s.log("Checking for GPUs")
            for gpu in gpus:
                s.log(str("Found an GPU: {}".format(gpu.name)))
                for known_gpu in known_niv_gpus:
                    if gpu.name.startswith(known_gpu):
                        setgpu = True
                        print("Found an NVIDIA GPU: {}".format(gpu.name))
                        s.log(str("Found an NVIDIA GPU: {}".format(gpu.name)))
        except:
            s.log("No GPUs found, setting to false")
            setgpu = False
        
        if setgpu == True:
            question = "Would you like to use GPU and CPU for these new backends?: "
            valid_answers = ["yes", "no", "true", "false"]
            
            context_temp = f"The user was asked if they would like to use GPU for the Midori AI Docker Subsystem and other AI Images. This is a yes or no question."
            context_temp = f"{context_temp}\nThis is the output of the nvidia-smi command\n{str(os.popen('nvidia-smi').read())}\nIf the user does not have cuda installed please tell them to type no"
                
            answer_backend_type = s.check_str(question, valid_answers, "no", None, None, context_temp, client_openai)

            if answer_backend_type.lower() == "no":
                GPUUSE = False

            if answer_backend_type.lower() == "yes":
                GPUUSE = True

            if answer_backend_type.lower() == "false":
                GPUUSE = False

            if answer_backend_type.lower() == "true":
                GPUUSE = True

            s.clear_window(ver_os_info)
        else:
            GPUUSE = False

            s.log(f"You are running on CPU only.")
        
        str_temp = f"``localai and anythingllm`` or ``localai, anythingllm, and invokeai``"
        s.log(f"{str(list_of_supported_backends).lower()}")
        s.log("Please pick from this list of supported AI backends to add to the subsystem.")
        s.log(f"You can list them out like this. {str_temp}")
        s.log(f"Or type ``all`` to install all supported backends")
        s.log(f"Type ``back`` to go back to the main menu")

        picked_backends = str(input("Request Backends: ")).lower()
        requested_backends = []

        if picked_backends == "back":
            return

        if picked_backends == "all":
            picked_backends = str(list_of_supported_backends)
        
        if "oobabooga" in picked_backends:
            picked_backends = picked_backends + " oobaboogaapi"

        if "localai" in picked_backends:
            print(Fore.RED + 'Warning:' + Fore.WHITE + ' Please note that this will download about 20gbs or more to your host drive')
            print(Fore.RED + 'Warning:' + Fore.WHITE + ' If this is not okay please type ``no``')
            exitout = input("Press enter to install LocalAI: ")
            
            if exitout == "no":
                return
        
        for item in list_of_supported_backends:
            if item in picked_backends:
                requested_backends.append(item)

        for container in containers:
            s.log(f"Checking Name: {container.name}, ID: {container.id}")
            if "midori_ai_subsystem" in container.name:
                s.log(f"Found the subsystem, logging into: {container.name} / {container.id}")
                container = client.containers.get(container.name)
                break
    
        docker_commands = [
            f"echo Installing New Backends",
                ]
        backends = backend_checker.check_json()
        for item in requested_backends:
            s.log(f"Requesting config and commands to install {item}")
            download_item = f"{item}-subsystem-install"
            backend_checker.add_backend(item)
            
            if GPUUSE:
                download_item = f"{download_item}-gpu"

            decrypted_commands = bytes(s.download_commands(f"https://tea-cup.midori-ai.xyz/download/{download_item}.json", str(discord_id))).decode()
            for command in decrypted_commands.splitlines():
                command = command.strip()
                if command and not command.startswith("#"): 
                    docker_commands.append(command)

        s.log("Running commands inside of the Midori AI Subsystem!")
        for item_docker in docker_commands:
            s.log(f"Running {item_docker}")
            void, stream = container.exec_run(item_docker, stream=True)
            for data in stream:
                s.log(data.decode())
        
        for item_os in requested_backends:

            if os.path.exists(subsystem_ver_unraid_mount):
                with open(subsystem_ver_unraid_mount, 'r') as f:
                    vol_mountpoint = str(f.read())
            else:
                vol_mountpoint = "/var/lib/docker/volumes/midoriai_midori-ai"

            with open(f"/app/files/{item_os}/docker-compose.yaml", "r") as f:
                compose_yaml = f.read()

            compose_yaml = compose_yaml.replace("changememountpointgobrr", vol_mountpoint)

            with open(f"/app/files/{item_os}/docker-compose.yaml", "w") as f:
                f.write(compose_yaml)

            s.log(f"Running: docker compose -f ./files/{item_os}/docker-compose.yaml up -d")

            if "Unraid" in os_checker:
                os.system(f"docker compose -f /app/files/{item_os}/docker-compose.yaml up -d")
            else:
                os.system(f"docker compose -f ./files/{item_os}/docker-compose.yaml up -d")
        
        for backend_port in requested_backends:
            normal_port = s.get_port_number(backend_port)
            s.log(f"We are running {backend_port} on {normal_port}")

        input("Please press enter to go back to the main menu: ")

    def backend_uninstaller(self, docker_compose_yaml, client, ver_os_info):
        containers = client.containers.list()
        backend_checker = s.backends_checking()
        os_checker = platform.release()

        list_of_supported_backends = backend_checker.check_json()
        
        s.clear_window(ver_os_info)
        
        s.log(f"{str(list_of_supported_backends).lower()}")
        s.log("Please pick from this list of supported AI backends to remove from the subsystem.")
        s.log(f"Type ``all`` to remove all supported backends")
        s.log(f"Type ``back`` to go back to the main menu")

        picked_backends = str(input("Request Backends: ")).lower()
        requested_backends = []

        if picked_backends == "back":
            return

        if picked_backends == "all":
            picked_backends = str(list_of_supported_backends)
        
        for item in list_of_supported_backends:
            if item in picked_backends:
                requested_backends.append(item)

        for container in containers:
            s.log(f"Checking Name: {container.name}, ID: {container.id}")
            if "midori_ai_subsystem" in container.name:
                s.log(f"Found the subsystem, logging into: {container.name} / {container.id}")
                container = client.containers.get(container.name)
                break
    
        docker_commands = [
            f"echo removing backends",
                ]
        
        for item in requested_backends:
            s.log(f"Uninstalling {item}")
            backend_checker.remove_backend(item)
            if "Unraid" in os_checker:
                docker_commands.append(f"docker compose -f /app/files/{item}/docker-compose.yaml down --rmi all")
            else:
                docker_commands.append(f"docker compose -f ./files/{item}/docker-compose.yaml down --rmi all")
            docker_commands.append(f"rm -rf ./files/{item}")

        s.log("Running commands inside of the Midori AI Subsystem!")
        for item_docker in docker_commands:
            s.log(f"Running {item_docker}")
            void, stream = container.exec_run(item_docker, stream=True)
            for data in stream:
                s.log(data.decode())

        input("Please press enter to go back to the main menu: ")

    def backend_updater(self, docker_compose_yaml, client, ver_os_info):
        backend_checker = s.backends_checking()
        os_checker = platform.release()

        list_of_supported_backends = backend_checker.check_json()
        
        s.clear_window(ver_os_info)
        
        s.log(f"{str(list_of_supported_backends).lower()}")
        s.log("Updating all Backends that are installed in the subsystem")

        picked_backends = str("all").lower()
        requested_backends = []

        if picked_backends == "all":
            picked_backends = str(list_of_supported_backends)
        
        for item in list_of_supported_backends:
            if item in picked_backends:
                requested_backends.append(item)
    
        docker_commands = [
            f"echo updating backends",
                ]
        
        for item in requested_backends:
            s.log(f"Updating {item}")
            if "Unraid" in os_checker:
                docker_commands.append(f"docker compose -f /app/files/{item}/docker-compose.yaml up --pull always -d")
            else:
                docker_commands.append(f"docker compose -f ./files/{item}/docker-compose.yaml up --pull always -d")

        s.log("Running commands on the Host OS!")
        for item_docker in docker_commands:
            s.log(f"Running {item_docker}")
            os.system(item_docker)