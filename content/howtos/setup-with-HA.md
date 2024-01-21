
+++
disableToc = false
title = "Home Assistant x LocalAI"
weight = 10
+++

Home Assistant is an open-source home automation platform that allows users to control and monitor various smart devices in their homes. It supports a wide range of devices, including lights, thermostats, security systems, and more. The platform is designed  to be user-friendly and customizable, enabling users to create automations and routines to make their homes more convenient and efficient. Home Assistant can be accessed through a web interface or a mobile app, and it can be installed on a variety of hardware platforms, such as Raspberry Pi or a dedicated server.

Currently, Home Assistant supports conversation-based agents and services. As of writing this, OpenAIs API is supported as a conversation agent; however, access to your homes devices and entities is only possible through custom components. Local based services, such as LocalAI, are also available as a drop-in replacement for OpenAI services.

An example custom integration to utilize Local-based services in Home-LLM. Home-LLM is a Home Assistant integration developed by Alex O'Connell (acon96) that allows for a completely local Large Language Model acting as a personal assistant. Using LocalAI as the backend is one of the supported platforms .

## Installation Instructions – LocalAI

To install LocalAI, use our [LocalAI Manager]({{%relref "howtos/easy-model-installer" %}})

## Installation Instructions – Home LLM (The HA plugin)


Please follow the installation instructions on [Home-LLM](https://github.com/acon96/home-llm?tab=readme-ov-file#installing-with-hacs) repo to install HACS plug-in.

## Setting up the plugin for HA & LocalAI

Before adding setting up the Llama Conversation agent in Home Assistant, you must download a LLM in the LocalAI models directory. Although you may use any model you want, this specific integration uses a model that has been specifically fine-tuned to work with Home Assistant. Performance will vary widely with other models.

The models can be found on the Midori AI model repo, as a part of the LocalAI manager.

Use the [LocalAI Manager]({{%relref "howtos/easy-model-installer" %}}) for a easy time installing models or follow [Seting up a Model]({{%relref "howtos/easy-model" %}})

## Setting up the "remote" backends:

You need the following settings in order to configure LocalAI backend:

- Hostname: the host of the machine where LocalAI is installed and hosted.
- Port: The port you listed in your ``docker-compose.yaml`` (normally ``8080``)
- Name of the Model as exactly in the `model.yaml` file: This name must EXACTLY match the name as it appears in the file.

The component will validate that the selected model is available for use and will ensure it is loaded remotely.

Once you have this information, proceed to “add Integration” in Home Assistant and search for “Llama Conversation” Here you will be greeted with a config flow to add the above information. Once the information is accepted, search your integrations for “Llama Conversation” and you can now view your settings including prompt, temperature, top K and other parameters.

## Configuring the component as a Conversation Agent

In order to utilize the conversation agent in HomeAssistant, you will need to configure it as a conversation agent. This can be done by following the the instructions [here](https://github.com/acon96/home-llm?tab=readme-ov-file#configuring-the-component-as-a-conversation-agent).

{{% notice note %}}
ANY DEVICES THAT YOU SELECT TO BE EXPOSED TO THE MODEL WILL BE ADDED AS CONTEXT AND POTENTIALLY HAVE THEIR STATE CHANGED BY THE MODEL. ONLY EXPOSE DEVICES THAT YOU ARE OK WITH THE MODEL MODIFYING THE STATE OF, EVEN IF IT IS NOT WHAT YOU REQUESTED. THE MODEL MAY OCCASIONALLY HALLUCINATE AND ISSUE COMMANDS TO THE WRONG DEVICE! USE AT YOUR OWN RISK.
{{% /notice %}}

## Changing the prompt.

Example on how to use the prompt can be seen here.

https://github.com/acon96/home-llm?tab=readme-ov-file#model
