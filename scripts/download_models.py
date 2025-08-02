import sys
from dataclasses import dataclass

from huggingface_hub import hf_hub_download

DEFAULT_DESTINATION = "data/models"


@dataclass(frozen=True)
class ModelInformation:
    name: str
    repositoryId: str
    fileName: str


PREDEFINED_GGUF_MODELS = [
    ModelInformation(
        name='DeepSeek-R1-Distill-Llama-8B',
        repositoryId='unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF',
        fileName='DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Qwen3-8B (Reasoning)',
        repositoryId='unsloth/Qwen3-8B-GGUF',
        fileName='Qwen3-8B-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Qwen3-8B (Non-Reasoning)',
        repositoryId='unsloth/Qwen3-8B-GGUF',
        fileName='Qwen3-8B-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Qwen3-14B (Reasoning)',
        repositoryId='unsloth/Qwen3-14B-GGUF',
        fileName='Qwen3-14B-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Qwen3-14B (Non-Reasoning)',
        repositoryId='unsloth/Qwen3-14B-GGUF',
        fileName='Qwen3-14B-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Qwen3-30B-A3B-Instruct-2507',
        repositoryId='unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF',
        fileName='Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='gemma-3n-E4B-it',
        repositoryId='unsloth/gemma-3n-E4B-it-GGUF',
        fileName='gemma-3n-E4B-it-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='gemma-3-12b-it-qat',
        repositoryId='unsloth/gemma-3-12b-it-qat-GGUF',
        fileName='gemma-3-12b-it-qat-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='gemma-3-27b-it-qat',
        repositoryId='unsloth/gemma-3-27b-it-qat-GGUF',
        fileName='gemma-3-27b-it-qat-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Mistral-Small-3.2-24B-Instruct-2506',
        repositoryId='unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF',
        fileName='Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf',
    ),
    ModelInformation(
        name='Llama-3.1-8B-Instruct',
        repositoryId='unsloth/Llama-3.1-8B-Instruct-GGUF',
        fileName='Llama-3.1-8B-Instruct-Q4_K_M.gguf',
    )
]


def download_model(repo_id: str, filename: str, dest_path: str):
    """Download model from Hugging Face Hub to specified destination"""
    print(f"\nDownloading {filename} from {repo_id}...")
    try:
        hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=dest_path,
            local_dir_use_symlinks=False,
        )
        print(f"✓ Successfully downloaded to {dest_path}/{repo_id}/{filename}")
    except Exception as e:
        print(f"✗ Download failed: {str(e)}")
        sys.exit(1)


def main():
    # Display available models
    print("Available models to download:")

    PREDEFINED_GGUF_MODELS.sort(key=lambda x: x.name)

    for idx, model in enumerate(PREDEFINED_GGUF_MODELS, 1):
        print(f"{idx}. {model.name}")

    # Get user selection
    while True:
        try:
            choice = int(input(f"\nEnter model number (1-{len(PREDEFINED_GGUF_MODELS)}): "))
            if 1 <= choice <= len(PREDEFINED_GGUF_MODELS):
                break
            print(f"Invalid number. Please enter a number between 1 and {len(PREDEFINED_GGUF_MODELS)}.")
        except ValueError:
            print("Please enter a valid number.")

    # Download selected model
    selected_model = PREDEFINED_GGUF_MODELS[choice - 1]
    download_model(
        repo_id=selected_model.repositoryId,
        filename=selected_model.fileName,
        dest_path=DEFAULT_DESTINATION,
    )

    print("\nDownload complete! Model is ready for use.")


if __name__ == "__main__":
    main()
