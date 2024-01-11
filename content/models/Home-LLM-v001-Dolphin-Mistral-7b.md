+++
disableToc = false
title = "Home-LLM-v001-Dolphin-Mistral-7b"
weight = 10
+++

# Model Card for Home-LLM-v001-Dolphin-Mistral-7b

The model is quantized using Lama.cpp in order to enable running the model in low resource environments that are common with Home Assistant installations such as Home PCs / Gaming computers.

The model can be used as an "Chat" type model using the ChatML prompt format. The system prompt is used to provide information about the state of the Home Assistant installation including available devices and callable services.

Example "system" prompt:
```
You are 'Al', a helpful AI Assistant that controls the devices in a house. Complete the following task as instructed with the information provided only.
Services: light.turn_off, light.turn_on, fan.turn_on, fan.turn_off
Devices:
light.office 'Office Light' = on
fan.office 'Office fan' = off
light.kitchen 'Kitchen Light' = on
```

Output from the model will consist of a response that should be relayed back to the user, along with an optional code block that will invoke different Home Assistant "services". The output format from the model for function calling is as follows:

```
turning on the kitchen lights for you now
light.turn_on(light.kitchen)
```

Due to the mix of data used during fine tuning, the model is also capable of basic instruct and QA tasks. For example, the model is able to perform basic logic tasks such as the following:

```
user if mary is 7 years old, and I am 3 years older than her. how old am I?
assistant If Mary is 7 years old, then you are 10 years old (7+3=10).
```

## Models (Quantised / Non Quantised)
| Quant Mode | Description |
|---|---|
|Q3_K_L| Smallest, significant quality loss - not recommended|
|Q4_K_M| Medium, balanced quality|
|Q5_K_M| Large, very low quality loss|
|Q6_K| Very large, extremely low quality loss|
|None| Extremely large, No quality loss, hard to install - not recommended|


## Training
The model was trained as a LoRA on an Midori AI's supercomputer using a custom training script to enable gradient checkpointing. The LoRA has rank = 256, alpha = 512, "saves" the `wte,lm_head.linear` modules The embedding weights were "saved" and trained normally along with the rank matricies in order to train the newly added tokens to the embeddings. The full model is merged together at the end.

## Authors 
Luna Midori - https://github.com/lunamidori5
Midori AI - https://io.midori-ai.xyz/
Acon96 - https://github.com/acon96
Cognitive Computations - https://erichartford.com/
MistralAI - https://mistral.ai/

## License
License: Apache-2.0 - https://choosealicense.com/licenses/apache-2.0/