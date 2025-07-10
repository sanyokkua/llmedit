from abc import ABC, abstractmethod


class LLMRequest:
    def __init__(self, user_prompt: str, system_prompt: str, temperature: float, model: str) -> None:
        self.user_prompt: str = user_prompt
        self.system_prompt: str = system_prompt
        self.model: str = model
        self.temperature: float = temperature


class ILLMClient(ABC):

    @abstractmethod
    def get_models(self) -> list[str]:
        pass

    @abstractmethod
    def load_model(self, model_name: str):
        pass

    @abstractmethod
    def get_last_used_model(self) -> str:
        pass

    @abstractmethod
    def get_current_state(self) -> str:
        pass

    @abstractmethod
    def get_answer(self, llm_request: LLMRequest) -> str:
        pass
