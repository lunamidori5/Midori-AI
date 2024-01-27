
+++
disableToc = false
title = "LocalAI Manager"
weight = 1
+++

{{% notice note %}}

- Servers are overloaded at this time, deeply sorry for the slow download speeds. More servers are on their way! - Luna

**Windows Users**
- There seems to be a bug where the manager is adding ``140_1.dll`` to file request. We are working on a fix.
- There seems to be false positive from virus checkers, [this file](https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip) is safe to download, [check here for the code](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

{{% /notice %}}

## ----- Midori AI LocalAI Manager -----
The LocalAI manager  can set up and install [LocalAI](https://github.com/mudler/LocalAI)/[AnythingLLM](https://github.com/Mintplex-Labs/anything-llm). Place it in a folder with nothing else before use. If you are just using this for model management of a running LocalAI docker, put this in the folder with the `docker-compose.yaml` file.

Note that model downloads may be slow because they are hitting Midori Ai's servers. If the servers are down, please inform Luna.

{{< tabs >}}
{{% tab title="Windows" %}}
### Prerequisites
[Docker Desktop Windows](https://docs.docker.com/desktop/install/windows-install/)

### Quick install

1. Download - https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip
2. Unzip into LocalAI folder
3. Run `model_installer.exe`

### Quick install with script

Open a Command Prompt or PowerShell terminal and run:

```bat
curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/model_installer.bat -o model_installer.bat && model_installer.bat
```

### Manual download and installation

Open a Command Prompt or PowerShell terminal and run:

```bat
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip -o model_installer.zip
powershell Expand-Archive model_installer.zip -DestinationPath .
model_installer.exe
```
[![Windows Build Test](https://github.com/lunamidori5/Midori-AI/actions/workflows/Windows_Build_Test.yml/badge.svg?branch=master)](https://github.com/lunamidori5/Midori-AI/actions/workflows/Windows_Build_Test.yml)
{{% /tab %}}

{{% tab title="Linux" %}}
### Prerequisites
[Docker Desktop Linux](https://docs.docker.com/desktop/install/linux-install/) 

or 

[Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Quick install with script

```sh
curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/model_installer.sh | sh
```

### Manual download and installation

Open a terminal and run:

```sh
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_linux.tar.gz -o model_installer.tar.gz
tar -xzf model_installer.tar.gz
chmod +x model_installer
./model_installer
```
[![Linux Build Test](https://github.com/lunamidori5/Midori-AI/actions/workflows/Linux_Build_Test.yml/badge.svg?branch=master)](https://github.com/lunamidori5/Midori-AI/actions/workflows/Linux_Build_Test.yml)
{{% /tab %}}
{{< /tabs >}}

## AnythingLLM install

When setting up this copy of AnythingLLM, please use the host computers ip. 
- LocalAI - ``192.168.?.?:8080/v1``
- AnythingLLM - ``192.168.?.?:3001``


## ----- Model Info and Links -----

Check out our [Model Repository]({{%relref "models" %}}) for info about the models used and supported!

## ----- Footnotes -----

*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)

***If you or someone you know would like a model supported by this model manager please reach out to us at [contact-us@midori-ai.xyz](mailto:contact-us@midori-ai.xyz)