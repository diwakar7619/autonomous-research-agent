"""
tavily_service.py

Purpose:
Handles all communication with the Tavily Search API.

Responsibilities:
- Search the web
- Return structured search results
- Handle API errors

Does NOT:
- Summarize content
- Remove duplicates
- Save to database
"""

from tavily import TavilyClient

from config import TAVILY_API_KEY


# Create Tavily client
client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web using Tavily.

    Args:
        query (str): User search query.
        max_results (int): Maximum number of search results.

    Returns:
        list[dict]:
            A list containing structured search results.
    """

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
            include_images=False,
            include_raw_content=False,
        )

        return response.get("results", [])

    except Exception as e:
        raise RuntimeError(f"Tavily Search Failed: {e}")
