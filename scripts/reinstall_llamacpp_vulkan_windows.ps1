Write-Output "Installing llama-cpp-python with Vulkan backend on Windows..."

$env:CMAKE_ARGS = "-DLLAMA_VULKAN=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

Write-Output "Vulkan installation completed."
