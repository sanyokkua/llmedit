from core.abstracts.services import PromptValidator


class TranslationPromptValidator(PromptValidator):
    def validate_prompt(self, prompt: str) -> bool:
        if not prompt or len(prompt.strip()) == 0:
            return False
        return "{{user_text}}" in prompt and "{{input_language}}" in prompt and "{{output_language}}" in prompt


class TextGenericPromptValidator(PromptValidator):
    def validate_prompt(self, prompt: str) -> bool:
        if not prompt or len(prompt.strip()) == 0:
            return False
        return "{{user_text}}" in prompt
