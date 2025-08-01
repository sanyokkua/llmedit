from enum import StrEnum


class PromptCategory(StrEnum):
    """
    Enumeration of prompt categories used to classify and organize prompts.

    Each category corresponds to a specific type of text processing task.
    """
    SYSTEM = "system"
    PROOFREAD = "proofread"
    FORMAT = "format"
    TRANSLATE = "translate"
