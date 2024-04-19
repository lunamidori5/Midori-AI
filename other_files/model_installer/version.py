import os
import sys

try:
    # this handles the case when we are running the code remotely
    with open(os.path.join("..","midori_program_ver.txt"), 'r') as f: 
        # Read the entire contents of the file into a string
        VERSION = f.read()
except FileNotFoundError:
    VERSION = "development"

try:
    # this handles the case when we are running the code directly
    with open("midori_program_ver.txt", 'r') as f: 
        # Read the entire contents of the file into a string
        VERSION = f.read()
except FileNotFoundError:
    VERSION = "development"