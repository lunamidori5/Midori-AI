ARG BASE_IMAGE=quay.io/go-skynet/local-ai:v2.12.4-cublas-cuda12-ffmpeg

FROM ubuntu:22.04 as builder


RUN apt update && \
    apt install -y python3-pip

RUN python3 --version

RUN pip3 install pyinstaller

WORKDIR /build
COPY . .

RUN pip install cryptography aiohttp tk
RUN pip install -r ./other_files/model_installer/requirements.txt

RUN pyinstaller --onefile --distpath /opt/midori-ai/ ./other_files/model_installer/yaml_edit.py
RUN pyinstaller --onefile --distpath /opt/midori-ai/ -n midori_ai_downloader ./other_files/model_installer/support.py
RUN pyinstaller --onefile --distpath /opt/midori-ai/ -n hf-downloader ./other_files/midori_ai_manager/huggingface_downloader.py

FROM ${BASE_IMAGE}

RUN mkdir -p /models &&\
    apt update && \
    apt install -y wget

COPY --from=builder /opt/midori-ai/ /opt/midori-ai/
COPY --from=builder --chmod=755 /build/other_files/subsystem_docker_stuff/localai/supporting_files/localai_entrypoint.sh /build/entrypoint_md_ai.sh