import os
import sys

try:
    # this handles the case when we are running the code remotely
    if os.path.exists(os.path.join("..","midori_program_ver.txt")):
        with open(os.path.join("..","midori_program_ver.txt"), 'r') as f: 
            # Read the entire contents of the file into a string
            VERSION = f.read()
    
    elif os.path.exists("midori_program_ver.txt"):
        with open("midori_program_ver.txt", 'r') as f: 
            # Read the entire contents of the file into a string
            VERSION = f.read()
    
    else:
        VERSION = "development"
        
except FileNotFoundError:
    VERSION = "development"