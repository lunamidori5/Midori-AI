import os

files_to_download = {
    "requirements.txt": "https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/requirements.txt",
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

# Purge the downloaded files
print("Purging the downloaded files ...")
os.system('pip cache purge')

for file_name in files_to_download:
    os.remove(file_name)