"""
deduplication.py

Purpose:
Remove duplicate and low-quality search results.
"""


def clean_results(results: list[dict]) -> list[dict]:
    """
    Remove duplicate URLs, duplicate titles,
    and empty search results.
    """

    seen_urls = set()
    seen_titles = set()

    cleaned = []

    for result in results:
        url = result.get("url", "").strip()
        title = result.get("title", "").strip()
        content = result.get("content", "").strip()

        if not url:
            continue

        if not content:
            continue

        if url in seen_urls:
            continue

        if title in seen_titles:
            continue

        seen_urls.add(url)
        seen_titles.add(title)

        cleaned.append(result)

    return cleaned
