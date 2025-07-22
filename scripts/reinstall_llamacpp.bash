#!/bin/bash

echo "Installing llama-cpp-python with Metal backend..."

export CMAKE_ARGS="-DLLAMA_METAL=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

echo "Installing llama-cpp-python with Metal backend ended"