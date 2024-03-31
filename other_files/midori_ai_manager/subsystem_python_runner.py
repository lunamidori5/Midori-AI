import os
import time

files_to_download = {
    "model_installer.py": "https://tea-cup.midori-ai.xyz/download/model_installer.py",
    "requirements.txt": "https://tea-cup.midori-ai.xyz/download/midori_program_requirments.txt",
    "carly_help.py": "https://tea-cup.midori-ai.xyz/download/carly_help.py",
    "setup_docker.py": "https://tea-cup.midori-ai.xyz/download/setup_docker.py",
    "setup_models.py": "https://tea-cup.midori-ai.xyz/download/setup_models.py",
    "edit_models.py": "https://tea-cup.midori-ai.xyz/download/edit_models.py",
    "support.py": "https://tea-cup.midori-ai.xyz/download/support.py",
}

# Download all the needed files
print("Downloading the needed files...")
for file_name, download_url in files_to_download.items():
    os.system(f"curl -s {download_url} > {file_name}")

time.sleep(1)

# Install pip requirements one item at a time
print("Installing pip requirements...")
with open('requirements.txt', 'r') as f:
    for line in f:
        os.system('pip install ' + line.strip())

# Run the Python program
print("Running the Python program...")
os.system('python3 model_installer.py')

# Purge the downloaded files
print("Purging the downloaded files ...")
os.system('pip cache purge')
for file_name in files_to_download:
    os.remove(file_name)