from core.abstracts.providers import PromptProvider
from core.abstracts.services import TextTransformation, LLMModelClient, TextSanitizer, PromptValidator
from core.abstracts.types import PromptType, LLMRequest


class TransformationService(TextTransformation):
    def __init__(self,
                 llm_model_client: LLMModelClient,
                 prompt_provider: PromptProvider,
                 prompt_validator: PromptValidator,
                 text_sanitizer: TextSanitizer,
                 ):
        self.llm_model_client = llm_model_client
        self.prompt_provider = prompt_provider
        self.prompt_validator = prompt_validator
        self.text_sanitizer = text_sanitizer

    def process_text(self, text: str, prompt_type: PromptType) -> str:
        system_prompt = self.prompt_provider.get_prompt(PromptType.APP_SYSTEM_PROMPT)
        user_prompt = self.prompt_provider.get_prompt(prompt_type)

        if not self.prompt_validator.validate_prompt(user_prompt):
            raise ValueError("Invalid prompt")

        user_prompt = user_prompt.replace("{{user_text}}", text)
        llm_request = LLMRequest(user_prompt, system_prompt)
        print(llm_request)
        content = self.llm_model_client.generate(llm_request).content
        return self.text_sanitizer.sanitize_text(content)
