import os
import sys
import json
import time
import base64
import shutil
import hashlib
import tarfile
import zipfile
import getpass
import pathlib
import platform
import argparse
import subprocess

from halo import Halo

from rich import print
from rich.text import Text
from rich.tree import Tree
from rich.markup import escape
from rich.console import Console
from rich.prompt import Confirm
from rich.filesize import decimal

from cryptography.fernet import Fernet

spinner = Halo(text='Loading', spinner='dots', color='red')

description = """
File manager for packing, unpacking, uploading, and downloading files and folders to / from Midori AI\'s servers.
It uses the Midori AI cloud service to store and retrieve files securely. 
The program encrypts the files before uploading them to Midori AI and decrypts them after downloading them. 
The program can also be used to pack and unpack files into tar archives.
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-i", "--item", type=str, help="Full path of the file or folder")
parser.add_argument("-c", "--pack", action="store_true", help="Create archive (pack)")
parser.add_argument("-x", "--unpack", action="store_true", help="Extract archive (unpack)")
parser.add_argument("-u", "--upload", action="store_true", help="Upload items (must be packed first)")
parser.add_argument("-d", "--download", action="store_true", help="Download items")
parser.add_argument("-P", "--purgetemp", action="store_true", help="Purge temporary files (use with caution)") 

args = parser.parse_args()

purge = args.purgetemp

console = Console()

home_dir = os.path.expanduser("~")
folder_path = os.path.join(home_dir, ".midoriai")
temp_folder_path = os.path.join(folder_path, "tmp")
temp_workfolder = os.path.join(temp_folder_path, 'workfolder')
temp_tar_file = os.path.join(temp_folder_path, 'userfolder.zip')
os.makedirs(folder_path, exist_ok=True)
os.makedirs(temp_folder_path, exist_ok=True)
os.makedirs(temp_workfolder, exist_ok=True)

username_file = os.path.join(folder_path, "MIDORI_AI_USERNAME")
api_key_file = os.path.join(folder_path, "MIDORI_AI_API_KEY_TEMP")

username = "None"

if os.path.exists(username_file):
    with open(username_file, 'r') as f:
        username = str(f.read())
    
    os.system("midori_ai_login")

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

def confirm(text="Are you sure?"):
    """
    Asks the user if they are sure they want to continue.

    Returns:
    True if the user wants to continue, False otherwise.
    """

    while True:
        answer = input(f"{text} (Y/n): ")
        if answer == "" or answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def walk_directory(directory: pathlib.Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        pathlib.Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta][link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            icon = "PYTHON " if path.suffix == ".py" else "FILE "
            tree.add(Text(icon) + text_filename)

def remove_directory_recursively(path, spinner):
    """Recursively removes a directory and its contents."""

    if not os.path.exists(path):
        spinner.warn(f"Path not found: {path}")
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                spinner.start(text=f"Removing file: {file_path}")
                os.remove(file_path)
                spinner.succeed(text=f"Removed file: {file_path}")
            except OSError as e:
                spinner.fail(text=f"Error removing file {file_path}: {str(e)}")

        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                spinner.start(text=f"Removing directory: {dir_path}")
                os.rmdir(dir_path)
                spinner.succeed(text=f"Removed directory: {dir_path}")

            except OSError as e:
                spinner.fail(text=f"Error removing directory {dir_path}: {str(e)}")     
    try:        
        if os.path.exists(path):
            spinner.start(text=f"Removing directory: {path}")
            os.rmdir(path)
            spinner.succeed(text=f"Removed directory: {path}")
    except OSError as e:
        spinner.fail(text=f"Error removing directory {path}: {str(e)}")


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

    key = base64.urlsafe_b64encode(hashlib.sha512(hash_hex.encode() + salt).digest()[:32])
    cipher = Fernet(key)

    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def build_zip(src_dir, compression_level=9):
    """ Builds a directory / file into a zip file, encrypting file contents (except those over 750MB).

    Args:
        src_dir: The source directory / file to compress.
    """
    salt = get_token_from_user()
    size_limit = 750 * 1024 * 1024
    
    spinner.start(text=f"Packing {temp_workfolder}")
    with zipfile.ZipFile(temp_tar_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zipf:
        if os.path.isfile(src_dir):
            file_size = os.path.getsize(src_dir)
            spinner.start(text=f"Reading {src_dir}")  
            with open(src_dir, 'rb') as f:
                data = f.read()
                spinner.start(text=f"Processing {src_dir}") 
                if file_size <= size_limit:
                    encrypted_data = encrypt_user_data(data, username, salt)
                    spinner.start(text=f"Encrypting {src_dir}") 
                    zipf.writestr(os.path.basename(src_dir), encrypted_data)
                    spinner.succeed(text=f"Adding (encrypted) {src_dir} to archive") 

                else:
                    zipf.writestr(os.path.basename(src_dir), data)
                    spinner.succeed(text=f"Adding {src_dir} to archive") 

        elif os.path.isdir(src_dir):
            for root, _, files in os.walk(src_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src_dir)
                    file_size = os.path.getsize(file_path)
                    spinner.start(text=f"Reading {file_path}") 
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        spinner.start(text=f"Processing {file_path}") 

                        if file_size <= size_limit:
                            encrypted_data = encrypt_user_data(data, username, salt)
                            spinner.start(text=f"Encrypting {file_path}") 
                            zipf.writestr(arcname, encrypted_data)
                            spinner.succeed(text=f"Adding (encrypted) {file_path} to archive") 

                        else:
                            zipf.writestr(arcname, data)
                            spinner.succeed(text=f"Adding {file_path} to archive") 

def unpack_tar(dst_dir):
    """Unpacks a zip file into a directory and moves files to a destination directory."""
    salt = get_token_from_user()
    size_limit = 750 * 1024 * 1024

    spinner.start(text='Unpacking zip file...')
    with zipfile.ZipFile(temp_tar_file, 'r') as zipf:
        for info in zipf.infolist():
            with zipf.open(info) as f:
                if info.file_size > size_limit:
                    data = f.read() 
                else:
                    encrypted_data = f.read()
                    data = decrypt_user_data(encrypted_data, username, salt)

                target_path = os.path.join(temp_workfolder, info.filename)
                target_dir = os.path.dirname(target_path)
                os.makedirs(target_dir, exist_ok=True)

                with open(target_path, 'wb') as outfile:
                    outfile.write(data)
            
    spinner.succeed(text=f'Zip file unpacked to {temp_workfolder}')

    spinner.start(text='Moving files to the destination folder...')
    shutil.copytree(temp_workfolder, dst_dir, dirs_exist_ok=True)
    spinner.succeed(text=f"Done moving files to {dst_dir}")

    spinner.start(text=f"Cleaning up temporary folder: {temp_workfolder}")
    remove_directory_recursively(temp_workfolder, spinner)
    spinner.succeed(text=f"Done cleaning up temporary folder: {temp_workfolder}")

def get_token_from_user():
    print("Please enter a token to encrypt / decrypt your data before sending / downloading to / from Midori AI")
    print("Midori AI will not get this token, please record this token in a safe place")
    print("Token will not be shown, please be mindful...")
    while True:
        try:
            print("~" * 50)
            pre_salt = getpass.getpass("Token: ")
            print("~" * 50)
            if confirm():
                salt = str(pre_salt).encode()
                return salt
            else:
                raise Exception("Token not entered")
        except Exception as error:
            print(str(error))

def upload_to_midori_ai():
    filename_to_upload =  "userfile"

    go_on = confirm()

    if go_on:
        try:
            os.system(f"midori_ai_login")
            os.system(f"midori_ai_uploader --type Linux --file \"{temp_tar_file}\" --filename \"{filename_to_upload}\"")
            os.remove(temp_tar_file)
        except Exception as error:
            print(f"Midori AI Uploader failed ({str(error)}), please try again")

def download_from_midori_ai():
    filename_to_download =  "userfile"
    os.system(f"midori_ai_downloader -o \"{temp_tar_file}\" -u {filename_to_download}")

    print(f"Downloaded file: {temp_tar_file}")

def main(args):
    list_of_items = []
    pack = bool(args.pack)
    unpack = bool(args.unpack)
    upload = bool(args.upload)
    download = bool(args.download)

    midori_ai_programs = ["midori_ai_downloader", "midori_ai_uploader", "midori_ai_login"]

    for program in midori_ai_programs:
        if check_programs(program):
            continue
        else:
            raise ImportError(f"You are missing {program} form your path, please install or update them...")
    # Interactive input if no item is provided via command-line
    print(str(args.item))
    if args.item is None:
        use_interactive = Confirm.ask("Do you want to select files/folders interactively?")
        if use_interactive:
           while True:
                item = console.input(prompt="Enter a file or folder path (or type 'done'): ")
                if item.lower() == 'done':
                    break
                
                if not os.path.isabs(item):
                    item = os.path.join(os.getcwd(), item)
                
                if os.path.isdir(item):
                     try:
                        directory = os.path.abspath(item)
                     except IndexError:
                        print("Some type of error happened...")
                     else:
                        tree = Tree(f"[link file://{directory}]{directory}", guide_style="bold bright_blue",)
                        walk_directory(pathlib.Path(directory), tree)
                        print(tree)

                        go_on = confirm(text="Are you sure you want to touch these folders?")

                        if go_on:
                           pass
                        else:
                           continue

                     for root, dirs, files in os.walk(item):
                           for file in files:
                                list_of_items.append(os.path.join(root, file))

                elif os.path.isfile(item):
                    list_of_items.append(item)
                
                else:
                   print(f"[bold red]Error:[/] {str(item).title()} is not a path or could not be found")
                   continue
        else:
             print("[bold blue]No paths given, please pass a path in arguments[/]")
             sys.exit(0)
                
    # Old logic if item provided from command-line
    else:
        item = os.path.join(args.item)
        if not os.path.isabs(item):
            item = os.path.join(os.getcwd(), item)
        
        if os.path.isdir(item):
            try:
                directory = os.path.abspath(item)
            except IndexError:
                print("Some type of error happened...")
            else:
                tree = Tree(f"[link file://{directory}]{directory}", guide_style="bold bright_blue",)
                walk_directory(pathlib.Path(directory), tree)
                print(tree)

                go_on = confirm(text="Are you sure you want to touch these folders?")

                if go_on:
                    pass
                else:
                    sys.exit(0)

            for root, dirs, files in os.walk(item):
                for file in files:
                    list_of_items.append(os.path.join(root, file))

        elif os.path.isfile(item):
            list_of_items.append(item)
        
        else:
            raise FileNotFoundError(f"{str(item).title()} is not a path or could not be found")

    os.chdir(temp_folder_path)

    if pack:
        for working_item in list_of_items:
            spinner.start(text=f"Copying {working_item} to {temp_workfolder}")

            temp_working_item = os.path.join(temp_workfolder, os.path.basename(working_item))
            shutil.copy2(working_item, temp_working_item)

            spinner.succeed(text=f"Copied {working_item} to {temp_working_item}")

        build_zip(temp_workfolder)
        spinner.succeed(text=f"Packed {temp_workfolder}")

    if upload:
        if os.path.exists(temp_tar_file):
            upload_to_midori_ai()

            remove_directory_recursively(temp_workfolder, spinner)
        else:
            print("Please pack the files before uploading...")

    if download:
        download_from_midori_ai()

    if unpack:
        unpack_tar(item)


if __name__ == "__main__":
    if purge:
        remove_directory_recursively(temp_folder_path, spinner)
        sys.exit(0)

    try:
        main(args)
    except Exception as error:
        print(str(error))