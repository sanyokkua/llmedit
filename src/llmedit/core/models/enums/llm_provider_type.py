from enum import StrEnum


class LlmProviderType(StrEnum):
    """
    Enumeration of supported LLM provider types.

    Defines the available backends for language model execution.
    """
    LLAMA_CPP = "Llama.cpp"
    OLLAMA = "Ollama"
