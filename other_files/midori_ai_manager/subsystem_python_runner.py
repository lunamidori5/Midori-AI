import os
import subprocess
import urllib.request
    
# Create  a new virtual environment
print("Creating a new virtual environment...")
os.system('python3 -m venv venv')

# Activate the virtual environment
print("Activating the virtual environment...")
os.system('source venv /bin/activate')

# Download all the needed files
print("Downloading the needed files...")
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/model_installer.py', 'model_installer.py')
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/midori_program_requirments.txt', 'requirments.txt')
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/carly_help.py', 'carly_help.py')
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/setup_docker.py', 'setup_docker.py')
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/setup_models.py', 'setup_models.py')
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/edit_models.py', 'edit_models.py')
urllib.request.urlretrieve('https://tea-cup.midori-ai.xyz/download/support.py', 'support.py')

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

# Deactivate the virtual environment
print("Deactivating the virtual environment...")
os.system('deactivate')