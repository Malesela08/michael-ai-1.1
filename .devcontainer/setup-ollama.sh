#!/usr/bin/env bash
set -euo pipefail

if ! command -v zstd >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y zstd
fi

curl -fsSL https://ollama.com/install.sh | sh

if ! curl --silent --fail http://127.0.0.1:11434/api/tags >/dev/null; then
    ollama serve > ollama.log 2>&1 &
fi

for _ in $(seq 1 30); do
    if curl --silent --fail http://127.0.0.1:11434/api/tags >/dev/null; then
        ollama pull llama3.2
        exit 0
    fi
    sleep 1
done

echo "Ollama did not become ready on 127.0.0.1:11434; see ollama.log." >&2
exit 1
