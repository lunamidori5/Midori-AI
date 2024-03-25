import os
import time

# Download all the needed files
print("Downloading the needed files...")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/model_installer.py > model_installer.py")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/midori_program_requirments.txt > requirements.txt")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/carly_help.py > carly_help.py")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/setup_docker.py > setup_docker.py")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/setup_models.py > setup_models.py")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/edit_models.py > edit_models.py")
os.system("curl -s https://tea-cup.midori-ai.xyz/download/support.py > support.py")

time.sleep(5)

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
os.remove('model_installer.py')
os.remove('requirements.txt')
os.remove('carly_help.py')
os.remove('setup_docker.py')
os.remove('setup_models.py')
os.remove('edit_models.py')
os.remove('support.py')