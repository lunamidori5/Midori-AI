import os

files_to_download = {
    "requirements.txt": "https://tea-cup.midori-ai.xyz/download/midori_program_requirments.txt",
    "helper_app.py": "https://tea-cup.midori-ai.xyz/download/helper_app.py",
}

files_to_download_enx = {
    "model_installer.py": "https://tea-cup.midori-ai.xyz/download/model_installer.py",
    "carly_help.py": "https://tea-cup.midori-ai.xyz/download/carly_help.py",
    "setup_docker.py": "https://tea-cup.midori-ai.xyz/download/setup_docker.py",
    "setup_models.py": "https://tea-cup.midori-ai.xyz/download/setup_models.py",
    "edit_models.py": "https://tea-cup.midori-ai.xyz/download/edit_models.py",
    "version.py": "https://tea-cup.midori-ai.xyz/download/version.py",
    "support.py": "https://tea-cup.midori-ai.xyz/download/support.py",
    "midori_program_ver.txt": "https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt",
}

if os.path.exists("running_subsystem_manager_other_os.py"):
    print("Removing outdated copy of python runner...")
    os.remove("running_subsystem_manager_other_os.py")

# Get this folder we are in
current_file_path = os.path.abspath(__file__)

# Rename the file
os.rename(current_file_path, "running_subsystem_manager_other_os.py")

# Download all the needed files
print("Downloading the needed files...")
for file_name, download_url in files_to_download.items():
    os.system(f"curl -s {download_url} > {file_name}")

# Make the python venv
# use "temp/bin/python" for python
# use "temp/bin/pip" for pip

os.system("python3 -m venv temp")

# Check if the virtual environment 'my_venv' is installed
if os.path.exists('temp/bin/python'):
    print('Virtual environment is installed')
else:
    print('Virtual environment is not installed')
    print('Please install the python3 venv package for your Distro')
    exit(404)

os.system('temp/bin/pip install -v -r requirements.txt')
os.system('temp/bin/pip cache purge')

if os.name == 'posix':
    print("Downloading the needed files...")
    for file_name, download_url in files_to_download_enx.items():
        os.system(f"temp/bin/python helper_app.py {file_name}")
else:
    for file_name, download_url in files_to_download_enx.items():
        os.system(f"curl -s {download_url} > {file_name}")

# Run the Python program
print("Running the Python program...")
os.system('temp/bin/python model_installer.py')

while True:
    yn = input("Purge the venv? (Y/n): ")
    if yn == "" or yn == "Y" or yn == "y":
        print("Purging the venv...")
        os.system("rm -rf temp")
        break
    elif yn == "N" or yn == "n":
        print("Not purging the venv...")
        print("It is super recommended to purge the venv every time you run the subsystem")
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")

# Purge the downloaded files
print("Purging the downloaded files...")

for file_name in files_to_download:
    os.remove(file_name)

for file_name in files_to_download_enx:
    os.remove(file_name)

if os.path.exists(current_file_path):
    print("Python runner updated by manager, update will happen on next run")
else:
    # Get this folder we are in
    current_file_path_post = os.path.abspath(__file__)

    # Rename the file
    os.rename(current_file_path_post, "subsystem_python_runner.py")
