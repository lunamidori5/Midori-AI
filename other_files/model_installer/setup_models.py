import os
import json
import yaml
import requests

import support as s

def models_install(compose_path, ver_os_info, containers, client, use_gui, sg, about_model_size, about_model_q_size):
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

    s.log("Alright, now that I am s.logged into the docker, lets get you started with installing the model...")
    s.log("For more info on the models used, or links to the models, go to ``https://io.midori-ai.xyz/howtos/easy-model-installer/``")
    s.log(f"I am going to save our chat here and every thing I do to a file called ``{s.log_file_name}``, check it out if you like <3")
    s.log("Here are a few questions to find out what model you would like to try")

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

    if use_gui == "yes":
        layout = [[sg.Text(f"{questionbasic}", size=(100, 1))],
                [sg.Input(key='-QUERY-'),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
        
    answerbasic = s.check_str(questionbasic, sd_valid_answers, use_gui, layout, sg)

    if answerbasic.lower() == "no":
        answerbasic = "False"
            
    if answerbasic.lower() == "yes":
        answerbasic = "True"

    answerbasic = answerbasic.lower()

    s.clear_window(ver_os_info)

    if answerbasic:
        question4 = "What would you like to name the models file?: \n"

        if use_gui == "yes":
            layout = [[sg.Text(f"{question4}", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
            
            window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=True)

            while True:     # The Event Loop
                event, values = window.read()
                if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                    break
                if event == 'SEND':
                    answer4 = str(values['-QUERY-'].rstrip())
                    break

            window.close()
        else:
            answer4 = input(question4)
        
        answer4 = str(answer4.lower())

        s.clear_window(ver_os_info)

        s.log(about_model_size)
        valid_answers2 = ["7b", "2x7b", "8x7b", "70b", "id"]
        question2 = f"What size of known and supported model would you like to setup ({', '.join(valid_answers2)}): "

        if use_gui == "yes":
            layout = [[sg.Text(f"{about_model_size}", size=(100, 1))],
                    [sg.Text(f"{question2}", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                    ]
            
        answer2 = s.check_str(question2, valid_answers2, use_gui, layout, sg)
        answer2 = str(answer2.lower())

        valid_answers1 = ["q3", "q4", "q5", "q6", "q8"] 
        added_valid_answers1 = ["q4-k-m", "q5-k-m"]
        added_valid_answers2 = ["none"]

        if answer2.lower() == "8x7b":
            valid_answers1.extend(added_valid_answers1)
        
        if answer2.lower() != "id":
            valid_answers1.extend(added_valid_answers2)

        if answer2.lower() == "id":
            s.clear_window(ver_os_info)
            valid_answers2 = s.check_model_ids_file()
            question2 = f"What is the id of the model you would like to install? ({', '.join(valid_answers2)}): "

            if use_gui == "yes":
                layout = [[sg.Text(f"{question2}", size=(100, 1))],
                        [sg.Input(key='-QUERY-'),
                        sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                        ]
                
            answer2 = s.check_str(question2, valid_answers2, use_gui, layout, sg)
            answer2 = str(answer2.lower())

        s.clear_window(ver_os_info)

        s.log(about_model_q_size)

        question = f"What type of quantised model would you like to setup? ({', '.join(valid_answers1)}): "

        if use_gui == "yes":
            layout = [[sg.Text(f"{about_model_q_size}", size=(100, 1))],
                    [sg.Text(f"{question}", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                    ]
            
        answer1 = s.check_str(question, valid_answers1, use_gui, layout, sg)

        if answer1.lower() == "none":
            answer1 = str(answer1.lower())
        else:
            answer1 = str(answer1.upper())

        # Check if the word "model" is in the answer
        if "model" in answer4:
            # Remove the word "model"  from the answer
            answer4 = answer4.replace("model", "")

            # Print a message to the user
            s.log("\nThe word 'model' has been removed from the file name.")

        # Check if GPU is turned on
        if "cuda11" in service_image or "cuda12" in service_image:
            s.clear_window(ver_os_info)
            # Ask the user the third question
            if not answer1 == "none":
                question = "\nNumber of GPU layers to give the model?  (0 to 2000): \n"
                
                if use_gui == "yes":
                    layout = [[sg.Text(f"{question}", size=(100, 1))],
                            [sg.Input(key='-QUERY-'),
                            sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                        ]
                    
                    window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=True)

                    while True:     # The Event Loop
                        event, values = window.read()
                        if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                            break
                        if event == 'SEND':
                            answer3 = str(values['-QUERY-'].rstrip())
                            break

                    window.close()
                else:
                    answer3 = input(question)

                answer3 = int(answer3)
                use_gpu = True
        else:
            answer3 = 0
            answer3 = int(answer3)
            use_gpu = False

        s.clear_window(ver_os_info)

        if not answer1 == "none":
            question = "\nNumber of CPU Cores to give the model?  (0 to 2000): \n"
                
            if use_gui == "yes":
                layout = [[sg.Text(f"{question}", size=(100, 1))],
                        [sg.Input(key='-QUERY-'),
                        sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                    ]
                
                window = sg.Window('LocalAI Manager', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2), use_default_focus=True)

                while True:     # The Event Loop
                    event, values = window.read()
                    if event in (sg.WIN_CLOSED, 'EXIT'):            # quit if exit button or X
                        break
                    if event == 'SEND':
                        answer3 = str(values['-QUERY-'].rstrip())
                        break

                window.close()
            else:
                answercpu = input(question)

            answercpu = int(answercpu)

        s.clear_window(ver_os_info)

    if "ffmpeg" in service_image:
        question = "Would you like me to install a few Text to Speech models?: "
        sd_valid_answers = ["yes", "no", "true", "false"]

        if use_gui == "yes":
            layout = [[sg.Text(f"{question}", size=(100, 1))],
                        [sg.Input(key='-QUERY-'),
                        sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                    ]
    
        answertts = s.check_str(question, sd_valid_answers, use_gui, layout, sg)

        if answertts.lower() == "no":
            answertts = "False"
            
        if answertts.lower() == "yes":
            answertts = "True"

        answertts = answertts.lower()
        use_tts = answertts

        s.clear_window(ver_os_info)

    question = "Would you like me to install the embedding model?: "
    sd_valid_answers = ["yes", "no", "true", "false"]

    if use_gui == "yes":
        layout = [[sg.Text(f"{question}", size=(100, 1))],
                    [sg.Input(key='-QUERY-'),
                    sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                ]
        
    answerenbed = s.check_str(question, sd_valid_answers, use_gui, layout, sg)

    if answerenbed.lower() == "no":
        answerenbed = "False"
            
    if answerenbed.lower() == "yes":
        answerenbed = "True"

    answerenbed = answerenbed.lower()
    use_enbed = answerenbed

    s.clear_window(ver_os_info)

    if "core" in service_image:
        s.log("Looks like you are running a Core Image, Skipping: Stable diffusion, Llava, Huggingface Models")
    else:
        if "cuda11" in service_image or "cuda12" in service_image:
            question = "Would you like me to install a Stable diffusion model?: "
            sd_valid_answers = ["yes", "no", "true", "false"]

            if use_gui == "yes":
                layout = [[sg.Text(f"{question}", size=(100, 1))],
                            [sg.Input(key='-QUERY-'),
                            sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                        ]

            answersd = s.check_str(question, sd_valid_answers, use_gui, layout, sg)

            if answersd.lower() == "no":
                answersd = "False"
            
            if answersd.lower() == "yes":
                answersd = "True"

            answersd = answersd.lower()
            use_sd = answersd

            s.clear_window(ver_os_info)
            
            question = "Would you like me to install the Llava model?: "
            sd_valid_answers = ["yes", "no", "true", "false"]

            if use_gui == "yes":
                layout = [[sg.Text(f"{question}", size=(100, 1))],
                            [sg.Input(key='-QUERY-'),
                            sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                        ]

            answerllava = s.check_str(question, sd_valid_answers, use_gui, layout, sg)

            if answerllava.lower() == "no":
                answerllava = "False"
            
            if answerllava.lower() == "yes":
                answerllava = "True"

            answerllava = answerllava.lower()
            use_llava = answerllava

            s.clear_window(ver_os_info)
        else:
            s.log("Looks like you are running on CPU only, Skipping: Stable diffusion, Llava, Huggingface Models")
        
        question = "Would you like to use our slower but encrypted endpoint for LocalAI to serve and setup the model's files (Not the models file itself)?: "
        sd_valid_answers = ["yes", "no", "true", "false"]

        if use_gui == "yes":
            layout = [[sg.Text(f"{question}", size=(100, 1))],
                        [sg.Input(key='-QUERY-'),
                        sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),]
                    ]

        answerencrypted = s.check_str(question, sd_valid_answers, use_gui, layout, sg)

        if answerencrypted.lower() == "no":
            answerencrypted = "False"
        
        if answerencrypted.lower() == "yes":
            answerencrypted = "True"

        answerencrypted = answerencrypted.lower()

        s.clear_window(ver_os_info)

    s.log(f"I am now going to install everything you requested, please wait for me to get done. As ill be running commands inside of your docker image.")
    s.log("Hit enter to start")

    input()

    s.clear_window(ver_os_info)

    if answer1 == "none":
        if answer2 == "7b":
            answer4_name = "cognitivecomputations"
            answer4_name_b = "dolphin-2.6-mistral-7b"
        if answer2 == "8x7b":
            answer4_name = "cognitivecomputations"
            answer4_name_b = "dolphin-2.7-mixtral-8x7b"
        if answer2 == "70b":
            answer4_name = "cognitivecomputations"
            answer4_name_b = "dolphin-2.2-70b"

    if answerbasic == "true":
        s.log(f"The type of model you want to setup is: {answer1}")
        s.log(f"The size of the known model you want to setup is: {answer2}")
        s.log(f"The amount of GPU layers you want to give it is: {answer3}")
        s.log(f"You named the model: {answer4}")

        if answer2 == "8x7b":
            answer2 = "43b"

        if answer2 == "2x7b":
            answer2 = "14b"

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
            ["echo", f"This next step will take 10+ mins, please do not exit or close this program"],
            ["wget", "-O", f"{answer4}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"{answer4}.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer4}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/threads.*/threads: {answercpu}/g", f"{yaml_path_temp}"],
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
            ["echo", f"This next step will take 10+ mins, please do not exit or close this program"],
            ["wget", "-O", f"{answer4}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"{answer4}.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer4}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/threads.*/threads: {answercpu}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/gpu_layers.*/gpu_layers: {answer3}/g", f"{yaml_path_temp}"],
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
            ["rm", "-f", "helper_app.py"],
            ["wget", "-O", "helper_app.py", "https://tea-cup.midori-ai.xyz/download/helper_app.py"],
            ["python3", "helper_app.py", "localai-chat.tmpl"],
            ["python3", "helper_app.py", "localai-chatmsg.tmpl"],
            ["python3", "helper_app.py", "models.yaml"],
            ["echo", f"This next step will take 10+ mins, please do not exit or close this program"],
            ["wget", "-O", f"{answer2}model{answer1}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"models.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer2}model{answer1}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/threads.*/threads: {answercpu}/g", f"{yaml_path_temp}"],\
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
            ["rm", "-f", "helper_app.py"],
            ["wget", "-O", "helper_app.py", "https://tea-cup.midori-ai.xyz/download/helper_app.py"],
            ["python3", "helper_app.py", "localai-chat.tmpl"],
            ["python3", "helper_app.py", "localai-chatmsg.tmpl"],
            ["python3", "helper_app.py", "models-gpu.yaml"],
            ["echo", f"This next step will take 10+ mins, please do not exit or close this program"],
            ["wget", "-O", f"{answer2}model{answer1}.gguf", f"https://tea-cup.midori-ai.xyz/download/{answer2}model{answer1}.gguf"],
            ["cp", f"localai-chat.tmpl", f"{temp_chat_path}"],
            ["cp", f"localai-chatmsg.tmpl", f"{temp_chatmsg_path}"],
            ["cp", f"models-gpu.yaml", f"{yaml_path_temp}"],
            ["cp", f"{answer2}model{answer1}.gguf", f"{model_path_temp}"],
            ["sed", "-i", f"s/name.*/name: {answer4}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/threads.*/threads: {answercpu}/g", f"{yaml_path_temp}"],
            ["sed", "-i", f"s/gpu_layers.*/gpu_layers: {answer3}/g", f"{yaml_path_temp}"],
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
            ["echo", f"This next step will take 5+ mins, please do not exit or close this program"],
            ["wget", "-O", inside_model_folder + f"/ggml-model-q4_k.gguf", f"https://huggingface.co/mys/ggml_bakllava-1/resolve/main/ggml-model-q4_k.gguf"],
            ["wget", "-O", inside_model_folder + f"/mmproj-model-f16.gguf", f"https://huggingface.co/mys/ggml_bakllava-1/resolve/main/mmproj-model-f16.gguf"],
            ["wget", "-O", inside_model_folder + f"/chat-simple.tmpl", f"https://github.com/mudler/LocalAI/blob/b8240b4c1839089b9d06a3e2b1c629a294cff87e/examples/configurations/llava/chat-simple.tmpl"],
            ["wget", "-O", inside_model_folder + f"/llava.yaml", f"https://github.com/mudler/LocalAI/blob/b8240b4c1839089b9d06a3e2b1c629a294cff87e/examples/configurations/llava/llava.yaml"],
        ]
        docker_commands.extend(llava_commands)

    # Run a command inside the container
    s.log("Downloading and setting up model into the docker")
    for command in docker_commands:
        s.log(f"Running {command}: ")
        command_output = container.exec_run(command)
        s.log(command_output.output.decode("utf-8"))

    s.log("All done, I am now rebooting LocalAI")
    container.restart()
    s.log("Thank you! Please enjoy your new models!")

def models_uninstall(compose_path, ver_os_info, containers, client, use_gui, sg):
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
                    s.log("Localhost is not a IP address... Please try again...")
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

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    response = requests.get(f"http://{ip_address}:{models_ports}/models", headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        models = response_data["data"]

        # Extract model IDs
        model_ids = [model["id"] for model in models]

        # Print model IDs or perform other operations as needed
        s.clear_window(ver_os_info)

        s.log(f"Available model IDs: {model_ids}")

        questionbasic = "What model would you like to uninstall?: "
        valid_answers = model_ids
        answeruninstallmodel = s.check_str(questionbasic, valid_answers)

        # If the answeruninstallmodel  contains ".yaml" or ".gguf", strip it
        if ".yaml" in answeruninstallmodel or ".gguf" in answeruninstallmodel:
            answeruninstallmodel = answeruninstallmodel.replace(".yaml", "").replace(".gguf", "")

        inside_model_folder = models_folder_container

        docker_commands = [
            ["rm", "-f", f"{inside_model_folder}/{answeruninstallmodel}.gguf"],
            ["rm", "-f", f"{inside_model_folder}/{answeruninstallmodel}.yaml"],
        ]

        # Run a command inside the container
        s.log("Uninstalling model from the docker")
        for command in docker_commands:
            s.log(f"Running {command}: ")
            command_output = container.exec_run(command)
            s.log(command_output.output.decode("utf-8"))

        s.log("All done, I am now rebooting LocalAI")
        container.restart()
        s.log("Thank you! Models unintalled!")

    else:
        s.log("Request failed with status code:", response.status_code)
        s.log("Response text:", response.text)