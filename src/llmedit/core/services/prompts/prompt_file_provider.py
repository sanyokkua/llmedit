from pathlib import Path

from core.abstracts.providers import PromptProvider
from core.abstracts.types import PromptType

PROMPT_TYPE_TO_FILE_NAME: dict[PromptType, str] = {
    PromptType.APP_SYSTEM_PROMPT: "systemPrompt.txt",
    PromptType.PROOFREADING_BASE: 'userPromptParametrizedProofreadBase.txt',
    PromptType.PROOFREADING_REWRITING: 'userPromptParametrizedProofreadRewrite.txt',
    PromptType.PROOFREADING_CASUAL: 'userPromptParametrizedProofreadCasual.txt',
    PromptType.PROOFREADING_FRIENDLY: 'userPromptParametrizedProofreadFriendly.txt',
    PromptType.PROOFREADING_FORMAL: 'userPromptParametrizedProofreadFormal.txt',
    PromptType.PROOFREADING_SEMI_FORMAL: 'userPromptParametrizedProofreadSemiFormal.txt',
    PromptType.TRANSFORMING_PULL_REQUEST_DESCRIPTION: 'userPromptParametrizedProofreadPullRequestDescription.txt',
    PromptType.TRANSFORMING_PULL_REQUEST_COMMENT: 'userPromptParametrizedProofreadPullRequestPoliteComment.txt',
    PromptType.TRANSFORMING_CHAT: 'userPromptParametrizedFormatTextChat.txt',
    PromptType.TRANSFORMING_EMAIL: 'userPromptParametrizedFormatTextEmail.txt',
    PromptType.TRANSFORMING_INSTRUCTION_GUIDE: 'userPromptParametrizedFormatTextInstructionGuide.txt',
    PromptType.TRANSFORMING_PLAIN_DOCUMENTATION: 'userPromptParametrizedFormatTextPlainDocument.txt',
    PromptType.TRANSFORMING_WIKI_DOCUMENTATION: 'userPromptParametrizedFormatTextWikiMarkdown.txt',
    PromptType.TRANSFORMING_SOCIAL_MEDIA_POST: 'userPromptParametrizedFormatTextSocialMediaPost.txt',
    PromptType.TRANSLATE_BASE: 'userPromptParametrizedTranslateBase.txt',
    PromptType.TRANSLATE_DICTIONARY: 'userPromptParametrizedTranslateDictionary.txt',
}


class PromptFileProvider(PromptProvider):
    def __init__(self, prompt_dir: Path):
        self.prompt_dir = prompt_dir
        self._cache: dict[str, str] = {}

    def _load_prompt(self, filename: str) -> str:
        if filename not in self._cache:
            path = self.prompt_dir / filename
            try:
                self._cache[filename] = path.read_text(encoding='utf-8').strip()
            except FileNotFoundError:
                raise ValueError(f"Prompt file not found: {path}")
        return self._cache[filename]

    def get_prompt(self, prompt_type: PromptType) -> str:
        prompt_file_name = PROMPT_TYPE_TO_FILE_NAME.get(prompt_type)
        prompt = self._load_prompt(prompt_file_name)
        print(f"Loaded prompt: {prompt}")
        return prompt
