#!/bin/bash

MODEL=${1:-llama3}

echo "Starting Michael AI with $MODEL..."

ollama run $MODEL
