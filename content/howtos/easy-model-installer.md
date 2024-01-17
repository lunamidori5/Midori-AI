
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
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer.bat -o model_installer.bat && model_installer.bat
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
curl -sSL https://tea-cup.midori-ai.xyz/download/model_installer.sh | sh
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


*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)