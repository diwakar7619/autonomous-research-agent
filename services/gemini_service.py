"""
gemini_service.py

Purpose:
Handles all interactions with the Gemini API.

Responsibilities:
- Accept cleaned search results
- Generate a structured research summary

Does NOT:
- Search the web
- Remove duplicates
- Generate PDFs
"""

import json


from google import genai


from config import GOOGLE_API_KEY


client = genai.Client(api_key=GOOGLE_API_KEY)


def summarize_results(search_results: list[dict]) -> dict:
    """
    Generate a structured summary using Gemini.

    Args:
        search_results: List of Tavily search results.

    Returns:
        dict containing:
        - key_points
        - important_findings
        - actionable_insights
        - sources
    """

    prompt = f"""
You are an expert research assistant.

Analyze the following search results.

Return ONLY valid JSON.

Structure:

{{
  "key_points": [],
  "important_findings": [],
  "actionable_insights": [],
  "sources": []
}}

Search Results:

{json.dumps(search_results, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    clean_text = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(clean_text)
