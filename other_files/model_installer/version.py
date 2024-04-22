import os

# Get the current working directory
cwd = os.getcwd()

# Initialize the VERSION variable to "development"
VERSION = "development"

# Iterate over all the files in the current working directory and all subdirectories
for root, directories, files in os.walk(cwd):
    # Iterate over all the files in the current directory
    for file in files:
        # Check if the file is named "midori_program_ver.txt"
        if file == "midori_program_ver.txt":
            # Open the file and read its contents
            with open(os.path.join(root, file), 'r') as f:
                # Read the entire contents of the file into a string
                VERSION = f.read()

# If the VERSION variable is still "development", then no "midori_program_ver.txt" file was found
if VERSION == "development":
    print("No version file found. Using development version.")