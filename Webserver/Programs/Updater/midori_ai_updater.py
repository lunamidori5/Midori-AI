import os
import sys
import shutil
import requests
import subprocess

from halo import Halo

spinner = Halo(text='Loading', spinner='dots', color='green')

jobs = []

try:
    if os.geteuid() == 0:
        print("We are running as root, updating programs")
    else:
        raise PermissionError("This program needs root to update programs, please run with root...")
except Exception as error:
    print(f"{str(error)}")
    sys.exit(15)

supported_flavors = ["pixelarch", "endeavouros", "arch linux"]
non_standard_supported_flavors = ["pixelgen", "gentoo"]

pixelarch_program_to_update = [
    ["midori_ai_login", "pixelarch-midori-ai-login"],
    ["midori_ai_hf_downloader", "pixelarch-hf-downloader"],
    ["midori_ai_downloader", "pixelarch-midori-ai-downloader"],
    ["midori_ai_file_manager", "pixelarch-midori-ai-file-manager"],
    ["midori_ai_uploader", "pixelarch-midori-ai-uploader"],
    ["midori_ai_updater", "pixelarch-midori-ai-updater"]
    ]

standard_program_to_update = [
    ["midori_ai_login", "standard-linux-midori-ai-login"],
    ["midori_ai_hf_downloader", "standard-linux-hf-downloader"],
    ["midori_ai_downloader", "standard-linux-midori-ai-downloader"],
    ["midori_ai_file_manager", "standard-linux-midori-ai-file-manager"],
    ["midori_ai_uploader", "standard-linux-midori-ai-uploader"],
    ["midori_ai_updater", "standard-linux-midori-ai-updater"]
    ]

cluster_check = [
    ["midori_ai_login", "midori-ai-login"],
    ["midori_ai_hf_downloader", "midori-ai-hf-downloader"],
    ["midori_ai_downloader", "midori-ai-downloader"],
    ["midori_ai_file_manager", "midori-ai-file-manager"],
    ["midori_ai_uploader", "midori-ai-uploader"],
    ["midori_ai_updater", "midori-ai-updater"]
    ]

with open("/etc/os-release", "r") as f:
    os_release_data = f.read()
    
for flavor in supported_flavors:
    if flavor in os_release_data.lower():
        program_to_update = pixelarch_program_to_update
        break
else:
    program_to_update = standard_program_to_update

# Create a temporary directory
home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
os.makedirs(folder_path, exist_ok=True)
temp_folder_path = os.path.join(folder_path, "tmp")
os.makedirs(temp_folder_path, exist_ok=True)
os.chdir(temp_folder_path)

# Download new programs
for program in program_to_update:
    spinner.start(text=f"Downloading program: {program[0]}")
    response = requests.get("https://tea-cup.midori-ai.xyz/download/" + program[1], stream=True, timeout=55)
    if response.status_code == 200:
        with open(program[1], 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            del response
    else:
        spinner.fail(text=f"Error downloading {program[0]}: HTTP status code {response.status_code}")
        sys.exit(10)

# Remove existing programs
for program in program_to_update:
    if "midori_ai_updater" in program[0]:
        continue
    path = "/usr/local/bin/" + program[0]
    if os.path.isfile(path):
        spinner.start(text=f"Removing existing program: {program[0]}")
        os.remove(path)

# install new programs
for program in program_to_update:

    os.chmod(program[1], 0o755)
    spinner.start(text=f"Installing program: {program[0]}")
    
    shutil.move(program[1], "/usr/local/bin/" + program[0])
    
    # Check if the file was moved successfully
    if os.path.isfile("/usr/local/bin/" + program[0]):
        spinner.succeed(text=f"Program {program[0]} installed successfully.")
    else:
        spinner.fail(text=f"Error: Program {program[0]} was not installed successfully.")
    del program

for program in cluster_check:
    if os.path.isfile("/usr/local/bin/" + program[1]):
        shutil.copy("/usr/local/bin/" + program[0], "/usr/local/bin/" + program[1])

# Clean up
os.chdir("..")
os.rmdir(temp_folder_path)