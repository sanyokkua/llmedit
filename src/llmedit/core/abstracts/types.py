from enum import StrEnum


class PromptType(StrEnum):
    APP_SYSTEM_PROMPT = 'Application System Prompt',
    PROOFREADING_BASE = 'Proofreading Base Prompt',
    PROOFREADING_REWRITING = 'Proofreading Rewriting Prompt',
    PROOFREADING_CASUAL = 'Proofreading Casual Prompt',
    PROOFREADING_FRIENDLY = 'Proofreading Friendly Prompt',
    PROOFREADING_FORMAL = 'Proofreading Formal Prompt',
    PROOFREADING_SEMI_FORMAL = 'Proofreading Semi-Formal Prompt',
    TRANSFORMING_PULL_REQUEST_DESCRIPTION = 'Transforming text to pull Request Description Prompt',
    TRANSFORMING_PULL_REQUEST_COMMENT = 'Transforming text to pull Request Comment Prompt',
    TRANSFORMING_CHAT = 'Chat Prompt',
    TRANSFORMING_EMAIL = 'Email Prompt',
    TRANSFORMING_INSTRUCTION_GUIDE = 'Instruction/Guide Prompt',
    TRANSFORMING_PLAIN_DOCUMENTATION = 'Plain Documentation Prompt',
    TRANSFORMING_WIKI_DOCUMENTATION = 'Wiki Markdown Documentation Prompt',
    TRANSFORMING_SOCIAL_MEDIA_POST = 'Social Media Post Prompt',
    TRANSLATE_BASE = 'Translation Base Prompt',
    TRANSLATE_DICTIONARY = 'Translation Dictionary Prompt',


class AppTheme(StrEnum):
    DARK = 'dark',
    LIGHT = 'light',


class AppLLMProviderType(StrEnum):
    LLAMA_CPP = 'llama-cpp',
    OLLAMA = 'ollama',


class LLMRequest:
    def __init__(
            self,
            user_prompt: str,
            system_prompt: str,
    ):
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt


class LLMResponse:
    def __init__(self, content: str, metadata: dict = None):
        self.content = content
        self.metadata = metadata or {}


class AppSettings:
    def __init__(self, model_name: str,
                 model_temperature: float = 0.5,
                 app_llm_provider: AppLLMProviderType = AppLLMProviderType.LLAMA_CPP,
                 theme: AppTheme = AppTheme.DARK):
        self.model_name = model_name
        self.model_temperature = model_temperature
        self.app_llm_provider = app_llm_provider
        self.theme = theme


class LLMStatus(StrEnum):
    READY = 'READY',
    NOT_READY = 'NOT_READY',
