import ollama
from ollama import GenerateResponse

from core.abstracts.services import LLMModelClient
from core.abstracts.types import LLMRequest, LLMResponse


class OllamaModelClient(LLMModelClient):
    def __init__(self, model_name: str, temperature: float = 0.5):
        self.model_name = model_name
        self.temperature = temperature

    def generate(self, request: LLMRequest) -> LLMResponse:
        user_prompt = request.user_prompt
        if not user_prompt:
            raise RuntimeError("No user prompt passed.")
        system_prompt = request.system_prompt
        if not system_prompt:
            raise RuntimeError("No system prompt passed.")

        try:
            response: GenerateResponse = ollama.generate(
                model=self.model_name,
                prompt=user_prompt,
                system=system_prompt,
                options={
                    "temperature": self.temperature,
                }
            )
            print(response.thinking)
            print(response.response)
            return LLMResponse(content=response.response)
        except Exception as e:
            print(e)
            return LLMResponse('')
