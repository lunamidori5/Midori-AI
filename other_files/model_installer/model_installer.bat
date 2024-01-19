@echo off

curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip -o model_installer.zip
powershell Expand-Archive model_installer.zip -DestinationPath . 
model_installer.exe
