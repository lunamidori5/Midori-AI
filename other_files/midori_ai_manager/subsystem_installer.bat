@echo off

curl -sSL https://tea-cup.midori-ai.xyz/download/subsystem_installer_windows.zip -o subsystem_installer.zip
powershell Expand-Archive subsystem_installer.zip -DestinationPath . -Force
subsystem_installer.exe
