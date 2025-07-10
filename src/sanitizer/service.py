import re

from src.business_logic.interface import ITextSanitizer


class TextSanitizer(ITextSanitizer):
    def sanitize_text(self, text: str) -> str:
        # Remove <think>…</think> (non-greedy, across lines)
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        # Strip leading/trailing whitespace
        return cleaned.strip()
