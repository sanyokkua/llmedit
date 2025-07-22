from huggingface_hub import hf_hub_download

DEFAULT_DESTINATION = "data/models"

def download_model(repo_id: str, filename: str, dest_path: str):
    hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=dest_path,
    )

download_model(
    repo_id="unsloth/gemma-3n-E4B-it-GGUF",
    filename="gemma-3n-E4B-it-Q4_K_M.gguf",
    dest_path=DEFAULT_DESTINATION
)

download_model(
    repo_id="unsloth/gemma-3-12b-it-GGUF",
    filename="gemma-3-12b-it-Q4_K_M.gguf",
    dest_path=DEFAULT_DESTINATION
)

download_model(
    repo_id="Qwen/Qwen3-14B-GGUF",
    filename="Qwen3-14B-Q4_K_M.gguf",
    dest_path=DEFAULT_DESTINATION
)