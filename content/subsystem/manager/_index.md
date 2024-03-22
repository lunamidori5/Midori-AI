+++
disableToc = false
title = "Subsystem Manager"
weight = 1
+++

![Midori AI photo](https://tea-cup.midori-ai.xyz/download/logosubsystem.png)

## ----- How to Enter Beta -----

You are already useing the new Beta! As of 24.4.1!

# -- Midori AI Subsystem Manager --

**How Docker Works**

Docker is a containerization platform that allows you to package and run applications in isolated and portable environments called containers. Containers share the host operating system kernel but have their own dedicated file system, processes, and resources. This isolation allows applications to run independently of the host environment and each other, ensuring consistent and predictable behavior.

**Midori AI Subsystem**

The Midori AI Subsystem extends Docker's capabilities by providing a modular and extensible platform for managing AI workloads. Each AI system is encapsulated within  its own dedicated Docker image, which contains the necessary software and dependencies. This approach provides several benefits:

* **Simplified Deployment:** The Midori AI Subsystem provides a streamlined and efficient way to deploy AI systems using Docker container technology.
* **Eliminates Guesswork:** Standardized configurations and settings reduce complexities, enabling seamless setup and management of AI programs.

{{% notice style="warning" title="Notice" %}}
**Warnings / Heads up**
- This program is in beta! By using it you take on risk, please see the disclaimer in the footnotes
- The webserver has been moved to the new OS and Server!

**Server outage**
- Midori AI's servers went down due to a programming error, this has been fixed thank you

**Windows Users**
- There seems to be a bug where the manager is adding ``140_1.dll`` to file request. We are working on a fix.
- There seems to be false positive from virus checkers, [this file](https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip) is safe to download, [check here for the code](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)
- This seems to be a widely known bug with Google Chorme, Edge, and others, here are our [virus scans from a few websites](https://www.virustotal.com/gui/url/6d36b491ed76cc9f1e284b43fe7fcd4158696edb5730b614469bbdf6f1e616f0/details). We will try other ways of packing the files.
{{% /notice %}}

## Install Midori AI Subsystem Manager

{{% notice style="info" title="Notice" %}}
- As we are in beta, we have implemented telemetry to enhance bug discovery and resolution. This data is anonymized and will be configurable when out of beta.
{{% /notice %}}

{{< tabs >}}
{{% tab title="Windows" %}}
### Prerequisites
[Docker Desktop Windows](https://docs.docker.com/desktop/install/windows-install/)

### Recommended
Please make a folder for the Manager program with nothing in it, do not use the user folder.

### Quick install

1. Download - https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip
2. Unzip into LocalAI folder
3. Run `subsystem_manager.exe`

### Quick install with script

Open a Command Prompt or PowerShell terminal and run:

```bat
curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/shell_files/model_installer.bat -o subsystem_manager.bat && subsystem_manager.bat
```

### Manual download and installation

Open a Command Prompt or PowerShell terminal and run:

```bat
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_windows.zip -o subsystem_manager.zip
powershell Expand-Archive subsystem_manager.zip -DestinationPath .
subsystem_manager.exe
```
[![Windows Build Test](https://github.com/lunamidori5/Midori-AI/actions/workflows/Windows_Build_Test.yml/badge.svg?branch=master)](https://github.com/lunamidori5/Midori-AI/actions/workflows/Windows_Build_Test.yml)
{{% /tab %}}

{{% tab title="Linux / WSL" %}}
### Prerequisites
[Docker Desktop Linux](https://docs.docker.com/desktop/install/linux-install/) / [Docker Desktop Windows](https://docs.docker.com/desktop/install/windows-install/)

or 

[Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Quick install with script

```sh
curl -sSL https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/other_files/model_installer/shell_files/model_installer.sh | sh
```

### Manual download and installation

Open a terminal and run:

```sh
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer_linux.tar.gz -o subsystem_manager.tar.gz
tar -xzf subsystem_manager.tar.gz
chmod +x subsystem_manager
./subsystem_manager
```
[![Linux Build Test](https://github.com/lunamidori5/Midori-AI/actions/workflows/Linux_Build_Test.yml/badge.svg?branch=master)](https://github.com/lunamidori5/Midori-AI/actions/workflows/Linux_Build_Test.yml)
{{% /tab %}}
{{< /tabs >}}

## ----- Model Info and Links -----

Check out our [Model Repository]({{%relref "models" %}}) for info about the models used and supported!

## ----- Disclaimer -----

The functionality of this product is subject to a variety of factors that are beyond our control, and we cannot guarantee that it will work flawlessly in all situations. We have taken every possible measure to ensure that the product functions as intended, but there may be instances where it does not perform as expected. Please be aware that we cannot be held responsible for any issues that arise due to the product's functionality not meeting your expectations. By using this product, you acknowledge and accept the inherent risks associated with its use, and you agree to hold us harmless for any damages or losses that may result from its functionality not being guaranteed.

## ----- Footnotes -----

*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)

***If you or someone you know would like a model supported by this model manager please reach out to us at [contact-us@midori-ai.xyz](mailto:contact-us@midori-ai.xyz)