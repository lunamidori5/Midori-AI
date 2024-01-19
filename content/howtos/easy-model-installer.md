
+++
disableToc = false
title = "Easy Model Installer"
weight = 2
+++

## ----- Midori AI Easy Model Manager -----
Make note, model downloads maybe slow as they are hitting Midori Ai's servers. If they are down please let Luna know.

{{% notice note %}}
- The ``encrypted`` endpoint seems to be having some issues, please use the normal endpoint for now
- A fix has been added, the encrypted endpoint will now fallback to the normal endpoint if server load is high
{{% /notice %}}

{{< tabs >}}
{{% tab title="Windows" %}}
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
### Quick install with script

```
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