from src.business_logic.interface import ILLMProvider, ILanguageProvider, ITextSanitizer, ITextTools, IPromptProvider
from src.business_logic.service import LLMProvider, LanguageService, TextTools
from src.llm_inference.ollama_client import OllamaClient
from src.prompts.provider import PromptProvider
from src.sanitizer.service import TextSanitizer


class AppContext:
    def __init__(self, llm_provider: ILLMProvider, language_provider: ILanguageProvider, text_tools: ITextTools,
                 prompt_provider: IPromptProvider, sanitizer: ITextSanitizer):
        self._llm_provider: ILLMProvider = llm_provider
        self._language_provider: ILanguageProvider = language_provider
        self._text_tools: ITextTools = text_tools
        self._prompt_provider: IPromptProvider = prompt_provider
        self._sanitizer: ITextSanitizer = sanitizer

    @property
    def llm_provider(self) -> ILLMProvider:
        return self._llm_provider

    @property
    def language_provider(self) -> ILanguageProvider:
        return self._language_provider

    @property
    def text_tools(self) -> ITextTools:
        return self._text_tools

    @property
    def prompt_provider(self) -> IPromptProvider:
        return self._prompt_provider

    @property
    def sanitizer(self) -> ITextSanitizer:
        return self._sanitizer


def get_app_context() -> AppContext:
    llm_client = OllamaClient()
    llm_provider = LLMProvider(llm_client)
    language_provider = LanguageService()
    prompt_provider = PromptProvider()
    sanitizer = TextSanitizer()
    text_tools = TextTools(llm_client, prompt_provider, sanitizer)

    return AppContext(llm_provider=llm_provider, language_provider=language_provider, text_tools=text_tools,
                      prompt_provider=prompt_provider, sanitizer=sanitizer)
