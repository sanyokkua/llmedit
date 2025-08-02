#!/usr/bin/env bash

echo "Installing llama-cpp-python with Vulkan backend on Linux..."

export CMAKE_ARGS="-DLLAMA_VULKAN=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

echo "Vulkan installation completed."
