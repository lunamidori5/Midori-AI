"""
#!/usr/bin/env bash

source ~/sigma/logo.sh

read -p "github repo name (user/thing): " repolink

git clone https://github.com/${repolink}.git

echo "git clone succesful!"
"""

import subprocess

github_repo = input("github repo name (user/thing): ")

url = f"https://github.com/{github_repo}.git"

print(f"Downloading `{url}`")

subprocess.call(["git", "clone", url])