import os
import json
import re
from typing import Dict, Any
from graph_utils import compute_insights

# Optional: Initialize Gemini / OpenAI client here if API key is present
# e.g., google.genai, openai, etc.
USE_MOCK_FALLBACK = os.getenv("USE_MOCK_FALLBACK", "false").lower() == "true"

SYSTEM_PROMPT = """You are an investigative intelligence analyst engine.
Extract entities and relationships from messy police / investigative notes.

Allowed Entity Types:
- PERSON, LOCATION, VEHICLE, PHONE, ORGANIZATION, MONEY

Allowed Relationship Types:
- MET, CONTACTED, TRANSFERRED_MONEY, OWNS, VISITED, WORKS_FOR, CONNECTED_TO

Strict Rules:
1. Every entity MUST have a unique "id" (e.g. p1, p2, l1, v1), "name", and "type".
2. Every relationship MUST reference valid entity IDs in "source" and "target", and have a valid "type".
3. Return ONLY a valid JSON object matching this schema:
{
  "entities": [{"id": "...", "name": "...", "type": "..."}],
  "relationships": [{"source": "...", "target": "...", "type": "..."}]
}
Do not include markdown fences, preambles, or explanations."""

def _clean_json_response(raw_text: str) -> Dict[str, Any]:
    """Strips markdown code ticks if returned by the LLM."""
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return json.loads(raw_text)

def _get_mock_fallback(text: str) -> Dict[str, Any]:
    """Guarantees immediate team unblocking if LLM API is unavailable or slow."""
    return {
        "entities": [
            { "id": "p1", "name": "Rahul", "type": "PERSON" },
            { "id": "p2", "name": "Arjun", "type": "PERSON" },
            { "id": "p3", "name": "Vikram", "type": "PERSON" },
            { "id": "p4", "name": "Sameer", "type": "PERSON" },
            { "id": "l1", "name": "Park Street", "type": "LOCATION" },
            { "id": "m1", "name": "₹50,000", "type": "MONEY" },
            { "id": "v1", "name": "WB02AB1234", "type": "VEHICLE" }
        ],
        "relationships": [
            { "source": "p1", "target": "p2", "type": "MET" },
            { "source": "p1", "target": "l1", "type": "VISITED" },
            { "source": "p2", "target": "l1", "type": "VISITED" },
            { "source": "p2", "target": "m1", "type": "TRANSFERRED_MONEY" },
            { "source": "m1", "target": "p3", "type": "TRANSFERRED_MONEY" },
            { "source": "p3", "target": "v1", "type": "OWNS" },
            { "source": "p3", "target": "p4", "type": "CONTACTED" },
            { "source": "p4", "target": "p1", "type": "MET" }
        ]
    }

def extract_intelligence(text: str) -> Dict[str, Any]:
    """
    Main extraction function.
    Input: raw text string.
    Output: { entities: [...], relationships: [...], insights: [...] }
    """
    if not text or not text.strip():
        return {"entities": [], "relationships": [], "insights": []}

    extracted_data = None

    if not USE_MOCK_FALLBACK:
        try:
            # --- LLM API CALL BLOCK ---
            # Replace with your active LLM provider SDK call:
            # response = client.models.generate_content(
            #     model="gemini-2.5-flash",
            #     contents=f"{SYSTEM_PROMPT}\n\nEvidence Text:\n{text}"
            # )
            # extracted_data = _clean_json_response(response.text)
            pass
        except Exception as e:
            print(f"[WARN] LLM API failure: {e}. Falling back to default baseline.")

    # Fallback if API is unconfigured or failed
    if not extracted_data:
        extracted_data = _get_mock_fallback(text)

    # Compute graph metrics & add intelligence layer
    entities = extracted_data.get("entities", [])
    relationships = extracted_data.get("relationships", [])
    insights = compute_insights(entities, relationships)

    return {
        "entities": entities,
        "relationships": relationships,
        "insights": insights
    }

if __name__ == "__main__":
    sample_text = "Rahul met Arjun at Park Street. Arjun transferred ₹50,000 to Vikram. Vikram owns vehicle WB02AB1234."
    result = extract_intelligence(sample_text)
    print(json.dumps(result, indent=2))