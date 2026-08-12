#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="model"
MODEL_PATH="$MODEL_DIR/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf"
MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"

mkdir -p "$MODEL_DIR"

if [[ -s "$MODEL_PATH" ]] && [[ "$(head -c 4 "$MODEL_PATH")" == "GGUF" ]]; then
  echo "Model already present and has a GGUF header: $MODEL_PATH"
  exit 0
fi

temporary_path="$MODEL_PATH.part"
curl --fail --location --retry 4 --retry-delay 3 --continue-at - \
  --output "$temporary_path" "$MODEL_URL"

if [[ "$(head -c 4 "$temporary_path")" != "GGUF" ]]; then
  echo "Downloaded file does not have a valid GGUF header." >&2
  exit 1
fi

mv "$temporary_path" "$MODEL_PATH"
echo "Downloaded model to $MODEL_PATH"
