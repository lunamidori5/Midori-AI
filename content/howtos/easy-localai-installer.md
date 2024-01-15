
+++
disableToc = false
title = "Easy LocalAI Installer"
weight = 2
+++

## ----- Midori AI Easy LocalAI installer -----
This is the easy installer for [LocalAI](https://github.com/mudler/LocalAI) / [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm), please place it in a folder with nothing else in it

{{% notice note %}}
- The ``encrypted`` endpoint seems to be having some issues, please use the normal endpoint for now
- A fix has been added, the encrypted endpoint will now fallback to the normal endpoint if server load is high
{{% /notice %}}

{{< tabs >}}
{{% tab title="Windows" %}}
Get started by running these commands one at a time or copy and pastes these into notepad and save it as ``localaiinstaller.bat``

```bat
curl https://tea-cup.midori-ai.xyz/download/localai_installer_windows.zip -o localai_installer.zip
curl https://tea-cup.midori-ai.xyz/download/7zip.exe -o 7zip.exe

call 7zip.exe x localai_installer.zip -odist

call localai_installer.exe
```
{{% /tab %}}

{{% tab title="Linux" %}}
Get started by running these commands one at a time or copy and pastes these into notepad and save it as ``localaiinstaller.sh``

```sh
#!/ bin/bash

curl https://tea-cup.midori-ai.xyz/download/localai_installer_linux.zip -o localai_installer.zip

echo "Unzip the installer how ever you wish to, unzip / 7z works great"

chmod +x localai_installer

sudo ./localai_installer
```

{{% /tab %}}
{{< /tabs >}}

*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)