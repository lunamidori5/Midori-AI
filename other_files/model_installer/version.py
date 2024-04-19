import os
import sys

try:
    # this handles the case when we are running the code directly
    with open(os.path.join("..","midori_program_ver.txt"), 'r') as f: 
        # Read the entire contents of the file into a string
        VERSION = f.read()
except FileNotFoundError:
    # this handles the case when we have been bundled into an executable by CI
    with open(os.path.join(sys._MEIPASS, "midori_program_ver.txt"), 'r') as f: 
        # Read the entire contents of the file into a string
        VERSION = f.read()
finally:
    # all else fails, fall back to "development"
    VERSION = "development"