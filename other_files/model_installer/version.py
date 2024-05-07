import os

cwd = os.getcwd()

VERSION = "development"

for root, directories, files in os.walk(cwd):
    for file in files:
        if file == "midori_program_ver.txt":
            with open(os.path.join(root, file), 'r') as f:
                VERSION = f.read()

if VERSION == "development":
    print("No version file found. Using development version.")

def news(blank_line, Fore):
    print(blank_line)
    print(Fore.GREEN + "News" + Fore.WHITE)
    print(Fore.GREEN + "Ollama - As of Ver ->| 24.5.7.0 |<-" + Fore.WHITE)
    print('Please fully uninstall and reinstall Ollama,')
    print('fixes to the backend need a fresh install. (Auto model backup added)')
    print(blank_line)
    print(Fore.GREEN + "LocalAI - As of Ver ->| 24.5.7.0 |<-" + Fore.WHITE)
    print('LocalAIs model downloader / setup program will be reworked to work with gallerys api')
    print(blank_line)
    print(Fore.RED + "Dev Notes" + Fore.WHITE)
    print('Please report bugs to the github or email so we can fix them!')
    print('Thank you all so much for helping with the beta! <3')
    print(blank_line)
    input("Press enter to go to main menu: ")