#!/usr/bin/env bash

echo "Installing llama-cpp-python with CUDA backend on Linux..."

export CMAKE_ARGS="-DLLAMA_CUDA=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

echo "CUDA installation completed."
