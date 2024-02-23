
+++
disableToc = false
title = "Easy Model Setup"
weight = 2
+++

## ----- Midori AI Easy Model Manager -----
Use the model manager to install all of the base models like ``Llava``, ``tts``, ``Stable Diffusion``, and more! [Click Link]({{%relref "howtos/easy-model-installer" %}})

## ----- By Hand Setup -----
*(You do not have to run these steps if you have already done the auto manager)*

Lets learn how to setup a model, for this ``How To`` we are going to use the ``Dolphin Mistral 7B`` model.

To download the model to your models folder, run this command in a commandline of your picking.
```bash
curl -O https://tea-cup.midori-ai.xyz/download/7bmodelQ5.gguf
```

Each model needs at least ``4`` files, with out these files, the model will run raw, what that means is you can not change settings of the model.
```
File 1 - The model's GGUF file
File 2 - The model's .yaml file
File 3 - The Chat API .tmpl file
File 4 - The Chat API helper .tmpl file
```
So lets fix that! We are using ``lunademo`` name for this ``How To`` but you can name the files what ever you want! Lets make blank files to start with

```bash
touch lunademo-chat.tmpl
touch lunademo-chat-block.tmpl
touch lunademo.yaml
```
Now lets edit the `"lunademo-chat-block.tmpl"`, This is the template that model "Chat" trained models use, but changed for LocalAI

```txt
<|im_start|>{{if eq .RoleName "assistant"}}assistant{{else if eq .RoleName "system"}}system{{else if eq .RoleName "user"}}user{{end}}
{{if .Content}}{{.Content}}{{end}}
<|im_end|>
```

For the `"lunademo-chat.tmpl"`, Looking at the huggingface repo, this model uses the ``<|im_start|>assistant`` tag for when the AI replys, so lets make sure to add that to this file. Do not add the user as we will be doing that in our yaml file!

```txt
{{.Input}}
<|im_start|>assistant
```

For the `"lunademo.yaml"` file. Lets set it up for your computer or hardware. (If you want to see advanced yaml configs - [Link](https://localai.io/advanced/))

We are going to 1st setup the backend and context size.

```yaml
context_size: 2000
```

What this does is tell ``LocalAI`` how to load the model. Then we are going to **add** our settings in after that. Lets add the models name and the models settings. The models ``name:`` is what you will put into your request when sending a ``OpenAI`` request to ``LocalAI``
```yaml
name: lunademo
parameters:
  model: 7bmodelQ5.gguf
```

Now that LocalAI knows what file to load with our request, lets add the stopwords and template files to our models yaml file now.
```yaml
stopwords:
- "user|"
- "assistant|"
- "system|"
- "<|im_end|>"
- "<|im_start|>"
template:
  chat: lunademo-chat
  chat_message: lunademo-chat-block
```

If you are running on ``GPU`` or want to tune the model, you can add settings like (higher the GPU Layers the more GPU used)
```yaml
f16: true
gpu_layers: 4
```

To fully tune the model to your like. But be warned, you **must** restart ``LocalAI`` after changing a yaml file

```bash
docker compose restart
```

If you want to check your models yaml, here is a full copy!
```yaml
context_size: 2000
##Put settings right here for tunning!! Before name but after Backend! (remove this comment before saving the file)
name: lunademo
parameters:
  model: 7bmodelQ5.gguf
stopwords:
- "user|"
- "assistant|"
- "system|"
- "<|im_end|>"
- "<|im_start|>"
template:
  chat: lunademo-chat
  chat_message: lunademo-chat-block
```

Now that we got that setup, lets test it out but sending a [request]({{%relref "easy-request" %}}) to Localai! 

