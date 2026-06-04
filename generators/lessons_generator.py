import json
import re
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

    # Try parsing directly
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        pass

    # Strip markdown backticks
    cleaned = result.strip()
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object in the response
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {"error": "Failed to parse lessons learned report. Please try again."}