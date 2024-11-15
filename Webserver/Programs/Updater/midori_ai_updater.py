import os
import subprocess

jobs = []

pixelarch_program_to_update = [
    {"midori-ai-login", "pixelarch-midori-ai-login"},
    {"hf-downloader", "pixelarch-hf-downloader"},
    {"midori-ai-downloader", "pixelarch-midori-ai-downloader"},
    {"midori-ai-login", "pixelarch-midori-ai-file-manager"},
    {"midori-ai-uploader", "pixelarch-midori-ai-uploader"}
    ]

standard_program_to_update = [
    {"midori-ai-login", "standard-linux-midori-ai-login"},
    {"hf-downloader", "standard-linux-hf-downloader"},
    {"midori-ai-downloader", "standard-linux-midori-ai-downloader"},
    {"midori-ai-login", "standard-linux-midori-ai-file-manager"},
    {"midori-ai-uploader", "standard-linux-midori-ai-uploader"}
    ]

with open("/etc/os-release", "r") as f:
    os_release_data = f.read()

if "pixelarch" in os_release_data.lower():
    pass
else:
    pass

# Check if the OS is PixelArch
with open("/etc/os-release", "r") as f:
    os_release_data = f.read()

if "pixelarch" in os_release_data.lower():
    program_to_update = pixelarch_program_to_update
else:
    program_to_update = standard_program_to_update

# Create a temporary directory
os.mkdir("tmp")
os.chdir("tmp")

# Remove existing programs
for program in program_to_update:
    subprocess.run(["sudo", "rm", "-rf", "/usr/local/bin/" + program[0]])

# Download and install new programs
for program in program_to_update:
    subprocess.run(["curl", "-k", "--disable", "--disable-eprt", "-s", "https://tea-cup.midori-ai.xyz/download/" + program[1], ">", program[1]])
    subprocess.run(["chmod", "+x", program[1]])
    subprocess.run(["sudo", "mv", program[1], "/usr/local/bin/" + program[0]])

# Clean up
os.chdir("..")
os.rmdir("tmp")