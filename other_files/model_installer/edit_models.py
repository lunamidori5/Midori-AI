import os
import json
import yaml
import requests

import support as s

def edit(compose_path, ver_os_info, containers, client, use_gui, sg, layout, client_openai):
    # Try to load the Docker Compose file
    s.log("Docker Server error, trying to check your docker-compose.yaml file...")
    docker_compose_found = False
    try:
        s.log("Loading your docker-compose.yaml")
        with open(compose_path, "r") as f:
            compose_data  = yaml.safe_load(f)
            s.log("Auto loaded the docker-compose.yaml")
            docker_compose_found = True
    except FileNotFoundError:
        # If the file is not found, ask the user where it is
        s.log("If your docker compose yaml file is named something else, please point me to the file using absolute path")
        s.log("If you used docker run or just want to try to run this in ``fallback mode`` type ``fallback``")
        compose_path = input("Could not find docker-compose.yaml in the current directory. Where is it located?: ")
        try:
            with open(os.path.join(compose_path), "r") as f:
                compose_data = yaml.safe_load(f)
            s.log("Loaded the docker-compose.yaml from users path")
            docker_compose_found = True
        except FileNotFoundError:
            # If the file is still not found, raise an error
            s.log("Could not find docker-compose.yaml at the specified location. Entering ``fallback mode``")


    # Extract service name and model folder path
    if docker_compose_found:
        for service_name, service_data in compose_data["services"].items():
            s.log(f"Checking... Service Name: {service_name}, Service Data: {service_data}")
            if service_data["image"].startswith("quay.io/go-skynet/local-ai"):
                models_volume = service_data["volumes"][0]
                models_folder_host = models_volume.split(":")[0]  # Assuming host path is first
                models_folder_container = models_volume.split(":")[1]  # Assuming container path is second
                models_ports = service_data["ports"][0]
                model_port_api = models_ports.split(":")[1]
                service_image = service_data["image"]

                s.log(f"The inside model folder of the docker is {models_folder_container}, This is were ill place all the files inside of the docker.")
                break

        # If no matching service is found, raise an error
        if service_name not in compose_data["services"]:
            raise Exception("Could not find a service with the image 'quay.io/go-skynet/local-ai' in your docker-compose.yaml file.")
    else:
        s.clear_window(ver_os_info)
        s.log("Running ``docker ps``")

        os.system('docker ps -a --format \"table {{.ID}}\t{{.Names}}\"')

        service_name = input("What is LocalAI called in ``docker ps`` (Please type the name like this ``localai-api-1`` or ``localai``): ")

        s.clear_window(ver_os_info)

        s.log("This folder will never be from the host OS side, please check your docker compose file or env file for the path")
        models_folder_container = input("Where is LocalAI's docker models folder located? (IE: ``/models`` or ``/build/models``): ")

        s.clear_window(ver_os_info)

        os.system('docker ps -a --format \"table {{.Names}}\t{{.Image}}\"')

        service_image = input("What is the full image name that you used? (Please paste the full link. IE: quay.io/go-skynet/local-ai:master-cublas-cuda12-ffmpeg): ")

        s.clear_window(ver_os_info)

        os.system('docker ps -a --format \"table {{.Names}}\t{{.Ports}}\"')
        models_ports = input("What port are you running LocalAI on?: ")

    s.clear_window(ver_os_info)

    for container in containers:
        s.log(f"Checking Name: {container.name}, ID: {container.id}")

        # Check if there is a container with a name containing `service_name`
        if service_name in container.name:
            # Get the container object
            s.log(f"Found LocalAI, s.logging into: {container.name} / {container.id}")
            container = client.containers.get(container.name)
            break

    if container is None:
        s.log(f"Error: Could not find LocalAI container with name {service_name}")
        s.log("Checking images again with known names")
        for container in containers:
            s.log(f"Checking Name: {container.name}, ID: {container.id}")

            # Check if there is a container with a name containing `service_name`
            if service_name in container.name:
                # Get the container object
                s.log(f"Found LocalAI, s.logging into: {container.name} / {container.id}")
                container = client.containers.get(container.name)
                break
        
    s.clear_window(ver_os_info)

    if use_gui == "yes":
        layout = [[sg.Text(f"If you have a API Key, please put it here. Else hit enter:", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
        
        window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=True)

        while True:     # The Event Loop
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                break
            if event == 'SEND':
                bearer_token = str(values['-QUERY-'].rstrip())
                break

        window.close()

        layout = [[sg.Text(f"What is the LocalAI's IP? (192.168.x.x)", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
        
        window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=True)

        while True:     # The Event Loop
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                break
            if event == 'SEND':
                ip_address = str(values['-QUERY-'].rstrip())

                if "localhost" in ip_address:
                    s.log("Localhost is not a valid IP address... Please try again...")
                else:
                    break

        window.close()

        layout = [[sg.Text(f"What is the LocalAI's Port? (8080): ", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
        
        window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=True)

        while True:     # The Event Loop
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                break
            if event == 'SEND':
                models_ports = str(values['-QUERY-'].rstrip())
                break

        window.close()
    else:
        bearer_token = str(input("If you have a API Key, please put it here. Else type no: "))

        while True:
            try:
                ip_address = str(input("What is the LocalAI's IP? (192.168.x.x): "))
                if "localhost" in ip_address:
                    raise ValueError("Localhost is not a valid IP address.")
                break
            except ValueError as e:
                s.log(f"Error: {e}. Please try again.")

        models_ports = str(input(f"What is the LocalAI's Port? (8080): "))

    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(f"http://{ip_address}:{models_ports}/models", headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        models = response_data["data"]

        # Extract model IDs
        model_ids = [model["id"] for model in models]

        filtered_model_ids = model_ids

        s.log(filtered_model_ids)

        filtered_model_ids.append("exit")
        
        s.clear_window(ver_os_info)

        while True:
            s.log(f"Available model IDs: {filtered_model_ids}")
            s.log("Type ``exit`` to exit")

            question = "What model would you like to edit?: "
            valid_answers = filtered_model_ids

            if use_gui == "yes":
                layout = [[sg.Text(f"Please see the other window for the models list!", size=(100, 1))],
                        [sg.Text("Type ``exit`` to exit", size=(100, 1))],
                        [sg.Text(f"{question}", size=(100, 1))],
                        [sg.Input(key='-QUERY-'),
                        sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                        ]
    
            context_temp = f"The user was asked what model they would like to edit. Please tell them to pick from the list.\n{str(valid_answers)}"
                
            answeryamleditor = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)

            if ".yaml" in answeryamleditor or ".gguf" in answeryamleditor:
                answeryamleditor = answeryamleditor.replace(".yaml", "").replace(".gguf", "")

            if answeryamleditor == "exit":
                s.log("exiting...")
                return
            
            s.clear_window(ver_os_info)

            valid_answers = ["gpu_layers", "f16", "threads", "low_vram", "mmap", "mmlock", "name", "cuda", "numa", "no_mulmatq"]
            question = f"{str(valid_answers)}\nWhat setting would you like to edit?: "

            context_temp = f"The user was asked what setting of the {answeryamleditor} llm model they have installed would they like to edit. Here is a full list of thing they can edit"
            context_temp = f"{context_temp}\ngpu_layers = How much GPU the model can use, recommended starting at 5 then adding more if there is free vram"
            context_temp = f"{context_temp}\nthreads = CPU cores for the model, recommended to keep this to under 50% their real core count"
            context_temp = f"{context_temp}\nname = the name that the model goes by when being requested by OpenAI V1"
            context_temp = f"{context_temp}\ncuda = For the model to use the GPU or Not, is a bool"
            context_temp = f"{context_temp}\nlow_vram = Sets the model into low vram use mode, recommended for lower end computers, is a bool"
            context_temp = f"{context_temp}\nmmap = mmap is a system call that maps the model into memory, allowing direct access to the models files, is a bool"
            context_temp = f"{context_temp}\nmmlock = mmlock is a Linux kernel feature that allows users to lock pages in memory, keeping the model in memory, is a bool"
            context_temp = f"{context_temp}\nno_mulmatq = The ``no_mulmtq`` parameter controls whether or not XLA's MatMul will be used. Setting this to True may save memory, but may reduce performance and/or numerical precision. Is a bool"
            context_temp = f"{context_temp}\nnuma = NUMA (Non-Uniform Memory Access) optimizes memory access in systems with multiple memory controllers, improving performance by ensuring processes access data from the closest memory node, is a bool"
                
            answeryamleditor_two = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)
            
            s.clear_window(ver_os_info)

            questionbasic = f"What would you like to set ``{answeryamleditor_two}`` to (NO TYPECHECKING use at your own risk)?: "
            answeryamleditor_three = str(input(questionbasic))
            
            s.clear_window(ver_os_info)

            inside_model_folder = models_folder_container
            yaml_path_temp = inside_model_folder + f"/{answeryamleditor}.yaml"

            docker_commands = [
                ["rm", "-f", "yaml_edit.py"],
                ["apt-get", "-y", "install", "wget"],
                ["wget", "-O", "yaml_edit", "https://tea-cup.midori-ai.xyz/download/yaml_edit"],
                ["chmod", "+x", "yaml_edit"],
                ["./yaml_edit", "-i", answeryamleditor_two, "-d", f"{answeryamleditor_three.lower()}", yaml_path_temp],
            ]

            # Run a command inside the container
            s.log("editing model from inside the docker")
            for command in docker_commands:
                s.log(f"Running {command}: ")
                command_output = container.exec_run(command)
                s.log(command_output.output.decode("utf-8", errors="ignore"))

            s.log("All done, I am now rebooting LocalAI")
            container.restart()
            s.log("Thank you! Models edited!")

class subsystem_backend_manager:
    def backend_installer(self, docker_compose_yaml, client, client_openai, ver_os_info, discord_id):
        containers = client.containers.list()
        backend_checker = s.backends_checking()

        list_of_supported_backends = [
            "localai", 
            "anythingllm", 
            "ollama",
            "invokeai",
            "oobabooga",
            "home-assistant",
            "midoricluster"
            ]
        
        s.clear_window(ver_os_info)
        
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
        
        str_temp = f"``{list_of_supported_backends[0]} and {list_of_supported_backends[1]}`` or ``{list_of_supported_backends[1]}, {list_of_supported_backends[0]}, {list_of_supported_backends[5]}``"
        s.log(f"{str(list_of_supported_backends).lower()}")
        s.log("Please pick from this list of supported AI backends to add to the subsystem.")
        s.log(f"You can list them out like this. {str_temp}")
        s.log(f"Or type ``all`` to install all supported backends")

        picked_backends = str(input("Request Backends: ")).lower()
        requested_backends = []

        if picked_backends == "all":
            picked_backends = str(list_of_supported_backends)
        
        if "oobabooga" in picked_backends:
            picked_backends = picked_backends + " oobaboogaapi"
        
        for item in list_of_supported_backends:
            if item in picked_backends:
                requested_backends.append(item)

        s.log("Loading your docker-compose.yaml")
        with open(docker_compose_yaml, "r") as f:
            compose_data  = yaml.safe_load(f)
            s.log("Auto loaded the docker-compose.yaml")
            s.log(str(compose_data))

        for service_name, service_data in compose_data["services"].items():
            s.log(f"Checking... Service Name: {service_name}, Service Data: {service_data}")
            if service_data["image"].startswith("lunamidori5"):
                for container in containers:
                    s.log(f"Checking Name: {container.name}, ID: {container.id}")
                    if service_name in container.name:
                        s.log(f"Found the subsystem, logging into: {container.name} / {container.id}")
                        container = client.containers.get(container.name)
                    break
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
        
        for backend_port in requested_backends:
            normal_port = s.get_port_number(backend_port)
            s.log(f"We are running {backend_port} on {normal_port}")

        input("Please press enter to go back to the main menu: ")

    def backend_uninstaller(self, docker_compose_yaml, client, ver_os_info):
        containers = client.containers.list()
        backend_checker = s.backends_checking()

        list_of_supported_backends = [
            "localai", 
            "anythingllm", 
            "ollama",
            "invokeai",
            "oobabooga",
            "home-assistant",
            "midoricluster"
            ]
        
        s.clear_window(ver_os_info)
        
        str_temp = f"``{list_of_supported_backends[0]} and {list_of_supported_backends[1]}`` or ``{list_of_supported_backends[1]}, {list_of_supported_backends[0]}, {list_of_supported_backends[5]}``"
        s.log(f"{str(list_of_supported_backends).lower()}")
        s.log("Please pick from this list of supported AI backends to remove from the subsystem.")
        s.log(f"You can list them out like this. {str_temp}")
        s.log(f"Or type ``all`` to remove all supported backends")

        picked_backends = str(input("Request Backends: ")).lower()
        requested_backends = []

        if picked_backends == "all":
            picked_backends = str(list_of_supported_backends)
        
        for item in list_of_supported_backends:
            if item in picked_backends:
                requested_backends.append(item)

        s.log("Loading your docker-compose.yaml")
        with open(docker_compose_yaml, "r") as f:
            compose_data  = yaml.safe_load(f)
            s.log("Auto loaded the docker-compose.yaml")
            s.log(str(compose_data))

        for service_name, service_data in compose_data["services"].items():
            s.log(f"Checking... Service Name: {service_name}, Service Data: {service_data}")
            if service_data["image"].startswith("lunamidori5"):
                for container in containers:
                    s.log(f"Checking Name: {container.name}, ID: {container.id}")
                    if service_name in container.name:
                        s.log(f"Found the subsystem, logging into: {container.name} / {container.id}")
                        container = client.containers.get(container.name)
                    break
                break
    
        docker_commands = [
            f"echo removing backends",
                ]
        
        for item in requested_backends:
            s.log(f"Uninstalling {item}")
            backend_checker.remove_backend(item)
            docker_commands.append(f"docker compose -f ./files/{item}/docker-compose.yaml down --rmi all")
            docker_commands.append(f"rm -rf ./files/{item}")

        s.log("Running commands inside of the Midori AI Subsystem!")
        for item_docker in docker_commands:
            s.log(f"Running {item_docker}")
            void, stream = container.exec_run(item_docker, stream=True)
            for data in stream:
                s.log(data.decode())

        input("Please press enter to go back to the main menu: ")