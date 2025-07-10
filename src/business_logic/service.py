from src.business_logic.interface import ILLMProvider, ILanguageProvider, ITextTools, IPromptProvider, OperationOptions, \
    ITextSanitizer
from src.llm_inference.client import ILLMClient, LLMRequest


class LanguageService(ILanguageProvider):
    def __init__(self):
        self.languages = ['English', 'Ukrainian', 'Croatian']

    def get_supported_languages(self) -> list[str]:
        return self.languages


class LLMProvider(ILLMProvider):
    def __init__(self, client: ILLMClient):
        self.client = client

    def get_loaded_model(self) -> str:
        if self.client.get_last_used_model() is not None:
            return self.client.get_last_used_model()
        else:
            res = self.client.get_current_state()
            if res is not None and res.strip() != "":
                return res.split("\n")[0]
            return "None"

    def get_available_models(self) -> list[str]:
        return self.client.get_models()

    def load_model(self, model_name: str):
        self.client.load_model(model_name)

    def get_client(self) -> ILLMClient:
        return self.client


class TextTools(ITextTools):
    def __init__(self, client: ILLMClient, prompt_provider: IPromptProvider, sanitizer: ITextSanitizer):
        self.client = client
        self.prompt_provider = prompt_provider
        self.sanitizer = sanitizer

    def translate_text(self, source_language: str, target_language: str, oper_ops: OperationOptions) -> str:
        prompt = self.prompt_provider.get_translation_prompt(source_language, target_language)
        llm_req: LLMRequest = LLMRequest(user_prompt=oper_ops.content, system_prompt=prompt,
                                         temperature=oper_ops.temperature, model=oper_ops.model)
        return self.sanitizer.sanitize_text(self.client.get_answer(llm_req))

    def _make_request(self, oper_ops: OperationOptions, prompt: str) -> str:
        llm_req: LLMRequest = LLMRequest(user_prompt=oper_ops.content, system_prompt=prompt,
                                         temperature=oper_ops.temperature, model=oper_ops.model)
        return self.sanitizer.sanitize_text(self.client.get_answer(llm_req))

    def make_proofread(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_proofread_prompt())

    def make_rewrite(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_rewrite_prompt())

    def make_regenerate(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_regenerate_prompt())

    def make_formal(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_formal_prompt())

    def make_casual(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_casual_prompt())

    def make_friendly(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_friendly_prompt())

    def make_email(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_email_prompt())

    def make_chat(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_chat_prompt())

    def make_document(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_document_prompt())

    def make_social_media_post(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_social_media_post_prompt())

    def make_articles(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_articles_prompt())

    def make_documentation(self, oper_ops: OperationOptions) -> str:
        return self._make_request(oper_ops, self.prompt_provider.get_documentation_prompt())
