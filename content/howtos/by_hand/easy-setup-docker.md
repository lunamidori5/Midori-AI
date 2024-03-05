
+++
disableToc = false
title = "Easy Setup - Docker"
weight = 2
+++

{{% notice note %}}
It is highly recommended to check out the [Midori AI Subsystem Manager]({{%relref "subsystem/manager" %}}) for setting up LocalAI. It does all of this for you!
{{% /notice %}}

{{% notice Note %}}
- You will need about 10gb of RAM Free
- You will need about 15gb of space free on C drive for ``Docker compose``
{{% /notice %}}

We are going to run `LocalAI` with `docker compose` for this set up.

Lets setup our folders for ``LocalAI`` (run these to make the folders for you if you wish)
```batch
mkdir "LocalAI"
cd LocalAI
mkdir "models"
mkdir "images"
```

At this point we want to set up our `.env` file, here is a copy for you to use if you wish, Make sure this is in the ``LocalAI`` folder.

```bash
## Set number of threads.
## Note: prefer the number of physical cores. Overbooking the CPU degrades performance notably.
THREADS=2

## Specify a different bind address (defaults to ":8080")
# ADDRESS=127.0.0.1:8080

## Define galleries.
## models will to install will be visible in `/models/available`
GALLERIES=[{"name":"model-gallery", "url":"github:go-skynet/model-gallery/index.yaml"}, {"url": "github:go-skynet/model-gallery/huggingface.yaml","name":"huggingface"}]

## Default path for models
MODELS_PATH=/models

## Enable debug mode
DEBUG=true

## Disables COMPEL (Lets Stable Diffuser work)
COMPEL=0

## Enable/Disable single backend (useful if only one GPU is available)
# SINGLE_ACTIVE_BACKEND=true

## Specify a build type. Available: cublas, openblas, clblas.
BUILD_TYPE=cublas

## Uncomment and set to true to enable rebuilding from source
# REBUILD=true

## Enable go tags, available: stablediffusion, tts
## stablediffusion: image generation with stablediffusion
## tts: enables text-to-speech with go-piper 
## (requires REBUILD=true)
#
#GO_TAGS=tts

## Path where to store generated images
# IMAGE_PATH=/tmp

## Specify a default upload limit in MB (whisper)
# UPLOAD_LIMIT

# HUGGINGFACEHUB_API_TOKEN=Token here
```


Now that we have the `.env` set lets set up our `docker-compose` file.
It will use a container from [quay.io](https://quay.io/repository/go-skynet/local-ai?tab=tags).

{{< tabs >}}
{{% tab title="Vanilla / CPU Images" %}}
- `master`
- `latest`
- `{{< version >}}`
- `{{< version >}}-ffmpeg`
- `{{< version >}}-ffmpeg-core`

Core Images - Smaller images without predownload python dependencies
{{% /tab %}}

{{% tab title="GPU Images CUDA 11" %}}

Images with Nvidia accelleration support

> If you do not know which version of CUDA do you have available, you can check with `nvidia-smi` or `nvcc --version`

- `master-cublas-cuda11`
- `master-cublas-cuda11-core`
- `{{< version >}}-cublas-cuda11`
- `{{< version >}}-cublas-cuda11-core`
- `{{< version >}}-cublas-cuda11-ffmpeg`
- `{{< version >}}-cublas-cuda11-ffmpeg-core`

Core Images - Smaller images without predownload python dependencies
{{% /tab %}}

{{% tab title="GPU Images CUDA 12" %}}

Images with Nvidia accelleration support

> If you do not know which version of CUDA do you have available, you can check with `nvidia-smi` or `nvcc --version`

- `master-cublas-cuda12`
- `master-cublas-cuda12-core`
- `{{< version >}}-cublas-cuda12`
- `{{< version >}}-cublas-cuda12-core`
- `{{< version >}}-cublas-cuda12-ffmpeg`
- `{{< version >}}-cublas-cuda12-ffmpeg-core`

Core Images - Smaller images without predownload python dependencies

{{% /tab %}}

{{< /tabs >}}

{{< tabs >}}
{{% tab title="CPU Only" %}}
Also note this `docker-compose` file is for `CPU` only.

```docker
version: '3.6'

services:
  api:
    image: quay.io/go-skynet/local-ai:{{< version >}}
    tty: true # enable colorized logs
    restart: always # should this be on-failure ?
    ports:
      - 8080:8080
    env_file:
      - .env
    volumes:
      - ./models:/models
      - ./images/:/tmp/generated/images/
    command: ["/usr/bin/local-ai" ]
```
{{% /tab %}}

{{% tab title="GPU and CPU" %}}
Also note this `docker-compose` file is for `CUDA` only.

Please change the image to what you need.

```docker
version: '3.6'

services:
  api:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    image: quay.io/go-skynet/local-ai:CHANGEMETOIMAGENEEDED
    tty: true # enable colorized logs
    restart: always # should this be on-failure ?
    ports:
      - 8080:8080
    env_file:
      - .env
    volumes:
      - ./models:/models
      - ./images/:/tmp/generated/images/
    command: ["/usr/bin/local-ai" ]
```
{{% /tab %}}
{{< /tabs >}}


Make sure to save that in the root of the `LocalAI` folder. Then lets spin up the Docker run this in a `CMD` or `BASH`

```bash
docker compose up -d --pull always
```


Now we are going to let that set up, once it is done, lets check to make sure our huggingface / localai galleries are working (wait until you see this screen to do this)

You should see:
```
┌───────────────────────────────────────────────────┐
│                   Fiber v2.42.0                   │
│               http://127.0.0.1:8080               │
│       (bound on host 0.0.0.0 and port 8080)       │
│                                                   │
│ Handlers ............. 1  Processes ........... 1 │
│ Prefork ....... Disabled  PID ................. 1 │
└───────────────────────────────────────────────────┘
```

Now that we got that setup, lets go setup a [model]({{%relref "easy-model" %}})
