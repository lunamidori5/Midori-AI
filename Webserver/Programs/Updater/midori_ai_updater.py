import os
import shutil
import requests
import subprocess

from halo import Halo

spinner = Halo(text='Loading', spinner='dots', color='green')

jobs = []

if os.geteuid() == 0:
    print("We are running as root, updating programs")
else:
    raise PermissionError("This program needs root to update programs, please run with root...")

supported_flavors = ["pixelarch", "endeavouros", "arch linux"]
non_standard_supported_flavors = ["pixelgen", "gentoo"]

pixelarch_program_to_update = [
    ["midori-ai-login", "pixelarch-midori-ai-login"],
    ["midori-ai-hf-downloader", "pixelarch-hf-downloader"],
    ["midori-ai-downloader", "pixelarch-midori-ai-downloader"],
    ["midori-ai-file-manager", "pixelarch-midori-ai-file-manager"],
    ["midori-ai-uploader", "pixelarch-midori-ai-uploader"],
    ["midori-ai-updater", "pixelarch-midori-ai-updater"]
    ]

standard_program_to_update = [
    ["midori-ai-login", "standard-linux-midori-ai-login"],
    ["midori-ai-hf-downloader", "standard-linux-hf-downloader"],
    ["midori-ai-downloader", "standard-linux-midori-ai-downloader"],
    ["midori-ai-file-manager", "standard-linux-midori-ai-file-manager"],
    ["midori-ai-uploader", "standard-linux-midori-ai-uploader"],
    ["midori-ai-updater", "standard-linux-midori-ai-updater"]
    ]

non_standard_program_to_update = [
    ["midori-ai-login", "standard-linux-midori-ai-login"],
    ["midori-ai-hf-downloader", "standard-linux-hf-downloader"],
    ["midori-ai-downloader", "standard-linux-midori-ai-downloader"],
    ["midori-ai-file-manager", "standard-linux-midori-ai-file-manager"],
    ["midori-ai-uploader", "standard-linux-midori-ai-uploader"],
    ["midori-ai-updater", "standard-linux-midori-ai-updater"]
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

# Remove existing programs
for program in program_to_update:
    if "midori-ai-updater" in program[0]:
        continue
    path = "/usr/local/bin/" + program[0]
    if os.path.isfile(path):
        spinner.start(text=f"Removing existing program: {program[0]}")
        os.remove(path)

# Download and install new programs
for program in program_to_update:
    response = requests.get("https://tea-cup.midori-ai.xyz/download/" + program[1], stream=True, timeout=55)
    with open(program[1], 'wb') as out_file:
        spinner.start(text=f"Downloading program: {program[0]}")
        shutil.copyfileobj(response.raw, out_file)
        del response

    os.chmod(program[1], 0o755)
    spinner.start(text=f"Installing program: {program[0]}")
    
    shutil.move(program[1], "/usr/local/bin/" + program[0])
    
    # Check if the file was moved successfully
    if os.path.isfile("/usr/local/bin/" + program[0]):
        spinner.succeed(text=f"Program {program[0]} installed successfully.")
    else:
        spinner.fail(text=f"Error: Program {program[0]} was not installed successfully.")
    del program

# Clean up
os.chdir("..")
os.rmdir(temp_folder_path)