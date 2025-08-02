Write-Output "Installing llama-cpp-python with CUDA backend on Windows..."

$env:CMAKE_ARGS = "-DLLAMA_CUDA=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

Write-Output "CUDA installation completed."
