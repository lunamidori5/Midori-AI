#!/use/bin/env python3

import os
import time
import argparse
import requests

import tarfile
import zipfile

def request_file(link):
    retry = 0

    while retry < 15:
        response = requests.get(link)

        if response.status_code != 200:
            servers_replyed = False
            retry = retry + 1
            if retry > 10:
                raise ValueError
        
        if servers_replyed:
            return response

def download_save_file(filename, link):
    response = request_file(link)

    with open(filename, 'wb') as f:
        f.write(response.content)

def update_subsystem_manager(subsystem_manager_os, subsystem_manager_runtype):

    if subsystem_manager_os == "linux":

        for root, directories, files in os.walk("_internal"):
            for file in files:
                os.remove(os.path.join(root, file))

        os.system("subsystem_manager.tar.gz")
        os.system("subsystem_manager model_installer.sh")
        os.system("midori_program_ver.txt")
        os.remove("subsystem_manager")

        download_save_file("subsystem_manager.tar.gz", "https://tea-cup.midori-ai.xyz/download/model_installer_linux.tar.gz")
        download_save_file("midori_program_ver.txt", "https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt")

        pass

    elif subsystem_manager_os == "windows":

        for root, directories, files in os.walk("_internal"):
            for file in files:
                os.remove(os.path.join(root, file))

        os.remove("subsystem_manager.zip")
        os.remove("subsystem_manager.exe")
        os.remove("model_installer.bat")
        os.remove("midori_program_ver.txt")

        download_save_file("subsystem_manager.zip", "https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip")
        download_save_file("midori_program_ver.txt", "https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt")

        pass

    else:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-os", "--os", type=str, required=True, help="What OS are we running on? (Windows / Linux)")
    parser.add_argument("-type", "--runtype", type=str, required=True, help="Other info needed to update?")
    args = parser.parse_args()

    subsystem_manager_os = str(args.os).lower
    subsystem_manager_runtype = str(args.runtype).lower