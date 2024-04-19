@echo off

curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip -o subsystem_manager.zip
curl -sSL https://tea-cup.midori-ai.xyz/download/midori_program_ver.txt -o midori_program_ver.txt
powershell Expand-Archive subsystem_manager.zip -DestinationPath . -Force
subsystem_manager.exe
