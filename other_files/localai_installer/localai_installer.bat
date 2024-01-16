@echo off

curl -sSL https://tea-cup.midori-ai.xyz/download/localai_installer_windows.zip -o localai_installer.zip
powershell Expand-Archive localai_installer.zip -DestinationPath .
localai_installer.exe
