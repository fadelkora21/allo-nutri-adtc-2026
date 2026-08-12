#!/usr/bin/env bash
set -euo pipefail

# Run on Ubuntu 22.04 with internet access. The model is intentionally not
# redistributed in this repository; verify its current license before use.
git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
cmake -S llama.cpp -B llama.cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build llama.cpp/build --config Release -j 4 --target llama-cli llama-bench
bash download_model.sh
echo "export LLAMA_CLI=$PWD/llama.cpp/build/bin/llama-cli"
echo "export ALLO_NUTRI_MODEL=$PWD/model/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf"
echo "export PATH=$PWD/llama.cpp/build/bin:\$PATH"
