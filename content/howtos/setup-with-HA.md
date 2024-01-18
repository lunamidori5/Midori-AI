
+++
disableToc = false
title = "Home Assistant x LocalAI"
weight = 10
+++

Home Assistant is an open-source home automation platform that allows users to control and monitor various smart devices in their homes. It supports a wide range of devices, including lights, thermostats, security systems, and more. The platform is designed  to be user-friendly and customizable, enabling users to create automations and routines to make their homes more convenient and efficient. Home Assistant can be accessed through a web interface or a mobile app, and it can be installed on a variety of hardware platforms, such as Raspberry Pi or a dedicated server.

Currently, Home Assistant supports conversation-based agents and services. As of writing this, OpenAIs API is supported as a conversation agent; however, access to your homes devices and entities is only possible through custom components. Local based services, such as LocalAI, are also available as a drop-in replacement for OpenAI services.

An example custom integration to utilize Local-based services in Home-LLM. Home-LLM is a Home Assistant integration developed by Alex O'Connell (acon96) that allows for a completely local Large Language Model acting as a personal assistant. Using LocalAI as the backend is one of the supported platforms .

## Installation Instructions – LocalAI

To install LocalAI, use our [LocalAI Installer]({{%relref "howtos/easy-localai-installer" %}})

## Installation Instructions – Home LLM (The HA plugin)

Home LLM can be installed on Home Assistant in a couple of ways, with the HACS method being the preferred method.

You can use this button to add the repository to HACS and open the download page:

https://my.home-assistant.io/redirect/_change/?redirect=hacs_repository%2F%3Fowner%3Dacon96%26repository%3Dhome-llm%26category%3DIntegration

Once you have downloaded and installed it, be sure to reboot HA. Proceed to “Setting up Llama Conversation to work with HA and LocalAI”.

### Installing Manually

Ensure you have either the Samba, SSH, FTP, or another add-on installed that gives you access to the `config` folder

If there is not already a `custom_components` folder, create one now.

Copy the `custom_components/llama_conversation` folder from this repo to `config/custom_components/llama_conversation` on your Home Assistant machine.

Restart Home Assistant using the "Developer Tools" tab -> Services -> Run `homeassistant.restart`

The "LLaMA Conversation" integration should show up in the "Devices" section now.

## Setting up the plugin for HA & LocalAI

Before adding setting up the Llama Conversation agent in Home Assistant, you must download a LLM in the LocalAI models directory. Although you may use any model you want, this specific integration uses a model that has been specifically fine-tuned to work with Home Assistant. Performance will vary widely with other models.

The model can be found on HuggingFace. It is a 3B v1 model Based on Phi-2:

https://huggingface.co/acon96/Home-3B-v1-GGUF

We recommend trying the Home-3b and the all of the models from the model installer. 

Use the [Auto Model Installer]({{%relref "howtos/easy-model-installer" %}}) for a easy time installing models or follow [Seting up a Model]({{%relref "howtos/easy-model" %}})

## Setting up the "remote" backends:

You need the following settings in order to configure LocalAI backend:

- Hostname: the host of the machine where LocalAI is installed and hosted.
- Port: The port you listed in your ``docker-compose.yaml`` (normally ``8080``)
- Name of the Model as exactly in the `model.yaml` file: This name must EXACTLY match the name as it appears in the file.

The component will validate that the selected model is available for use and will ensure it is loaded remotely.

## Configuring the component as a Conversation Agent

In order to utilize the conversation agent in HomeAssistant:

1. Navigate to "Settings" -> "Voice Assistants"
2. Select "+ Add Assistant"
3. Name the assistant whatever you want.
4. Select the "Conversation Agent" that we created previously
5. If using STT or TTS configure these now
6. Return to the "Overview" dashboard and select chat icon in the top left.
7. From here you can submit queries to the AI agent.

In order for any entities be available to the agent, you must "expose" them first.

1. Navigate to "Settings" -> "Voice Assistants" -> "Expose" Tab
2. Select "+ Expose Entities" in the bottom right
3. Check any entities you would like to be exposed to the conversation agent.

{{% notice note %}}
ANY DEVICES THAT YOU SELECT TO BE EXPOSED TO THE MODEL WILL BE ADDED AS CONTEXT AND POTENTIALLY HAVE THEIR STATE CHANGED BY THE MODEL. ONLY EXPOSE DEVICES THAT YOU ARE OK WITH THE MODEL MODIFYING THE STATE OF, EVEN IF IT IS NOT WHAT YOU REQUESTED. THE MODEL MAY OCCASIONALLY HALLUCINATE AND ISSUE COMMANDS TO THE WRONG DEVICE! USE AT YOUR OWN RISK.
{{% /notice %}}

## Changing the prompt.

Example on how to use the prompt can be seen here.

https://github.com/acon96/home-llm?tab=readme-ov-file#model
