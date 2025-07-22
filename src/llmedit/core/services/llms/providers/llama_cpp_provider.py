import gc
from pathlib import Path
from typing import List

from llama_cpp import Llama

from core.abstracts.providers import LLMModelClientProvider
from core.abstracts.services import LLMModelClient
from core.services.llms.clients.llama_cpp_client import LlamaCppModelModelClient


class LlamaCppProvider(LLMModelClientProvider):
    def __init__(self, model_dir: Path, temperature: float = 0.5):
        self.model_dir = model_dir
        self.last_used_model: str | None = None
        self.llama_model: Llama | None = None
        self.temperature = temperature

    def get_model_client(self) -> LLMModelClient:
        if self.llama_model is None:
            raise RuntimeError("No model loaded. Call `load_model` first.")
        return LlamaCppModelModelClient(llama_model=self.llama_model, temperature=self.temperature)

    def get_available_models(self) -> List[str]:
        return [f.name for f in self.model_dir.glob("*.gguf")]

    def load_model(self, model_name: str) -> None:
        self.last_used_model = model_name
        print(f"Loading model: {model_name}")
        self.llama_model = Llama(
            model_path=str(self.model_dir / f"{model_name}.gguf"),
            n_ctx=4096,
            n_threads=8,
            n_gpu_layers=-1,  # Load all layers to GPU (Metal on Mac M1+)
            use_mlock=True
        )
        print(f"Loading {model_name} is finished")

    def unload_model(self) -> None:
        self.last_used_model = None
        del self.llama_model
        self.llama_model = None
        gc.collect()
