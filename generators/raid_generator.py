import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from prompts.raid_prompts import RAID_SYSTEM_PROMPT, RAID_USER_PROMPT


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_raid_log(document_text: str) -> dict:
    """Generate a RAID log from document text using Claude."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=RAID_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": RAID_USER_PROMPT.format(
                    document_text=document_text
                ),
            }
        ],
        temperature=0.2,
    )

    result = response.content[0].text

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        # Sometimes the model wraps JSON in backticks — strip them
        cleaned = result.strip().strip("```json").strip("```").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"error": "Failed to parse RAID log. Please try again."}