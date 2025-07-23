import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def summarize_issue(title: str, body: str) -> dict:
    prompt = f"""You are a GitHub Issue summarizer. Given the title and full body of an issue (including comments), return a JSON with the following structure:

{{
  "summary": "A one-sentence summary of the user's problem or request.",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "A score from 1 (low) to 5 (critical), with a brief justification",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "Brief sentence on impact"
}}

Respond ONLY in JSON format.

Here's the issue:
TITLE: {title}
BODY AND COMMENTS: {body}
"""

    try:
        response = httpx.post(
            f"{GROQ_API_BASE}/chat/completions",
            headers=HEADERS,
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are an expert GitHub issue analyst."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            },
            timeout=15.0
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()

        # Try parsing JSON from response
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM response as JSON", "raw_output": content}
    except Exception as e:
        return {"error": str(e)}
