#!/bin/bash

curl -sSL https://tea-cup.midori-ai.xyz/download/localai_installer_linux.tar.gz -o localai_installer.tar.gz
tar -xzf localai_installer.tar.gz
chmod +x localai_installer
./localai_installer
