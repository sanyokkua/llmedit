from config.prompts_raw import SYSTEM_PROMPT, FORMAT_CHAT, FORMAT_EMAIL, FORMAT_INSTRUCTION_GUIDE, \
    FORMAT_PLAIN_DOCUMENT, FORMAT_SOCIAL_MEDIA_POST, FORMAT_WIKI_MARKDOWN, PROOFREAD_BASE, PROOFREAD_REWRITE, \
    PROOFREAD_CASUAL, PROOFREAD_FORMAL, PROOFREAD_SEMI_FORMAL, PROOFREAD_FRIENDLY, PROOFREAD_PULL_REQUEST_DESCRIPTION, \
    PROOFREAD_PULL_REQUEST_POLITE, TRANSLATE_BASE, TRANSLATE_DICTIONARY
from core.models.data_types import Prompt
from core.models.enums.prompt import PromptCategory

ID_PROMPT_SYSTEM = 'prompt_system'
ID_PROMPT_FORMAT_CHAT = 'prompt_format_chat'
ID_PROMPT_FORMAT_EMAIL = 'prompt_format_email'
ID_PROMPT_FORMAT_INSTRUCTION_GUIDE = 'prompt_format_instruction_guide'
ID_PROMPT_FORMAT_PLAIN_DOCUMENT = 'prompt_format_plain_document'
ID_PROMPT_FORMAT_SOCIAL_MEDIA_POST = 'prompt_format_social_media_post'
ID_PROMPT_FORMAT_WIKI_MARKDOWN = 'prompt_format_wiki_markdown'
ID_PROMPT_PROOFREAD_BASE = 'prompt_proofread_base'
ID_PROMPT_PROOFREAD_REWRITE = 'prompt_proofread_rewrite'
ID_PROMPT_PROOFREAD_CASUAL = 'prompt_proofread_casual'
ID_PROMPT_PROOFREAD_FORMAL = 'prompt_proofread_formal'
ID_PROMPT_PROOFREAD_SEMI_FORMAL = 'prompt_proofread_semi_formal'
ID_PROMPT_PROOFREAD_FRIENDLY = 'prompt_proofread_friendly'
ID_PROMPT_PROOFREAD_PR_DESCRIPTION = 'prompt_proofread_pull_request_description'
ID_PROMPT_PROOFREAD_PR_POLITE = 'prompt_proofread_pull_request_polite'
ID_PROMPT_TRANSLATE_BASE = 'prompt_translate_base'
ID_PROMPT_TRANSLATE_DICTIONARY = 'prompt_translate_dictionary'

PROMPT_PARAM_USER_TEXT = "user_text"
PROMPT_PARAM_INPUT_LANGUAGE = "input_language"
PROMPT_PARAM_OUTPUT_LANGUAGE = "output_language"

APPLICATION_PROMPTS = [
    Prompt(
        id=ID_PROMPT_SYSTEM,
        name='System Prompt',
        description='Defines the overall behavior, constraints, and capabilities of the assistant.',
        category=PromptCategory.SYSTEM,
        template=SYSTEM_PROMPT,
        parameters=[]
    ),

    Prompt(
        id=ID_PROMPT_FORMAT_CHAT,
        name='Format Chat',
        description='Formats output for casual, conversational interactions.',
        category=PromptCategory.FORMAT,
        template=FORMAT_CHAT,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_FORMAT_EMAIL,
        name='Format Email',
        description='Structures content to be suitable for professional or personal email communication.',
        category=PromptCategory.FORMAT,
        template=FORMAT_EMAIL,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_FORMAT_INSTRUCTION_GUIDE,
        name='Format Instruction',
        description='Converts content into a clear, step-by-step instructional format.',
        category=PromptCategory.FORMAT,
        template=FORMAT_INSTRUCTION_GUIDE,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_FORMAT_PLAIN_DOCUMENT,
        name='Format Plain Document',
        description='Prepares clean, unstyled text suitable for plain documents or internal notes.',
        category=PromptCategory.FORMAT,
        template=FORMAT_PLAIN_DOCUMENT,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_FORMAT_SOCIAL_MEDIA_POST,
        name='Format Post for Social Media',
        description='Adapts content to be engaging and concise for platforms like Twitter, LinkedIn, or Instagram.',
        category=PromptCategory.FORMAT,
        template=FORMAT_SOCIAL_MEDIA_POST,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_FORMAT_WIKI_MARKDOWN,
        name='Format Document Markdown WiKi',
        description='Structures content using wiki-style Markdown for documentation or collaborative platforms.',
        category=PromptCategory.FORMAT,
        template=FORMAT_WIKI_MARKDOWN,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_BASE,
        name='Proofread',
        description='Identifies and corrects grammar, spelling, and clarity issues in the text.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_BASE,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_REWRITE,
        name='Rewrite',
        description='Rephrases the text while preserving meaning and improving tone or readability.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_REWRITE,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_CASUAL,
        name='Make Casual',
        description='Adapts formal or neutral text into a friendly, informal style.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_CASUAL,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_FORMAL,
        name='Make Formal',
        description='Elevates the tone of content for professional, academic, or official contexts.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_FORMAL,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_SEMI_FORMAL,
        name='Make SemiFormal',
        description='Balances friendliness with professionalism for versatile communication.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_SEMI_FORMAL,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_FRIENDLY,
        name='Make Friendly',
        description='Infuses the text with warmth and approachability.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_FRIENDLY,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_PR_DESCRIPTION,
        name='Make PR Description',
        description='Refines pull request descriptions to be clear, concise, and informative.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_PULL_REQUEST_DESCRIPTION,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_PROOFREAD_PR_POLITE,
        name='Make PR comment',
        description='Polishes pull request comments for respectful and constructive feedback.',
        category=PromptCategory.PROOFREAD,
        template=PROOFREAD_PULL_REQUEST_POLITE,
        parameters=[PROMPT_PARAM_USER_TEXT]
    ),

    Prompt(
        id=ID_PROMPT_TRANSLATE_BASE,
        name='Translate',
        description='Translates text into a target language using natural and fluent phrasing.',
        category=PromptCategory.TRANSLATE,
        template=TRANSLATE_BASE,
        parameters=[PROMPT_PARAM_USER_TEXT, PROMPT_PARAM_INPUT_LANGUAGE, PROMPT_PARAM_OUTPUT_LANGUAGE]
    ),

    Prompt(
        id=ID_PROMPT_TRANSLATE_DICTIONARY,
        name='Translate as Dictionary',
        description='Provides word-for-word translations with contextual definitions.',
        category=PromptCategory.TRANSLATE,
        template=TRANSLATE_DICTIONARY,
        parameters=[PROMPT_PARAM_USER_TEXT, PROMPT_PARAM_INPUT_LANGUAGE, PROMPT_PARAM_OUTPUT_LANGUAGE]
    ),
]
