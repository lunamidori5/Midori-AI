
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
### Quick install with script

Open a Command Prompt or PowerShell terminal and run:

```bat
curl -sSL https://tea-cup.midori-ai.xyz/download/localai_installer.bat -o localai_installer.bat && localai_installer.bat
```

### Manual download and installation

Open a Command Prompt or PowerShell terminal and run:

```bat
curl -sSL https://tea-cup.midori-ai.xyz/download/localai_installer_windows.zip -o localai_installer.zip
powershell Expand-Archive localai_installer.zip -DestinationPath .
localai_installer.exe
```
{{% /tab %}}

{{% tab title="Linux" %}}
### Quick install with script

```
curl -sSL https://tea-cup.midori-ai.xyz/download/localai_installer.sh | sh
```

### Manual download and installation

Open a terminal and run:

```sh
curl -sSL https://tea-cup.midori-ai.xyz/download/localai_installer_linux.tar.gz -o localai_installer.tar.gz
tar -xzf localai_installer.tar.gz
chmod +x localai_installer
./localai_installer
```

{{% /tab %}}
{{< /tabs >}}

*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)

## AnythingLLM install

When setting up this copy of AnythingLLM, please use the host computers ip. 
- LocalAI - ``192.168.?.?:8080/v1``
- AnythingLLM - ``192.168.?.?:3001``

LocalAI LLM Model / Embedding Model setup can be found here - [Model Installer]({{%relref "howtos/easy-model-installer" %}})