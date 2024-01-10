
+++
disableToc = false
title = "Easy Model Installer"
weight = 2
+++

## ----- Midori AI Easy Model installer -----
Make note, model downloads maybe slow as they are hitting Midori Ai's servers. If they are down please let Luna know.

{{< tabs >}}
{{% tab title="Windows" %}}
To run this program you will need to run these commands in the same folder as your ``LocalAI's`` ``docker-compose.yaml``
Get started by running these commands one at a time or copy and pastes these into notepad and save it as ``modelinstaller.bat``

```bat
@echo off
curl https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip -o model_installer.zip
curl https://tea-cup.midori-ai.xyz/download/7zip.exe -o 7zip.exe

7zip.exe x model_installer.zip -odist

copy dist\model_installer.exe .

model_installer.exe
```
{{% /tab %}}

{{% tab title="Linux" %}}
To run this program you will need to run these commands in the same folder as your ``LocalAI's`` ``docker-compose.yaml``
Get started by running these commands one at a time or copy and pastes these into notepad and save it as ``modelinstaller.sh``

```sh
#!/ bin/bash

curl https://tea-cup.midori-ai.xyz/download/model_installer_linux.zip -o model_installer.zip

echo "Unzip the installer how ever you wish to, unzip / 7z works great"

chmod +x dist/model_installer

cp dist/model_installer .

sudo ./model_installer
```

{{% /tab %}}
{{< /tabs >}}

## ----- Model Info and Links -----

All models are highly recommened for newer users as they are super easy to use and use the CHAT templ files from Twinz

The models used by this program as of right now are
```
7b - TheBloke/dolphin-2.6-mistral-7B-GGUF - https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF
43b - TheBloke/dolphin-2.7-mixtral-8x7b-GGUF - https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF
70b - TheBloke/dolphin-2.2-70B-GGUF - https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF
```

**If you would like to give to help us get better servers - [PayPal](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)