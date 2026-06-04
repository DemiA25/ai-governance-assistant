import json
import anthropic
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS
from prompts.lessons_prompts import LESSONS_SYSTEM_PROMPT, LESSONS_USER_PROMPT


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_lessons_learned(document_text: str) -> dict:
    """Generate a lessons learned report from document text using Claude."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=LESSONS_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": LESSONS_USER_PROMPT.format(
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
        cleaned = result.strip().strip("```json").strip("```").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"error": "Failed to parse lessons learned report. Please try again."}