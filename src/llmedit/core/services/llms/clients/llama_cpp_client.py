from llama_cpp import ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage
from llama_cpp import Llama

from core.abstracts.services import LLMModelClient
from core.abstracts.types import LLMRequest, LLMResponse


class LlamaCppModelModelClient(LLMModelClient):
    def __init__(self, llama_model: Llama, temperature: float = 0.5):
        self.llama_model = llama_model
        self.temperature = temperature

    def generate(self, request: LLMRequest) -> LLMResponse:
        user_prompt = request.user_prompt
        if not user_prompt:
            raise RuntimeError("No user prompt passed.")
        system_prompt = request.system_prompt
        if not system_prompt:
            raise RuntimeError("No system prompt passed.")

        messages: list[ChatCompletionRequestMessage] = [
            ChatCompletionRequestSystemMessage(role="system", content=system_prompt),
            ChatCompletionRequestUserMessage(role="user", content=user_prompt),
        ]

        try:
            response = self.llama_model.create_chat_completion(
                messages=messages,
                temperature=self.temperature
            )
            return LLMResponse(content=response["choices"][0]["message"]["content"])
        except Exception as e:
            print(e)
            return LLMResponse('')
