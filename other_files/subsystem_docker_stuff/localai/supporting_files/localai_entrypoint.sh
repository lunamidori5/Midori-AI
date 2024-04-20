#!/bin/bash
set -e

cd /models

if [ ! -f 7bmodelQ6.gguf ]; then
	midori_ai_downloader 7bmodelQ6.gguf
fi
if [ ! -f starter-7b-gpu.yaml ]; then
	midori_ai_downloader starter-7b-gpu.yaml
fi
if [ ! -f starter-7b-cpu.yaml ]; then
	midori_ai_downloader starter-7b-cpu.yaml
fi

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
	wget --no-check-certificate --no-cache --no-cookies https://huggingface.co/PsiPi/liuhaotian_llava-v1.5-13b-GGUF/resolve/main/llava-v1.5-13b-Q6_K.gguf
	mv llava-v1.5-13b-Q6_K.gguf ggml-model-q4_k.gguf
fi
if [ ! -f mmproj-model-f16.gguf ]; then
	wget --no-check-certificate --no-cache --no-cookies https://huggingface.co/PsiPi/liuhaotian_llava-v1.5-13b-GGUF/resolve/main/mmproj-model-f16.gguf
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

./local-ai "$@"