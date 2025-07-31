from enum import StrEnum


class PromptCategory(StrEnum):
    SYSTEM = "system"
    PROOFREAD = "proofread"
    FORMAT = "format"
    TRANSLATE = "translate"
