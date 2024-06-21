#!/bin/bash

echo "===> LocalAI All-in-One (AIO) container starting..."

GPU_ACCELERATION=false
GPU_VENDOR=""

function check_intel() {
    if lspci | grep -E 'VGA|3D' | grep -iq intel; then
        echo "Intel GPU detected"
        if [ -d /opt/intel ]; then
            GPU_ACCELERATION=true
            GPU_VENDOR=intel
        else
            echo "Intel GPU detected, but Intel GPU drivers are not installed. GPU acceleration will not be available."
        fi
    fi
}

function check_nvidia_wsl() {
    if lspci | grep -E 'VGA|3D' | grep -iq "Microsoft Corporation Device 008e"; then
        # We make the assumption this WSL2 cars is NVIDIA, then check for nvidia-smi
        # Make sure the container was run with `--gpus all` as the only required parameter
        echo "NVIDIA GPU detected via WSL2"
        # nvidia-smi should be installed in the container
        if nvidia-smi; then
            GPU_ACCELERATION=true
            GPU_VENDOR=nvidia
        else
            echo "NVIDIA GPU detected via WSL2, but nvidia-smi is not installed. GPU acceleration will not be available."
        fi
    fi
}

function check_amd() {
    if lspci | grep -E 'VGA|3D' | grep -iq amd; then
        echo "AMD GPU detected"
        # Check if ROCm is installed
        if [ -d /opt/rocm ]; then
            GPU_ACCELERATION=true
            GPU_VENDOR=amd
        else
            echo "AMD GPU detected, but ROCm is not installed. GPU acceleration will not be available."
        fi
    fi
}

function check_nvidia() {
    if lspci | grep -E 'VGA|3D' | grep -iq nvidia; then
        echo "NVIDIA GPU detected"
        # nvidia-smi should be installed in the container
        if nvidia-smi; then
            GPU_ACCELERATION=true
            GPU_VENDOR=nvidia
        else
            echo "NVIDIA GPU detected, but nvidia-smi is not installed. GPU acceleration will not be available."
        fi
    fi
}

function check_metal() {
    if system_profiler SPDisplaysDataType | grep -iq 'Metal'; then
        echo "Apple Metal supported GPU detected"
        GPU_ACCELERATION=true
        GPU_VENDOR=apple
    fi
}

function detect_gpu() {
    case "$(uname -s)" in
        Linux)
            check_nvidia
            check_amd
            check_intel
            check_nvidia_wsl
            ;;
        Darwin)
            check_metal
            ;;
    esac
}

function detect_gpu_size() {
    # Attempting to find GPU memory size for NVIDIA GPUs
    if [ "$GPU_ACCELERATION" = true ] && [ "$GPU_VENDOR" = "nvidia" ]; then
        echo "NVIDIA GPU detected. Attempting to find memory size..."
        # Using head -n 1 to get the total memory of the 1st NVIDIA GPU detected.
        # If handling multiple GPUs is required in the future, this is the place to do it
        nvidia_sm=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -n 1)
        if [ ! -z "$nvidia_sm" ]; then
            echo "Total GPU Memory: $nvidia_sm MiB"
            # if bigger than 8GB, use 16GB
            #if [ "$nvidia_sm" -gt 8192 ]; then
            #    GPU_SIZE=gpu-16g
            #else
            GPU_SIZE=gpu-8g
            #fi
        else
            echo "Unable to determine NVIDIA GPU memory size. Falling back to CPU."
            GPU_SIZE=gpu-8g
        fi
    elif [ "$GPU_ACCELERATION" = true ] && [ "$GPU_VENDOR" = "intel" ]; then
        GPU_SIZE=intel
    # Default to a generic GPU size until we implement GPU size detection for non NVIDIA GPUs
    elif [ "$GPU_ACCELERATION" = true ]; then
        echo "Non-NVIDIA GPU detected. Specific GPU memory size detection is not implemented."
        GPU_SIZE=gpu-8g

    # default to cpu if GPU_SIZE is not set
    else
        echo "GPU acceleration is not enabled or supported. Defaulting to CPU."
        GPU_SIZE=cpu
    fi
}

function check_vars() {
    if [ -z "$MODELS" ]; then
        echo "MODELS environment variable is not set. Please set it to a comma-separated list of model YAML files to load."
        exit 1
    fi

    if [ -z "$PROFILE" ]; then
        echo "PROFILE environment variable is not set. Please set it to one of the following: cpu, gpu-8g, gpu-16g, apple"
        exit 1
    fi
}

detect_gpu
detect_gpu_size

PROFILE="${PROFILE:-$GPU_SIZE}" # default to cpu
export MODELS="${MODELS:-/aio/${PROFILE}/embeddings.yaml,/aio/${PROFILE}/rerank.yaml,/aio/${PROFILE}/text-to-speech.yaml,/aio/${PROFILE}/image-gen.yaml,/aio/${PROFILE}/text-to-text.yaml,/aio/${PROFILE}/speech-to-text.yaml,/aio/${PROFILE}/vision.yaml}"

check_vars

set -e

cd /models

if [ ! -f en_US-amy-medium.onnx.json ]; then
	midori_ai_downloader en_US-amy-medium.onnx.json
fi
if [ ! -f en_US-amy-medium.onnx ]; then
	midori_ai_downloader en_US-amy-medium.onnx
fi
if [ ! -f en-us-kathleen-low.onnx.json ]; then
	midori_ai_downloader en-us-kathleen-low.onnx.json
fi
if [ ! -f en-us-kathleen-low.onnx ]; then
	midori_ai_downloader en-us-kathleen-low.onnx
fi

if [ ! -f diffusers.yaml ]; then
	midori_ai_downloader diffusers.yaml
fi

if [ ! -f bert-embeddings.yaml ]; then
	midori_ai_downloader bert-embeddings.yaml
fi
if [ ! -f bert-MiniLM-L6-v2q4_0.bin ]; then
	midori_ai_downloader bert-MiniLM-L6-v2q4_0.bin
fi

if [ ! -f ggml-model-q4_k.gguf ]; then
	wget --no-check-certificate --no-cache --no-cookies  https://tea-cup.midori-ai.xyz/download/llava-v1.5-13b-Q6_K.gguf
    mv llava-v1.5-13b-Q6_K.gguf ggml-model-q4_k.gguf
fi
if [ ! -f mmproj-model-f16.gguf ]; then
    wget --no-check-certificate --no-cache --no-cookies  https://tea-cup.midori-ai.xyz/download/mmproj-model-f16.gguf
    
fi
if [ ! -f chat-simple.tmpl ]; then
	wget --no-check-certificate --no-cache --no-cookies https://github.com/mudler/LocalAI/blob/b8240b4c1839089b9d06a3e2b1c629a294cff87e/examples/configurations/llava/chat-simple.tmpl
fi
if [ ! -f llava.yaml ]; then
	wget --no-check-certificate --no-cache --no-cookies https://github.com/mudler/LocalAI/blob/b8240b4c1839089b9d06a3e2b1c629a294cff87e/examples/configurations/llava/llava.yaml
fi

##https://huggingface.co/mys/ggml_bakllava-1/resolve/main/ggml-model-q4_k.gguf

cd /

cd /build

# If we have set EXTRA_BACKENDS, then we need to prepare the backends
if [ -n "$EXTRA_BACKENDS" ]; then
	echo "EXTRA_BACKENDS: $EXTRA_BACKENDS"
	# Space separated list of backends
	for backend in $EXTRA_BACKENDS; do
		echo "Preparing backend: $backend"
		make -C $backend
	done
fi

if [ "$REBUILD" != "false" ]; then
	rm -rf ./local-ai
	make build -j${BUILD_PARALLELISM:-1}
else
	echo "@@@@@"
	echo "Skipping rebuild"
	echo "@@@@@"
	echo "If you are experiencing issues with the pre-compiled builds, try setting REBUILD=true"
	echo "If you are still experiencing issues with the build, try setting CMAKE_ARGS and disable the instructions set as needed:"
	echo 'CMAKE_ARGS="-DLLAMA_F16C=OFF -DLLAMA_AVX512=OFF -DLLAMA_AVX2=OFF -DLLAMA_FMA=OFF"'
	echo "see the documentation at: https://localai.io/basics/build/index.html"
	echo "Note: See also https://github.com/go-skynet/LocalAI/issues/288"
	echo "@@@@@"
	echo "CPU info:"
	grep -e "model\sname" /proc/cpuinfo | head -1
	grep -e "flags" /proc/cpuinfo | head -1
	if grep -q -e "\savx\s" /proc/cpuinfo ; then
		echo "CPU:    AVX    found OK"
	else
		echo "CPU: no AVX    found"
	fi
	if grep -q -e "\savx2\s" /proc/cpuinfo ; then
		echo "CPU:    AVX2   found OK"
	else
		echo "CPU: no AVX2   found"
	fi
	if grep -q -e "\savx512" /proc/cpuinfo ; then
		echo "CPU:    AVX512 found OK"
	else
		echo "CPU: no AVX512 found"
	fi
	echo "@@@@@"
fi

echo "===> Starting LocalAI[$PROFILE] with the following models: $MODELS"

exec /build/entrypoint.sh "$@"