+++
disableToc = false
title = "Install LocalAI Models"
weight = 2
+++

![Midori AI photo](https://tea-cup.midori-ai.xyz/download/Midori_subsystem_x_localai.png)

## Install a Model from the Midori AI Model Repo

#### Step 1:
- Start the Midori AI Subsystem

#### Step 2:
- On the Main Menu, Type `5` to Enter the Backend Program Menu

#### Step 3:
- On the Backend Program Menu, Type `10` to Enter the LocalAI Model Installer

#### Step 4a:
- If you have LocalAI installed in the subsystem, skip this step.
- If you do not have LocalAI installed in the subsystem, the program will ask you to enter the LocalAI docker's name. It will look something like `localai-api-1`, but not always. If you need help, reach out on the [Midori AI Discord](https://discord.gg/xdgCx3VyHU) / [Email](mailto:contact-us@midori-ai.xyz).

#### Step 4b:
- If you have GPU support installed in that image, type `yes`.
- If you do not have GPU support installed in that image, type `no`.

#### Step 5:
- Type in the size you would like for your LLM and then follow the prompts in the manager!

#### Step 6:
- Sit Back and Let the Model Download from Midori AI's Model Repo
- Don't forget to note the name of the model you just installed so you can request it for OpenAI V1 later.

Need help on how to do that? Stop by - [How to send OpenAI request to LocalAI]({{%relref "howtos/by_hand/easy-request" %}})


## Install a Hugging Face Model from the Midori AI Model Repo

#### Step 1:
- Start the Midori AI Subsystem

#### Step 2:
- On the Main Menu, Type `5` to Enter the Backend Program Menu

#### Step 3:
- On the Backend Program Menu, Type `10` to Enter the LocalAI Model Installer

#### Step 4a:
- If you have LocalAI installed in the subsystem, skip this step.
- If you do not have LocalAI installed in the subsystem, the program will ask you to enter the LocalAI docker's name. It will look something like `localai-api-1`, but not always. If you need help, reach out on the [Midori AI Discord](https://discord.gg/xdgCx3VyHU) / [Email](mailto:contact-us@midori-ai.xyz).

#### Step 4b:
- If you have GPU support installed in that image, type `yes`.
- If you do not have GPU support installed in that image, type `no`.

#### Step 5:
- Type `huggingface` when asked what size of model you would like.

#### Step 6:
- Copy and Paste the Hugging Face Download URL That You Wish to Use
- For example: `https://huggingface.co/mlabonne/gemma-7b-it-GGUF/resolve/main/gemma-7b-it.Q2_K.gguf?download=true`
![midori ai photo](https://tea-cup.midori-ai.xyz/download/0a975dc7-ff7f-42a9-a77c-8efdd5bd95e4-chrome_tC2H9nfRdA.png)
- Or you can use the huggingface naming from their api
- For example: `mlabonne/gemma-7b-it-GGUF/gemma-7b-it.Q2_K.gguf`

#### Step 7:
- Sit Back and Let the Model Download from Midori AI's Model Repo
- Don't forget to note the name of the model you just installed so you can request it for OpenAI V1 later.

Need help on how to do that? Stop by - [How to send OpenAI request to LocalAI]({{%relref "howtos/by_hand/easy-request" %}})
