+++
disableToc = false
title = "Easy Setup - Stable Diffusion"
weight = 2
+++

## ----- Midori AI Easy Model installer -----
Use the model installer to install all of the base models like ``Llava``, ``tts``, ``Stable Diffusion``, and more! [Click Link]({{%relref "howtos/easy-model-installer" %}})

## ----- By Hand Setup -----
*(You do not have to run these steps if you have already done the auto installer)*

In your ``models`` folder make a file called ``stablediffusion.yaml``, then edit that file with the following. (You can change ``dreamlike-art/dreamlike-anime-1.0`` with what ever model you would like.)
```yaml
name: animagine
parameters:
  model: dreamlike-art/dreamlike-anime-1.0
backend: diffusers
cuda: true
f16: true
diffusers:
  scheduler_type: dpm_2_a
```

If you are using docker, you will need to run in the localai folder with the ``docker-compose.yaml`` file in it
```bash
docker compose down
```

Then in your ``.env`` file uncomment this line.
```yaml
COMPEL=0
```

After that we can reinstall the LocalAI docker VM by running in the localai folder with the ``docker-compose.yaml`` file in it
```bash
docker compose up -d
```

Then to download and setup the model, Just send in a normal ``OpenAI`` request! LocalAI will do the rest!
```bash
curl http://localhost:8080/v1/images/generations -H "Content-Type: application/json" -d '{
  "prompt": "Two Boxes, 1blue, 1red",
  "size": "1024x1024"
}'
```
