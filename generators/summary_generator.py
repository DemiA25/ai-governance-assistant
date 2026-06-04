import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from prompts.summary_prompts import SUMMARY_SYSTEM_PROMPT, SUMMARY_USER_PROMPT


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_executive_summary(document_text: str) -> str:
    """Generate an executive summary from document text using Claude."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SUMMARY_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": SUMMARY_USER_PROMPT.format(
                    document_text=document_text
                ),
            }
        ],
        temperature=0.3,
    )

    return response.content[0].text