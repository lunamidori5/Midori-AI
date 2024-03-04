#!/bin/bash

# download, extract and execute model_installer
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_linux.tar.gz -o subsystem_manager.tar.gz
tar -xzf subsystem_manager.tar.gz
chmod +x subsystem_manager
./subsystem_manager
