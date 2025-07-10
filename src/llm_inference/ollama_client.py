import json
from datetime import datetime, timezone

import ollama
from ollama import GenerateResponse, ProcessResponse

from src.llm_inference.client import ILLMClient, LLMRequest


def format_model_info(data: ProcessResponse) -> str:
    try:
        models = data["models"]
        now = datetime.now(timezone.utc)
        formatted_models = []

        for model in models:
            name = model.get("name", "Unknown")
            vram_bytes = model.get("size_vram", 0)
            expires_at_str = model.get("expires_at")

            vram_gb = vram_bytes / (1024 ** 3)

            try:
                expires_at = datetime.fromisoformat(expires_at_str)
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                delta_minutes = (expires_at - now).total_seconds() / 60
                delta_minutes = round(delta_minutes)
            except (ValueError, TypeError):
                delta_minutes = "N/A"

            formatted_models.append(
                f"{name}, VRAM:{vram_gb:.2f} GB, Will Be Stopped at: {delta_minutes} min"
            )

        return "\n".join(formatted_models)

    except json.JSONDecodeError:
        return "Invalid JSON input"


class OllamaClient(ILLMClient):

    def __init__(self):
        self.last_used_model: str | None = None
        pass

    def get_last_used_model(self) -> str:
        return self.last_used_model if self.last_used_model is not None else "None"

    def get_models(self) -> list[str]:
        ollama_list = ollama.list()
        models = [model['model'] for model in ollama_list.models]
        print(models)
        return models

    def load_model(self, model_name: str):
        self.last_used_model = model_name
        response = ollama.generate(
            model=model_name,
            prompt='Hello',
            system='You are echo service',
            think=False,
        )
        print(response['response'])

    def get_current_state(self) -> str:
        ollama_ps = ollama.ps()
        info = format_model_info(ollama_ps)
        print(info)
        return info

    def get_answer(self, llm_request: LLMRequest) -> str:
        self.last_used_model = llm_request.model
        response: GenerateResponse = ollama.generate(
            model=llm_request.model,
            prompt=llm_request.user_prompt,
            system=llm_request.system_prompt,
            options={
                "temperature": llm_request.temperature,
            }
        )
        print(response.response)
        print(response.thinking)
        return response.response
