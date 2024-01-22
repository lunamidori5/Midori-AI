
+++
disableToc = false
title = "LocalAI Manager"
weight = 1
+++

{{% notice note %}}

- Due to an unexpected outage from Cloudflare, which resulted in our servers becoming inaccessible, we have promptly rectified the routing issue, thereby restoring normal service.

**Windows Users**
- There seems to be a bug where the manager is adding ``140_1.dll`` to file request. We are working on a fix.

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

{{% /tab %}}
{{< /tabs >}}

## AnythingLLM install

When setting up this copy of AnythingLLM, please use the host computers ip. 
- LocalAI - ``192.168.?.?:8080/v1``
- AnythingLLM - ``192.168.?.?:3001``


## ----- Model Info and Links -----

All models are highly recommened for newer users as they are super easy to use and use the CHAT templ files from [Twinz](https://github.com/TwinFinz)

The models used by this program as of right now are

- 7b: [TheBloke/dolphin-2.6-mistral-7B-GGUF](https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF)
- 43b: [TheBloke/dolphin-2.7-mixtral-8x7b-GGUF](https://huggingface.co/TheBloke/dolphin-2.7-mixtral-8x7b-GGUF)
- 70b: [TheBloke/dolphin-2.2-70B-GGUF](https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF)

## ----- Outside Model Info and Links -----

All of these models originate from outside of the Midori AI model repository, and are not subject to the vetting process of Midori AI, although they are compatible with the model installer.

Note that some of these models may deviate from our conventional model formatting standards (Quantized/Non-Quantized), and will be served using a rounding-down approach. For instance, if you request a Q8 model and none is available, the Q6 model will be served instead, and so on.

- 3b-homellm-v1: [3BV1](https://huggingface.co/acon96/Home-3B-v1-GGUF)
- 3b-homellm-v2: [3BV2](https://huggingface.co/acon96/Home-3B-v2-GGUF)
- 1b-homellm-v1: [1BV1](https://huggingface.co/acon96/Home-1B-v1-GGUF)


*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)

***If you or someone you know would like a model supported by this model manager please reach out to us at [contact-us@midori-ai.xyz](mailto:contact-us@midori-ai.xyz)