#!/bin/bash

# download, extract and execute model_installer
sub_man_dir=$(pwd)
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_linux.tar.gz -o subsystem_manager.tar.gz
curl -sSL https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt -o midori_program_ver.txt
tar -xzf $sub_man_dir/subsystem_manager.tar.gz
chmod 755 $sub_man_dir/subsystem_manager
sudo $sub_man_dir/subsystem_manager