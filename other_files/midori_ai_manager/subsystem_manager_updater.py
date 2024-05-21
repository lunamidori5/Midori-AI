#!/usr/bin/env python3

import os
import time
import argparse
import requests

import tarfile
import zipfile

def request_file(link):
    retry = 0

    while retry < 15:
        print(f"Trying to request file from {link}. Retry number: {retry}")
        response = requests.get(link)

        if response.status_code != 200:
            print(f"Server replied with status code {response.status_code}. Retrying in 5 seconds")
            servers_replyed = False
            retry = retry + 1
            if retry > 10:
                raise ValueError
        else:
            servers_replyed = True

        if servers_replyed:
            print("Server replied with status code 200. Returning the response")
            return response

def download_save_file(filename, link):
    response = request_file(link)

    with open(filename, 'wb') as f:
        print(f"Saving file {filename} to disk")
        f.write(response.content)

def remove_file(file):
    times = 0
    while times < 150:
        try:
            os.remove(file)
            if not os.path.isfile(file):
                print(f"File {file} successfully removed.")
                break
            else:
                print("Trying again the file was not removed")
        except Exception as e:
            times = times + 1
            print(str(e))

def update_subsystem_manager(subsystem_manager_os, subsystem_manager_runtype):
    print("Updating subsystem manager...")
    os.chdir("/app/system_files")

    if subsystem_manager_os.lower() == "linux":

        print("Removing old files...")
        for root, directories, files in os.walk("_internal"):
            for file in files:
                remove_file(os.path.join(root, file))

        remove_file("subsystem_manager.tar.gz")
        remove_file("model_installer.sh")
        remove_file("subsystem_manager")
        remove_file("midori_program_ver.txt")

        print("Downloading new files...")
        download_save_file("subsystem_manager.tar.gz", "https://tea-cup.midori-ai.xyz/download/model_installer_linux.tar.gz")
        download_save_file("midori_program_ver.txt", "https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt")

        print("Extracting files...")
        with tarfile.open("subsystem_manager.tar.gz", "r") as tar:
            tar.extractall()
        print("Done Extracting files")

        remove_file("subsystem_manager.tar.gz")

        print("Please restart the manager at this time.")

        return True

    elif subsystem_manager_os.lower() == "windows":

        print("Removing old files...")
        for root, directories, files in os.walk("_internal"):
            for file in files:
                os.remove(os.path.join(root, file))

        remove_file("subsystem_manager.zip")
        remove_file("subsystem_manager.exe")
        remove_file("model_installer.bat")
        remove_file("midori_program_ver.txt")

        print("Downloading new files...")
        download_save_file("subsystem_manager.zip", "https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip")
        download_save_file("midori_program_ver.txt", "https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt")

        print("Extracting files...")
        with zipfile.ZipFile("subsystem_manager.zip", "r") as zip:
            zip.extractall()
        print("Done Extracting files")

        remove_file("subsystem_manager.zip")

        return True

    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-os", "--os", type=str, required=True, help="What OS are we running on? (Windows / Linux)")
    parser.add_argument("-type", "--runtype", type=str, required=True, help="Other info needed to update?")
    args = parser.parse_args()

    subsystem_manager_os = args.os
    subsystem_manager_runtype = args.runtype

    print(f"OS: {subsystem_manager_os}")
    print(f"Type: {subsystem_manager_runtype}")

    print("Updating in...")

    for timer in range(3, 0, -1):
        print(f"{timer}...")
        time.sleep(1)

    update_subsystem_manager(subsystem_manager_os, subsystem_manager_runtype)

    exit()