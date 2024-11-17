import os
import sys
import json
import time
import base64
import shutil
import hashlib
import tarfile
import getpass
import platform
import argparse
import subprocess

from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description="File manager for packing, unpacking, uploading, and downloading files and folders to / from Midori AI\'s servers")
parser.add_argument("-i", "--item", required=True, type=str, help="Full path of the File or Folder being worked with")
parser.add_argument("-t", "--type", required=True, type=str, help="Type of Item (file or folder)")
parser.add_argument("-p", "--pack", action="store_true", help="Pack items")
parser.add_argument("-un", "--unpack", action="store_true", help="Unpack items")
parser.add_argument("-up", "--upload", action="store_true", help="Upload items")
parser.add_argument("-d", "--download", action="store_true", help="Download items")

args = parser.parse_args()

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
temp_folder_path = os.path.join(folder_path, "tmp")
temp_workfolder = os.path.join(temp_folder_path, 'workfolder')
temp_tar_file = os.path.join(temp_folder_path, 'userfolder.tar')
compressed_tar_file = os.path.join(temp_folder_path, 'userfolder.xz.tar')
encrypted_tar_file = os.path.join(temp_folder_path, 'userfolder.xz.tar.excrypted')
os.makedirs(folder_path, exist_ok=True)
os.makedirs(temp_folder_path, exist_ok=True)
os.makedirs(temp_workfolder, exist_ok=True)

print(os.getcwd())
os.chdir(temp_folder_path)
print(os.getcwd())

username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

username = "None"

if os.path.exists(username_file):
    with open(username_file, 'r') as f:
        username = str(f.read())
    
    os.system("midori-ai-login")

if username == "None":
    if hasattr(args, "username"):
        username = str(args.username)

if username == "None":
    print("You have not logged into Midori AI\'s servers...")
    sys.exit(25)

def check_programs(program_name):
  try:
    shutil.which(program_name)
    return True
  except shutil.Error:
    return False

def confirm():
    """
    Asks the user if they are sure they want to continue.

    Returns:
    True if the user wants to continue, False otherwise.
    """

    while True:
        answer = input("Are you sure? (Y/n): ")
        if answer == "" or answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def encrypt_user_data(data: bytes, username: str, salt):
    stats = {
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
    }

    stats_json = json.dumps(stats)
    os_version = os.uname().machine

    hash_object = hashlib.sha512(stats_json.encode())
    os_hash_object = hashlib.sha512(os_version.encode())

    password = hash_object.hexdigest()
    twoflogin = os_hash_object.hexdigest()

    stats = {
        "user": {
            "username": username,
            "platform_hash": password,
            "os_version_hash": twoflogin,
        },
    }

    stats_json = json.dumps(stats)

    hash_object = hashlib.sha512(stats_json.encode())
    hash_hex = hash_object.hexdigest()
    
    # Generate a 32-byte Fernet-compatible key
    key = base64.urlsafe_b64encode(hashlib.sha512(hash_hex.encode() + salt).digest()[:32])

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def decrypt_user_data(encrypted_data: bytes, username: str, salt):
    stats = {
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
    }

    stats_json = json.dumps(stats)
    os_version = os.uname().machine

    hash_object = hashlib.sha512(stats_json.encode())
    os_hash_object = hashlib.sha512(os_version.encode())

    password = hash_object.hexdigest()
    twoflogin = os_hash_object.hexdigest()

    stats = {
        "user": {
            "username": username,
            "platform_hash": password,
            "os_version_hash": twoflogin,
        },
    }

    stats_json = json.dumps(stats)

    hash_object = hashlib.sha512(stats_json.encode())
    hash_hex = hash_object.hexdigest()

    # Generate the same 32-byte Fernet-compatible key for decryption
    key = base64.urlsafe_b64encode(hashlib.sha512(hash_hex.encode() + salt).digest()[:32])
    cipher = Fernet(key)

    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def build_tar(src_dir):
    """ Builds a directory into a tar file.

    Args:
    src_dir: The source directory to compress.
    """
    with tarfile.open(temp_tar_file, "a") as tar:
        tar.add(src_dir)

def compress_tar():
    print('Compressing tar file...')

    with tarfile.open(compressed_tar_file, "w:xz") as tar:
        tar.add(temp_tar_file)
    
    os.remove(temp_tar_file)
    
    print('Tar file compressed and saved as ', temp_tar_file)

def flatten_directory(base_dir):
    """Flatten a directory by moving all files to the base directory and removing nested folders."""
    # Move files to the base directory
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(base_dir, file)

            # Handle duplicate filenames
            if os.path.exists(new_file_path):
                base, ext = os.path.splitext(new_file_path)
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_path = f"{base}_{counter}{ext}"
                    counter += 1

            print(f"Moving {file_path} to {new_file_path}")
            os.rename(file_path, new_file_path)

    # Remove empty directories
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Check if directory is empty
                print(f"Removing empty directory: {dir_path}")
                os.rmdir(dir_path)


def unpack_tar(tar_file, dst_dir):
    """Unpacks a tar file into a directory, flatten it, and move files to a destination directory."""

    print('Unpacking tar file...')
    with tarfile.open(tar_file, "r") as tar:
        tar.extractall(temp_workfolder)
    print(f'Tar file unpacked to {temp_workfolder}')

    print('Flattening directory layout...')
    flatten_directory(temp_workfolder)
    print('Directory layout flattened.')

    print('Moving files to the destination folder...')
    for root, dirs, files in os.walk(temp_workfolder):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(dst_dir, file)

            # Handle duplicate filenames in destination
            if os.path.exists(new_file_path):
                base, ext = os.path.splitext(new_file_path)
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_path = f"{base}_{counter}{ext}"
                    counter += 1

            print(f"Moving {file_path} to {new_file_path}")
            os.rename(file_path, new_file_path)

    # Clean up temp directory
    print(f"Cleaning up temporary folder: {temp_workfolder}")
    os.rmdir(temp_workfolder)
    print(f"Done moving files to {dst_dir}")


def uncompress_internet_tar(compressed_tar_file, dst_dir):
    """Uncompress a tar.xz file, flatten it, and move files to a destination directory."""

    print('Uncompressing tar.xz file...')
    with tarfile.open(compressed_tar_file, "r:xz") as tar:
        tar.extractall(temp_workfolder)
    print(f'Tar.xz file uncompressed to {temp_workfolder}')

    print('Flattening directory layout...')
    flatten_directory(temp_workfolder)
    print('Directory layout flattened.')

    print('Moving files to the destination folder...')
    for root, dirs, files in os.walk(temp_workfolder):
        for file in files:
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(dst_dir, file)

            # Handle duplicate filenames in destination
            if os.path.exists(new_file_path):
                base, ext = os.path.splitext(new_file_path)
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_path = f"{base}_{counter}{ext}"
                    counter += 1

            print(f"Moving {file_path} to {new_file_path}")
            os.rename(file_path, new_file_path)

    # Clean up temp directory
    print(f"Cleaning up temporary folder: {temp_workfolder}")
    os.rmdir(temp_workfolder)
    print(f"Done moving files to {dst_dir}")

def upload_to_midori_ai(data: bytes):
    print("Please enter a token to encrypt your data before sending it to Midori AI")
    print("Midori AI will not get this token, please record this token in a safe place")
    print("Token will not be shown, please be mindful...")
    print("~" * 50)
    pre_salt = getpass.getpass("Token: ")
    salt = str(pre_salt).encode()
    filename_to_upload =  "userfile"

    go_on = confirm()

    if go_on:
        encrypted_data = encrypt_user_data(data, username, salt)

        with open(encrypted_tar_file, "wb") as f:
            f.write(encrypted_data)

        try:
            while not os.path.isfile(encrypted_tar_file):
                time.sleep(1)

            os.system(f"midori-ai-uploader --type Linux --file \"{encrypted_tar_file}\" --filename \"{filename_to_upload}\"")
            os.remove(compressed_tar_file)
            os.remove(encrypted_tar_file)
        except Exception as error:
            print(f"Midori AI Uploader failed ({str(error)}), please try again")

def download_from_midori_ai():
    print("Please enter a token to decrypt your data after downloading it from Midori AI")
    print("Token will not be shown, please be mindful...")
    print("~" * 50)
    pre_salt = getpass.getpass("Token: ")
    salt = str(pre_salt).encode()
    filename_to_download =  "userfile"
    os.system(f"midori-ai-downloader -o \"{encrypted_tar_file}\" -u {filename_to_download}")

    with open(encrypted_tar_file, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_user_data(encrypted_data, username, salt)

    os.remove(encrypted_tar_file)

    with open(compressed_tar_file, "wb") as f:
        f.write(decrypted_data)

    print(f"Downloaded file: {compressed_tar_file}")

def main(args):
    list_of_items = []
    item = os.path.join(args.item)
    item_type = str(args.type).lower()
    pack = bool(args.pack)
    unpack = bool(args.unpack)
    upload = bool(args.upload)
    download = bool(args.download)

    if pack and unpack:
        raise Exception("You cannot pack/unpack at the same time.")

    if upload and download:
        raise Exception("You cannot upload/download at the same time.")

    midori_ai_programs = ["midori-ai-downloader", "midori-ai-uploader", "midori-ai-login"]

    for program in midori_ai_programs:
        if check_programs(program):
            continue
        else:
            print(f"You are missing {program} form your path, please install or update them...")
    
    if "folder" in item_type:
        for root, dirs, files in os.walk(item):
            for file in files:
                list_of_items.append(os.path.join(root, file))

    if "file" in item_type:
        list_of_items.append(item)

    if pack:
        print("Packing items!")
        for working_item in list_of_items:
            print(f"Packing {working_item}")
            build_tar(working_item)

    if upload:
        if os.path.exists(temp_tar_file):

            compress_tar()

            with open(compressed_tar_file, "rb") as f:
                bytes_to_upload = f.read()
            
            upload_to_midori_ai(bytes_to_upload)

    if download:
        download_from_midori_ai()

    if unpack:
        uncompress_internet_tar(compressed_tar_file, item)
        unpack_tar(temp_tar_file, item)
        os.remove(compressed_tar_file)
        os.remove(temp_tar_file)


if __name__ == "__main__":
    main(args)