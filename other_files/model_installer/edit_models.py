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
                exit(0)
            
            s.clear_window(ver_os_info)

            question = "What setting would you like to edit?: "
            valid_answers = ["gpu_layers", "f16", "threads", "low_vram", "mmap", "mmlock", "name", "cuda", "numa", "no_mulmatq"]

            if use_gui == "yes":
                layout = [[sg.Text(f"Available settings: {str(valid_answers)}", size=(10000, 1))],
                        [sg.Text(f"{question}", size=(100, 1))],
                        [sg.Input(key='-QUERY-'),
                        sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                        ]
    
            context_temp = f"The user was asked what setting of the {answeryamleditor} llm model they have installed. Here is a full list of thing they can edit"
            context_temp = f"{context_temp}\ngpu_layers = How much GPU the model can use, recommended starting at 5 then adding more if there is free vram"
            context_temp = f"{context_temp}\nthreads = CPU cores for the model, recommended to keep this to under 50% their real core count"
            context_temp = f"{context_temp}\nname = the name that the model goes by when being requested by OpenAI V1"
                
            answeryamleditor_two = s.check_str(question, valid_answers, use_gui, layout, sg, context_temp, client_openai)
            
            s.clear_window(ver_os_info)

            questionbasic = f"What would you like to set ``{answeryamleditor_two}`` to (NO TYPECHECKING use at your own risk)?: "
            answeryamleditor_three = str(input(questionbasic))
            
            s.clear_window(ver_os_info)

            inside_model_folder = models_folder_container
            yaml_path_temp = inside_model_folder + f"/{answeryamleditor}.yaml"

            docker_commands = [
                ["rm", "-f", "yaml_edit.py"],
                ["pip", "install", "pyyaml"],
                ["wget", "-O", "yaml_edit.py", "https://tea-cup.midori-ai.xyz/download/yaml_edit.py"],
                ["python3", "yaml_edit.py", "-i", answeryamleditor_two, "-d", f"{answeryamleditor_three.lower()}", yaml_path_temp],
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