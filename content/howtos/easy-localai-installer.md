
+++
disableToc = false
title = "Easy LocalAI Installer"
weight = 2
+++

## ----- Midori AI Easy LocalAI installer -----
This is the easy installer for LocalAI, please place it in a folder with nothing else in it

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

{{% tab title="Python Virtual Env" %}}
Check your OS and pick your setup as needed to run this, recommened to run on ``python 3.10`` in a virtual env like conda.

```bash
curl https://tea-cup.midori-ai.xyz/download/localai_installer.py -o localai_installer.py

pip install docker python-on-whales pyyaml PyInstaller requests py-cpuinfo

python localai_installer.py
```

{{% /tab %}}
{{< /tabs >}}

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)