Write-Output "Installing llama-cpp-python with OpenCL backend on Windows..."

$env:CMAKE_ARGS = "-DLLAMA_OPENCL=on"
poetry run pip install --force-reinstall --no-binary llama-cpp-python llama-cpp-python

Write-Output "OpenCL installation completed."
