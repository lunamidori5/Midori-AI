class Config:
    def __init__(self):
        self.supported_programs = []
        self.installed_programs = {}
        self.installed_models =  {}

    def add_supported_program (self, program_name):
        self.supported_programs.append(program_name)

    def add_installed_program(self, program_name, installed_time, update):
        self.installed_programs[program_name] =  {
            "installed_time": installed_time,
            "update": update
        }

    def add_installed_model(self, model_name, installed_time, update):
        self.installed_models[model_name] = {
            "installed_time": installed_time,
            "update": update
        }

    def save(self, file):
        import json
        with open(file, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    def load(self, file):
        import json
        with open(file, "r") as f:
            data = json.load(f)
            self.__dict__.update(data)

def download_and_load_config(config_file, server_url):
    import requests
    import json
    
    # Download the config file from the server
    response = requests.get(server_url)
    
    # Load the config file
    config = Config()
    config.load(config_file)
    
    # Check for updates to supported programs
    supported_programs = response.json()["supported_programs"]
    for program_name in supported_programs:
        if program_name not in config.supported_programs:
            config.add_supported_program(program_name)
    
    # Check for updates to installed models
    installed_models = response.json()["installed_models"]
    for model_name, model_data in installed_models.items():
        if model_name not in config.installed_models:
            config.add_installed_model(model_name, model_data["installed_time"], model_data["update"])
        elif config.installed_models[model_name]["update"] != model_data["update"]:
            config.add_installed_model(model_name, model_data["installed_time"], model_data["update"])
    
    # Save the updated config file
    config.save(config_file)
