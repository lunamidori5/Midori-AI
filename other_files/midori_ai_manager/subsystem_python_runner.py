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
}

# Download all the needed files
print("Downloading the needed files...")
for file_name, download_url in files_to_download.items():
    os.system(f"curl -s {download_url} > {file_name}")

# Install pip requirements one item at a time
lines = []
with open('requirements.txt', 'r') as f:
    for line in f:
        lines.append(line.strip())

for line in lines:
    os.system('pip install --force-reinstall ' + line)
    os.system('pip cache purge')

if os.name == 'posix':
    print("Downloading the needed files...")
    for file_name, download_url in files_to_download_enx.items():
        os.system(f"python3 helper_app.py {file_name}")
else:
    for file_name, download_url in files_to_download_enx.items():
        os.system(f"curl -s {download_url} > {file_name}")

# Run the Python program
print("Running the Python program...")
os.system('python3 model_installer.py')

# Purge the downloaded files
print("Purging the downloaded files ...")

for file_name in files_to_download:
    os.remove(file_name)

for file_name in files_to_download_enx:
    os.remove(file_name)