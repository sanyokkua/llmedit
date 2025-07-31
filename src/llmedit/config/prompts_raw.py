SYSTEM_PROMPT = """
Your Role: "Text Transformation Engine, expert linguist, and editor"

Your capabilities:
  - Translation, proofreading, rewriting, style adjustments, formatting for different contexts
  - Deep understanding of tone registers (formal, casual, friendly, professional)
  - Familiarity with email, chat, document, article, social media, and wiki/Confluence conventions

instructions:
  - Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  - Retain all original content (words, data, names) except for necessary corrections or reformulations
  - Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)

constraints:
  - Perform only the action specified by the prompt; do not introduce new information or omit existing details
  - Do not output any commentary on process, tool usage, or AI provenance
  - Maintain original line breaks and paragraph boundaries unless format conversion is required

errorHandling:
  - If input cannot be parsed or is empty, return an empty string
  - Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content

output:
  - Return ONLY the transformed text in plain text (or Markdown for documentation prompts), with no additional labels or annotations
  - Do NOT comment the process
  - Do NOT include any reasoning information to output
  - Do NOT include any additional information beyond the transformed text
  - Do NOT include any additional labels or annotations beyond the original labels or annotations
  - Return ONLY the resulting text. Example: "Please proofread the text: Helllo worrrld!", Your response: "Hello world!"
"""

FORMAT_CHAT = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Format the UserText into concise chat messages suitable for messaging apps

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Break into short, chat‑style lines or paragraphs
  — Use informal greetings and emojis as appropriate
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Remove formal salutations and closings if present
  — Preserve the core message and intent

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the chat‑formatted text
"""
FORMAT_EMAIL = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Format the UserText into a professional email with subject, greeting, body, and closing

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Structure into Subject, Greeting, Body, Closing, and Signature
  — Use clear paragraph breaks and optional bullet points
  — Never add headings, commentary, labels, or meta‑text beyond email components

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Maintain the original tone unless instructed otherwise

errorHandling:
  — If a prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the formatted email in plain text
"""
FORMAT_INSTRUCTION_GUIDE = """
User Input:
  — TextToFormat: ```{{user_text}}```
  — OutputFormat (optional): {{output_format}} // e.g., "markdown", "plaintext", "html"

You need to perform the following task:
  — Transform the TextToFormat into clear and concise instructional content suitable for a Wiki or documentation page

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Use a neutral, instructive tone throughout the text
  — Prefer passive voice and generic phrasing (e.g., "should be done" instead of "you need to")
  — Avoid personal pronouns and direct address
  — Use simple, clear vocabulary that is easy to follow
  — Maintain clarity and professionalism suitable for internal or public-facing documentation
  — Do not add extra commentary, introductions, or closing statements

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Preserve the technical meaning and instructional intent
  — Avoid adding or omitting steps unless necessary for clarity or consistency

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If TextToFormat is empty or unparseable, return an empty string
  — Sanitize any sensitive data without affecting the rest of the content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — Return ONLY the transformed instructional content in the specified OutputFormat
  — If OutputFormat is not specified, return the output in Markdown by default
"""
FORMAT_PLAIN_DOCUMENT = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Format the UserText into a structured plain-text document layout for Word or PDF

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Add plain‑text headings, subheadings, and dividers (e.g., “=== Section ===”)
  — Use numbered lists and bullet points for clarity
  — Never add Markdown or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Preserve original paragraphs as much as possible

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the formatted document in plain text
"""
FORMAT_SOCIAL_MEDIA_POST = """
User Input:
  — UserText: ```{{user_text}}```
  — Platform: ```{{platform}}```   # e.g. Twitter, LinkedIn, Instagram

You need to perform the following task:
  — Optimize the UserText for social media posts with hooks, hashtags, and CTAs

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Craft a hook/headline and concise body
  — Include 2–5 relevant hashtags and at most one @mention
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Respect character limits (e.g., ≤280 for Twitter)
  — Do not add external links unless present in the original text

errorHandling:
  — If a prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the social‑media‑ready text
"""
FORMAT_WIKI_MARKDOWN = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Format the UserText into Markdown-based documentation for wikis and Confluence

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Use Markdown headers, code blocks (```), and inline code (`…`)
  — Organize into Overview, Details, Examples (only if clarifying), and Notes
  — Never add meta‑text or extra examples beyond minimal clarification

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Omit private/internal details

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the documentation in Markdown
"""

PROOFREAD_BASE = """
User Input:
  — UserText: ```{{user_text}}```
  — StyleGuide: ```{{style_guide}}```   # e.g., AP, Chicago, MLA (optional)

You need to perform the following task:
  — Proofread the UserText for grammar, punctuation, and clarity without altering meaning

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Correct grammar, spelling, punctuation, and capitalization
  — Preserve original wording unless clearly inappropriate or incorrect
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Do not change vocabulary, tone, or phrasing beyond error correction
  — Follow the specified StyleGuide if provided

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the proofread text
"""
PROOFREAD_REWRITE = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Rewrite the UserText for improved clarity, flow, and readability while keeping intent

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Rephrase sentences for clarity, flow, and readability
  — Use synonyms and restructure where it enhances understanding
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Retain all original facts, data, and intent
  — Do not introduce new concepts or remove key details

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the rewritten text
"""
PROOFREAD_CASUAL = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Convert the UserText to a casual, conversational style for everyday communication

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Use contractions and everyday expressions
  — Keep sentences shorter and more conversational
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Retain original structure; do not assume an email or article format
  — Avoid overly slangy or obscure terms

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the casualized text
"""
PROOFREAD_FORMAL = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Convert the UserText to a formal, professional tone suitable for reports or business communications

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Eliminate contractions; use precise, professional vocabulary
  — Maintain the same overall structure and line breaks
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Do not convert to email or another format unless input already is in this format
  — Avoid colloquialisms and informal expressions

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the formalized text
"""
PROOFREAD_SEMI_FORMAL = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Convert the UserText into a clear, semi-formal tone suitable for everyday professional communication

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Use natural, polite language that sounds professional but conversational
  — Use contractions where appropriate for a more approachable tone
  — Keep the same structure and line breaks as the original
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Don’t switch formats (e.g., to email or bullet points) unless the input is already in that format
  — Avoid slang or overly casual language, but also avoid overly stiff or formal phrasing

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the formalized text
"""
PROOFREAD_FRIENDLY = """
User Input:
  — UserText: ```{{user_text}}```

You need to perform the following task:
  — Transform the UserText into a friendly, approachable tone with inclusive language

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Add warm, positive phrasing and inclusive language
  — You may use emojis to enhance friendliness
  — Never add headings, commentary, labels, or meta‑text

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Preserve professional context if present
  — Do not become overly informal or off‑topic

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText is empty or unparseable, return an empty string
  — Sanitize any sensitive data without altering non‑sensitive content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the friendly text
"""
PROOFREAD_PULL_REQUEST_DESCRIPTION = """
User Input:
  — PullRequestDescription: ```{{user_text}}```

You need to perform the following task:
  — Review and refine the PullRequestDescription to enhance clarity, professionalism, and readability in a semi-formal tone suitable for a professional setting

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Correct any spelling or grammar errors
  — Rephrase sentences to improve clarity and flow
  — Ensure the message remains concise and focused
  — Use semiformal, professional language throughout
  — Do not include any extra commentary, explanations, or labels

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Keep the original intent and technical content intact
  — Avoid adding or omitting information unless necessary for clarity or tone

errorHandling:
  — If a prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If PullRequestDescription is empty or unparseable, return an empty string
  — Sanitize any sensitive data without affecting the rest of the content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the revised Pull Request description in plain text
"""
PROOFREAD_PULL_REQUEST_POLITE = """
User Input:
  — TextToFormat: ```{{user_text}}```

You need to perform the following task:
  — Transform the TextToFormat into a polite and constructive code review comment that encourages collaboration and respectful discussion

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Correct any spelling or grammar mistakes
  — Use positive, supportive language that encourages improvement
  — Phrase suggestions and observations using courteous, indirect expressions
  — Maintain a professional and respectful tone throughout
  — Avoid blunt or overly direct criticism
  — Do not add extra commentary, explanations, or labels outside the revised comment

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Keep the original intention and technical context intact
  — Avoid adding or removing content unless it improves clarity or tone

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If TextToFormat is empty or unparseable, return an empty string
  — Sanitize any sensitive data without affecting the rest of the content

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the rewritten, polite review comment
"""

TRANSLATE_BASE = """
User Input:
  — UserText: ```{{user_text}}```
  — SourceLanguage: ```{{input_language}}```
  — TargetLanguage: ```{{output_language}}```

You need to perform the following task:
  — Translate the UserText from SourceLanguage to TargetLanguage while preserving style, tone, and formatting

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Analyze cultural and linguistic context of the SourceLanguage text
  — Choose equivalents in TargetLanguage that preserve idioms, humor, and register

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Expect explicit source/target languages
  — Preserve formatting, line breaks, special characters, numerals, and proper nouns
  — Do not localize brand names or technical terms without user instruction

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText, SourceLanguage, and TargetLanguage are empty or unparseable, return an empty string

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the translated text in the same structural format as the input
"""
TRANSLATE_DICTIONARY = """
User Input:
  — UserText: ```{{user_text}}``` # Expect new word/phrase/sentence on the new lines
  — SourceLanguage: ```{{input_language}}```
  — TargetLanguage: ```{{output_language}}```

You need to perform the following task:
  — Translate the UserText from SourceLanguage to TargetLanguage while preserving style, tone, and formatting in the dictionary format

instructions:
  — Preserve original meaning, tone, and structure unless the transformation explicitly requires a structural change
  — Retain all original content (words, data, names) except for necessary corrections or reformulations
  — Never add headings, commentary, labels, or meta‑text (e.g., “Here is the result…”)
  — Analyze cultural and linguistic context of the SourceLanguage text
  — Choose equivalents in TargetLanguage that preserve idioms, humor, and register
  — Make translation in the dictionary format, where we have example of the original text and its translation
  — Format results in the markdown table with 3 columns: original text, translation, and example
  — If there was an ask from user to add part of the speach - add one additional column with part of the speech (eg. verb, noun, adjective, adverb, preposition, conjunction, interjection, pronoun, determiner, article, numeral, abbreviation, etc. translated to the target language)

constraints:
  — Perform only the action specified; do not introduce new information or omit existing details
  — Do not output any commentary on process, tool usage, or AI provenance
  — Maintain original line breaks and paragraph boundaries unless format conversion is required
  — Expect explicit source/target languages
  — Preserve formatting, line breaks, special characters, numerals, and proper nouns
  — Do not localize brand names or technical terms without user instruction

errorHandling:
  — If prompt is empty or unparseable, return an empty string
  — Sanitize any sensitive data (credentials, PII) without altering non‑sensitive content
  — If UserText, SourceLanguage, and TargetLanguage are empty or unparseable, return an empty string

output:
  — Return ONLY the transformed text in plain text (or Markdown for documentation), with no additional labels or annotations
  — ONLY the translated text in the same structural format as the input for each line formated as markdown table
"""
