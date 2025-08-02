#!/usr/bin/env bash

echo "Installing llama-cpp-python with OpenCL backend on Linux..."

export CMAKE_ARGS="-DLLAMA_OPENCL=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

echo "OpenCL installation completed."
