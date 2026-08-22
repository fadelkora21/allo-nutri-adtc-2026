#!/usr/bin/env bash

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MODEL_DIR="$HERE/model"
MODEL_FILE="$MODEL_DIR/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf"
PARTIAL_FILE="$MODEL_FILE.part"

MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"

mkdir -p "$MODEL_DIR"

is_valid_gguf() {
    local file="$1"

    if [[ ! -s "$file" ]]; then
        return 1
    fi

    [[ "$(head -c 4 "$file")" == "GGUF" ]]
}

if is_valid_gguf "$MODEL_FILE"; then
    echo "Model already present and valid:"
    echo "$MODEL_FILE"
    exit 0
fi

if [[ -f "$MODEL_FILE" ]]; then
    echo "Removing invalid or incomplete model file."
    rm -f "$MODEL_FILE"
fi

echo "Downloading the ALLO NUTRI GGUF model..."
echo "Source: $MODEL_URL"
echo "Destination: $MODEL_FILE"

if command -v curl >/dev/null 2>&1; then
    curl \
        --fail \
        --location \
        --retry 4 \
        --retry-delay 3 \
        --continue-at - \
        --output "$PARTIAL_FILE" \
        "$MODEL_URL"
elif command -v wget >/dev/null 2>&1; then
    wget \
        --continue \
        --output-document="$PARTIAL_FILE" \
        "$MODEL_URL"
else
    echo "Error: curl or wget is required." >&2
    exit 1
fi

if ! is_valid_gguf "$PARTIAL_FILE"; then
    echo "Error: the downloaded file is not a valid GGUF model." >&2
    rm -f "$PARTIAL_FILE"
    exit 1
fi

mv "$PARTIAL_FILE" "$MODEL_FILE"

echo "Model downloaded and validated successfully:"
echo "$MODEL_FILE"
