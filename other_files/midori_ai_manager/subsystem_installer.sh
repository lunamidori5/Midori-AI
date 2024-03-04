#!/bin/bash

# download, extract and execute model_installer
curl -sSL https://tea-cup.midori-ai.xyz/download/subsystem_installer_linux.tar.gz -o subsystem_installer.tar.gz
tar -xzf subsystem_installer.tar.gz
chmod +x subsystem_installer
./subsystem_installer
